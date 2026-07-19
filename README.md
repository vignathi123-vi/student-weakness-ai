\# Concepto



An AI agent that analyzes a student's written test answers and identifies exactly

which underlying concept they're weak in. Not just the broad topic. For example,

instead of saying "weak in Algebra," it identifies "weak in factorial simplification"

or "weak in trigonometric table values," along with whether the mistake looks like a

conceptual gap or a careless calculation slip.



\*\*Live demo:\*\* https://student-weakness-ai.onrender.com



\## Why this exists



Marks alone don't tell a student or teacher \*why\* a mistake happened. Two students

can both get a question wrong for completely different reasons, one has a real gap

in understanding, the other made a careless slip despite knowing the method. This

agent tells those two cases apart.



\## How it works



1\. \*\*Question Bank\*\*  each question is pre-tagged with the specific concept it

&#x20;  tests, plus the key terms/values a correct answer must contain.

2\. \*\*Answer Matching\*\*  a student's typed answer is checked against the required

&#x20;  elements for that question (full match / partial match / missing).

3\. \*\*Concept-Level Diagnosis\*\*  results are aggregated by concept (not by topic),

&#x20;  producing a status (Strong / Partial Gap / Weak) and a specific reason.



\## Example



Given a student's answers to 8 questions across 4 concepts (factorials, angle-sum

property, trig table values, quadratic formula application), the agent correctly

distinguishes:

\- A student who is genuinely weak in two concepts (missing steps entirely)

\- A student who gets the \*method\* right but the \*final value\* wrong (a slip, not a

&#x20; conceptual gap) flagged differently from a true gap



\## Tech stack



\- \*\*Backend:\*\* Python, Flask (REST API)

\- \*\*Matching engine:\*\* rule-based text matching against a pre-tagged question bank

\- \*\*Frontend:\*\* plain HTML/CSS/JS (no framework)  question form + diagnosis report

\- \*\*Deployment:\*\* Render (free tier)

\- \*\*Prior phase:\*\* an earlier ML model (Extra Trees Classifier, 86.7% accuracy)

&#x20; trained on simulated topic-level answer-sheet data, kept in this repo under

&#x20; `weak\_topic\_model\_training.ipynb` as the foundational experiment this project

&#x20; grew out of.



\## Project structure

