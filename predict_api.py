from flask import Flask, request, jsonify, render_template
import json

app = Flask(__name__)

with open("question_bank.json") as f:
    qbank = json.load(f)["questions"]
qbank_lookup = {q["id"]: q for q in qbank}


def check_answer(answer_text, question):
    text = answer_text.lower()
    required = [str(e).lower() for e in question["required_elements"]]
    partial = [str(e).lower() for e in question["partial_credit_elements"]]

    required_present = all(elem in text for elem in required)
    partial_present = all(elem in text for elem in partial)

    if required_present:
        return "full"
    elif partial_present:
        return "partial"
    else:
        return "missing"


def diagnose_concepts(student_results):
    import pandas as pd
    df = pd.DataFrame(student_results)

    concept_summary = []
    for concept, group in df.groupby("concept"):
        total = len(group)
        full = (group["match_status"] == "full").sum()
        partial = (group["match_status"] == "partial").sum()
        missing = (group["match_status"] == "missing").sum()

        score = (full * 1 + partial * 0.5) / total

        if score >= 0.8:
            status = "Strong"
        elif score >= 0.5:
            status = "Partial gap"
        else:
            status = "Weak"

        if missing > 0 and partial == 0:
            reason = "Missing key steps/values entirely — likely a conceptual gap"
        elif partial > 0 and missing == 0:
            reason = "Method correct but final answer wrong — likely a calculation slip"
        elif missing > 0 and partial > 0:
            reason = "Mixed: some conceptual gaps, some calculation errors"
        else:
            reason = "Consistently correct"

        concept_summary.append({
            "concept": concept,
            "status": status,
            "score": round(score, 2),
            "reason": reason
        })

    return sorted(concept_summary, key=lambda x: x["score"])


def full_diagnosis_pipeline(answers_dict):
    results = []
    for q_id, answer_text in answers_dict.items():
        if q_id not in qbank_lookup:
            continue
        question = qbank_lookup[q_id]
        match_status = check_answer(answer_text, question)
        results.append({
            "question_id": q_id,
            "concept": question["concept"],
            "match_status": match_status
        })
    return diagnose_concepts(results)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/questions", methods=["GET"])
def get_questions():
    """Returns the question bank so the frontend can display questions to answer."""
    return jsonify(qbank)


@app.route("/diagnose", methods=["POST"])
def diagnose_endpoint():
    data = request.get_json()
    answers = data.get("answers", {})
    diagnosis = full_diagnosis_pipeline(answers)
    return jsonify({"diagnosis": diagnosis})


if __name__ == "__main__":
    app.run(port=5000, debug=True)