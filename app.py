import os
import json
import concurrent.futures
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

COT_SYSTEM = (
    "Think step by step. Number each reasoning step clearly as 'Step 1:', 'Step 2:', etc. "
    "Be concise. End your response with 'Final answer:' followed by your conclusion."
)

ANALYSIS_SYSTEM = (
    "You are a JSON-only response system. "
    "Return only valid JSON with no markdown, no backticks, no explanation whatsoever."
)


def generate_trace(question: str) -> str:
    """Call the LLM once and return a chain-of-thought trace."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=800,
        messages=[
            {"role": "system", "content": COT_SYSTEM},
            {"role": "user",   "content": question}
        ]
    )
    return response.choices[0].message.content


def analyze_consistency(question: str, traces: list) -> str:
    """Ask the LLM to compare the 3 traces and score each step's uncertainty."""
    prompt = f"""Question: "{question}"

TRACE 1:
{traces[0]}

TRACE 2:
{traces[1]}

TRACE 3:
{traces[2]}

Parse TRACE 1 into its individual reasoning steps (include the final answer as the last step).
For each step assign an uncertainty score 0.0-1.0 based on cross-trace consistency:
  0.0 = same reasoning appears identically in all 3 traces  (very certain)
  1.0 = contradicted or completely absent in other traces   (very uncertain)

Return ONLY this JSON structure, nothing else:
{{"steps":[{{"text":"...","uncertainty":0.0,"note":"one-sentence reason for this score"}}]}}"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=1500,
        messages=[
            {"role": "system", "content": ANALYSIS_SYSTEM},
            {"role": "user",   "content": prompt}
        ]
    )
    return response.choices[0].message.content


def safe_parse_json(raw: str) -> dict:
    """Parse JSON, stripping accidental markdown fences if present."""
    cleaned = raw.replace("```json", "").replace("```", "").strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        import re
        match = re.search(r"\{[\s\S]*\}", cleaned)
        if match:
            return json.loads(match.group())
        raise ValueError(f"Could not parse JSON from model response:\n{raw}")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json(force=True)
    question = (data.get("question") or "").strip()
    if not question:
        return jsonify({"error": "Please enter a question."}), 400

    try:
        # Generate 3 independent CoT traces in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
            futures = [pool.submit(generate_trace, question) for _ in range(3)]
            traces = [f.result() for f in futures]

        # Score each step's uncertainty via cross-trace consistency
        raw_analysis = analyze_consistency(question, traces)
        analysis = safe_parse_json(raw_analysis)

        return jsonify({"traces": traces, "steps": analysis.get("steps", [])})

    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


if __name__ == "__main__":
    print("\n  CoT Uncertainty Visualiser")
    print("  Open http://localhost:5000 in your browser\n")
    app.run(debug=True, port=5000)
