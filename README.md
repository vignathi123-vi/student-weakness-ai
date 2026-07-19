# Concepto

An AI agent that analyzes a student's written test answers and identifies exactly which underlying concept they're weak in — not just the broad topic. For example, instead of saying "weak in Algebra," it identifies "weak in factorial simplification" or "weak in trigonometric table values," along with whether the mistake looks like a conceptual gap or a careless calculation slip.

**Live demo:** https://student-weakness-ai.onrender.com

## Why this exists

Marks alone don't tell a student or teacher why a mistake happened. Two students can both get a question wrong for completely different reasons — one has a real gap in understanding, the other made a careless slip despite knowing the method. This agent tells those two cases apart.

## How it works

1. **Question Bank** each question is pre-tagged with the specific concept it tests, plus the key terms/values a correct answer must contain.
2. **Answer Matching** a student's typed answer is checked against the required elements for that question (full match / partial match / missing).
3. **Concept-Level Diagnosis** results are aggregated by concept (not by topic), producing a status (Strong / Partial Gap / Weak) and a specific reason.

## Example

Given a student's answers to 8 questions across 4 concepts (factorials, angle-sum property, trig table values, quadratic formula application), the agent correctly distinguishes:

 A student who is genuinely weak in two concepts (missing steps entirely)
 A student who gets the method right but the final value wrong (a calculation slip, not a conceptual gap) — flagged differently from a true gap

## Tech stack

 **Backend:** Python, Flask (REST API)
 **Matching engine:** rule-based text matching against a pre-tagged question bank
 **Frontend:** plain HTML/CSS/JS (no framework) — question form + diagnosis report
 **Deployment:** Render (free tier)
 **Prior phase:** an earlier ML model (Extra Trees Classifier, 86.7% accuracy) trained on simulated topic-level answer-sheet data, kept in this repo under weak_topic_model_training.ipynb as the foundational experiment this project grew out of.

## Project structure

concepto/
├── predict_api.py                     - Flask API, the live agent
├── question_bank.json                 - Pre-tagged questions with required answer elements
├── student_answers.json               - Sample test data (3 example students)
├── templates/
│   └── index.html                     - Web UI, question form and diagnosis report
├── weak_topic_model_training.ipynb    - Earlier ML prototype (topic-level, synthetic data)
├── data/                              - Synthetic dataset used in the earlier ML phase
├── models/                            - Saved trained model from the earlier ML phase
├── outputs/                           - Charts and results from the earlier ML phase
├── requirements.txt
├── Procfile                           - Render deployment config
└── runtime.txt                        - Python version pin for deployment

## Running locally

pip install -r requirements.txt
python predict_api.py

Then open http://127.0.0.1:5000

## Known limitations

- Matching is rule-based (keyword and required-element checking), not true language understanding — an answer phrased very differently from the expected wording could be misjudged. This is an explicit, known tradeoff for this prototype stage.
- Currently supports typed/printed answers; handwritten OCR is a planned next phase.
- The question bank is built per-test rather than generated automatically from any arbitrary question paper — that generalization is future work.

## Future work

- OCR integration for scanned handwritten answer sheets
- Auto-generating question banks from uploaded question papers
- Orchestration via automation tools (e.g. n8n) for automatic parent/student alerts
- Expanding the concept library beyond the current 4-concept prototype

