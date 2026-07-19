from flask import Flask, request, jsonify
import pandas as pd
import joblib

app = Flask(__name__)
model = joblib.load("models/weak_topic_model.pkl")
feature_cols = ["silly_rate", "conceptual_rate", "calculation_rate", "avg_time_ratio"]

def mistake_rate(group, mtype):
    wrong = group[group["is_correct"] == 0]
    if len(wrong) == 0:
        return 0.0
    return (wrong["mistake_type"] == mtype).mean()

def diagnose(answer_rows):
    student_df = pd.DataFrame(answer_rows)
    topic_features = []
    for topic, group in student_df.groupby("topic"):
        topic_features.append({
            "topic": topic,
            "silly_rate": mistake_rate(group, "silly"),
            "conceptual_rate": mistake_rate(group, "conceptual"),
            "calculation_rate": mistake_rate(group, "calculation"),
            "avg_time_ratio": (group["time_taken_sec"] / group["expected_time_sec"]).mean(),
        })
    tf = pd.DataFrame(topic_features)
    X_new = tf[feature_cols]
    tf["predicted_weak"] = model.predict(X_new)
    tf["weak_probability"] = model.predict_proba(X_new)[:, 1]

    weak = tf[tf["predicted_weak"] == 1].sort_values("weak_probability", ascending=False)
    results = []
    for _, row in weak.iterrows():
        reasons = {"silly": row["silly_rate"], "conceptual": row["conceptual_rate"],
                   "calculation": row["calculation_rate"]}
        main_reason = max(reasons, key=reasons.get)
        results.append({
            "topic": row["topic"],
            "confidence": round(float(row["weak_probability"]), 2),
            "main_reason": main_reason,
            "time_ratio": round(float(row["avg_time_ratio"]), 2)
        })
    return {"weak_topics": results, "total_weak": len(results)}

@app.route("/diagnose", methods=["POST"])
def diagnose_endpoint():
    data = request.get_json()
    result = diagnose(data["answers"])
    return jsonify(result)

if __name__ == "__main__":
    app.run(port=5000, debug=True)