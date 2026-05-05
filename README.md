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
