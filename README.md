# CoT Uncertainty Visualiser
### Step-level hallucination detection via multi-trace consistency

A research prototype built for Yunrui Zhang's Winter Research Project 3 at Monash University.

---

## What it does

Most AI tools tell you "I'm 70% confident" for the whole answer.
This tool finds **which specific reasoning step** the AI is uncertain about.

It works by:
1. Asking the same question 3 times independently
2. Comparing the reasoning steps across all 3 answers
3. Flagging steps that are inconsistent or contradicted = uncertain

---

## Setup (takes ~2 minutes)

### 1. Get an Anthropic API key
Go to https://console.anthropic.com and create a free API key.

### 2. Clone / download this project
```bash
cd cot-uncertainty
```

### 3. Create a virtual environment
```bash
python -m venv venv

# Mac/Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Add your API key
```bash
cp .env.example .env
# Open .env and replace "your_api_key_here" with your actual key
```

### 6. Run the app
```bash
python app.py
```

### 7. Open your browser
Go to **http://localhost:5000**

---

## Project structure

```
cot-uncertainty/
├── app.py                  # Flask backend — API calls + routing
├── templates/
│   └── index.html          # Frontend UI
├── requirements.txt
├── .env.example
└── README.md
```

---

## Research context

This prototype implements a simplified version of **semantic consistency sampling**,
a real uncertainty quantification technique from the ML literature (related to
Kuhn et al., "Semantic Uncertainty", ICLR 2023).

The key contribution vs existing tools:
- **Existing tools**: single scalar confidence score for the whole answer
- **This tool**: per-step uncertainty scores localised to individual reasoning steps

This directly addresses the research direction described in Project 3 of
Yunrui Zhang's Winter Research Projects 2026 at Monash University.

## Example Outputs

### Test 1 — Catching a hallucination mid-chain
**Question:** *"Did Einstein fail mathematics at school?"*

<img width="800" alt="screenshot_einstein_myth" src="https://github.com/user-attachments/assets/f57e7744-6dda-4e1e-aa8d-76fe6b92f880" />

The tool samples 3 independent reasoning traces and compares them step by step.
Step 2 is flagged at **91% uncertainty** — this is exactly where the myth lives.
The AI contradicts itself across traces on whether Einstein "failed" or "excelled".
Notably, all 3 traces still converge on the correct final answer, but the tool
exposes that the reasoning path was unreliable.

---

### Test 2 — High confidence on a factual maths question
**Question:** *"What is 15% of 200?"*

<img width="800" alt="screenshot_math_certain" src="https://github.com/user-attachments/assets/e5f3018b-2754-44dc-96bc-6102a7d217ab" />

All 4 reasoning steps score below 10% uncertainty. Every trace follows the
exact same algebraic steps and arrives at the same answer (30). This shows
the tool is not just randomly flagging things red — it correctly recognises
when the model is genuinely certain.

---

### Test 3 — Pinpointing the exact step where the logic breaks
**Question:** *"A bat and ball cost $1.10. The bat costs $1 more than the ball. How much does the ball cost?"*

<img width="800" alt="screenshot_bat_ball_logic" src="https://github.com/user-attachments/assets/7976774e-8cb7-4f8a-ab68-857eec24c347" />

This is a classic cognitive bias trap — the intuitive answer ($0.10) is wrong,
the correct answer is $0.05. 2 out of 3 traces give the wrong answer.
The tool flags Steps 2 and 3 at **88% and 82% uncertainty** — precisely the
steps where traces diverge between the intuitive shortcut and the correct algebra.
The final answer step is also flagged uncertain (68%) because the traces genuinely
disagree on the answer itself.
