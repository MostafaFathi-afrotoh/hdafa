markdown
# HDAFA — Hyper-Deterministic Atomic Agentic Architecture

> **A multi-agent system that wraps probabilistic LLM generation inside a deterministic verification shell.**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Paper](https://img.shields.io/badge/Paper-PDF-red.svg)](paper/HDAFA_Final_Paper.pdf)

**Author:** Mustafa Fathy AbdelTawab Youssef
**Email:** afracosh12@gmail.com
**ORCID:** [0009-0000-4920-9333](https://orcid.org/0009-0000-4920-9333)

---

## 📖 Overview

HDAFA is a multi-agent architecture that transforms natural-language descriptions
into **verifiable** HTML/CSS pages through three specialized, atomic agents:
Task → Analyzer → JSON Schema → Coder → HTML → Validator → PASS/FAIL

text

The core hypothesis:

> **Structure + Deterministic Verification = More Reliable Output**

Unlike typical LLM-based code generators, HDAFA separates the **probabilistic**
step (generation) from the **deterministic** step (verification). The Validator
uses zero AI — only algorithmic checks — so its verdicts are reproducible and
auditable.

---

## 🏗️ Architecture

| Agent | Role | Input | Output |
|-------|------|-------|--------|
| **Requirements Analyzer** | Parses natural-language task | Task description | JSON Schema |
| **HTML/CSS Coder** | Generates the web page | JSON Schema | Complete HTML |
| **Deterministic Validator** | Verifies the output | HTML + Schema | PASS/FAIL + coverage |

### Design Principles

1. **Hyper-Atomicity** — Each agent performs exactly one task.
2. **Deterministic Outer Shell** — Verification is algorithmic, not AI-based.
3. **Ephemeral Agents** — No shared state between invocations.
4. **Closed-Loop Verification** — No output passes without validation.
5. **Intelligence Stratification** — Lighter models for atomic tasks.

---

## 📊 Key Results

Evaluated on **14 web generation tasks** across 5 categories
(services, e-commerce, landing pages, personal portfolios, edge cases),
using `gemini-3.5-flash-lite` with `temperature=0.0`.

| System | Pass Rate | Avg Coverage | Avg Retries | Avg Time |
|--------|:---------:|:------------:|:-----------:|:--------:|
| Single-Agent | 100.0% | 85.0% | 0.00 | 9.8s |
| Single+Validator | 92.9% | 84.8% | 0.14 | 11.0s |
| Multi-No-Validator | 100.0% | 100.0% | 0.00 | 11.8s |
| **HDAFA (Ours)** | **100.0%** | **100.0%** | **0.00** | **10.8s** |

### Key Findings

1. **Pass Rate alone is insufficient.** All systems achieve ~100% on universal
   structural checks — this metric does not capture content completeness.
2. **The Analyzer is the critical component.** Systems with an Analyzer achieve
   **100% section coverage**; systems without it average **85%** (a 15-point gap).
3. **Validator alone does not improve results.** `Single+Validator` performs
   *worse* on pass rate (92.9% vs 100%) without improving coverage.
4. **HDAFA achieves the best combination.** It matches Multi-No-Validator on
   quality while maintaining competitive execution time.
5. **Edge cases expose the largest gap.** On a 12-section page, Single-Agent
   drops to 50% coverage while HDAFA stays at 100%.

---

## 📁 Repository Structure
hdafa/
├── README.md # This file
├── LICENSE # MIT License
├── requirements.txt # Python dependencies
├── .gitignore
│
├── agents/ # The three atomic agents
│ ├── init.py
│ ├── analyzer.py # Agent 1: Requirements → JSON Schema
│ ├── coder.py # Agent 2: Schema → HTML/CSS
│ └── validator.py # Agent 3: Deterministic checks (no AI)
│
├── benchmark/ # Reproducing paper results
│ ├── run_baselines.py # Runs 14 tasks × 4 systems
│ └── analyze_results.py # Produces summary tables + chart
│
├── examples/ # Usage examples
│ ├── sample_task.py # Single-task pipeline demo
│ └── sample_outputs/
│ ├── restaurant.html
│ ├── clothing_store.html
│ └── coffee_shop.html
│
├── results/ # Generated outputs
│ ├── hdafa_baselines_gemini.csv # Raw benchmark results
│ ├── results_summary.csv # Table 5.3 in paper
│ ├── results_by_category.csv # Table 5.4 in paper
│ └── results_chart.png # Figure in paper
│
└── paper/
└── HDAFA_Final_Paper.pdf # Published paper

text

---

## 🚀 Installation

### 1. Clone the repository


git clone https://github.com/MostafaFathi-afrotoh/hdafa.git
cd hdafa
2. Install dependencies
bash
pip install -r requirements.txt
3. Set up your Gemini API key
Get a key from Google AI Studio, then:

bash
export GEMINI_API_KEY="your-key-here"
🧪 Quick Start
Single-task demo
bash
python examples/sample_task.py
This will:

Take a task description (e.g., "صفحة مطعم شرقي مع قائمة وحجز طاولة").

Run the full HDAFA pipeline (Analyzer → Coder → Validator).

Save the generated HTML and a JSON validation report.

Example output
json
{
  "final_verdict": "PASS",
  "score": "10/10",
  "coverage": 100.0,
  "retries": 0,
  "failed": []
}
🔬 Reproducing the Paper Results
Step 1 — Run the full benchmark
bash
cd benchmark
python run_baselines.py
Runtime: ~11 minutes (14 tasks × 4 systems).

Output: results/hdafa_baselines_gemini.csv

Note: Task 15 (صفحة بقبود صارمة (600 سطر)) is skipped if
schema generation fails. This is documented in the paper's Limitations section.

Step 2 — Generate summary tables and chart
bash
python analyze_results.py
Output:

results/results_summary.csv — Table 5.3 in paper

results/results_by_category.csv — Table 5.4 in paper

results/results_chart.png — Figure in paper

Step 3 — Verify against the paper
Compare your generated CSVs with the ones in results/. Both should match
exactly if you use the same model (gemini-3.5-flash-lite) and temperature=0.0.

🧩 Extending HDAFA
Add a new agent
Create agents/your_agent.py.

Export its main function in agents/__init__.py.

Wire it into benchmark/run_baselines.py.

Add new deterministic checks
Edit agents/validator.py::structural_checks() — no LLM call needed.

Add a new task
Append to the TASKS list in benchmark/run_baselines.py:

python
TASKS = [
    ("خدمات", "صفحة مطعم شرقي مع قائمة وحجز طاولة"),
    # ...
    ("فئتك", "وصف المهمة الجديدة"),
]
⚠️ Limitations
Scope: HTML/CSS only. No JavaScript, no backend, no business logic.

Model-dependent: Results are tied to gemini-3.5-flash-lite.

Sample size: 14 tasks; larger-scale evaluation is future work.

Visual quality: Not evaluated. The Validator checks structure and
content presence, not aesthetics.

Coverage bias: Section coverage is measured against a schema generated
by the same Analyzer used in HDAFA — see Section 7.3 of the paper.

🛠️ Tech Stack
Component	Technology
Language	Python 3.11+
LLM	Google Gemini (gemini-3.5-flash-lite)
Validation	Regex + JSON (zero LLM)
Analysis	pandas, matplotlib
Runtime	Google Colab / local Python
📚 Citation
If you use HDAFA in your research, please cite:

bibtex
@misc{youssef2026hdafa,
  title  = {HDAFA: A Hyper-Deterministic Atomic Agentic Architecture
            for Verifiable Code Generation},
  author = {Youssef, Mustafa Fathy AbdelTawab},
  year   = {2026},
  url    = {https://github.com/MostafaFathi-afrotoh/hdafa},
  note   = {Independent Research}
}
🤝 Contributing
Contributions are welcome. To propose changes:

Fork the repository.

Create a feature branch: git checkout -b feature/your-feature.

Commit your changes: git commit -m "Add your feature".

Push and open a Pull Request.

Please ensure your code:

Passes the existing benchmark without regression.

Adds unit tests for new Validator checks.

Updates this README if behavior changes.

📄 License
This project is licensed under the MIT License — see LICENSE for details.

📬 Contact
Author: Mustafa Fathy AbdelTawab Youssef

Email: afracosh12@gmail.com

LinkedIn: mustafa-fathy-abdeltawab

ORCID: 0009-0000-4920-9333

HDAFA is not magic — it is architectural discipline.
Put the probabilistic model inside a deterministic box,
make each agent do one thing, and never let output pass without verification.

markdown
# HDAFA — Hyper-Deterministic Atomic Agentic Architecture

> **A multi-agent system that wraps probabilistic LLM generation inside a deterministic verification shell.**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Paper](https://img.shields.io/badge/Paper-PDF-red.svg)](paper/HDAFA_Final_Paper.pdf)

**Author:** Mustafa Fathy AbdelTawab Youssef
**Email:** afracosh12@gmail.com
**ORCID:** [0009-0000-4920-9333](https://orcid.org/0009-0000-4920-9333)

---

## 📖 Overview

HDAFA is a multi-agent architecture that transforms natural-language descriptions
into **verifiable** HTML/CSS pages through three specialized, atomic agents:
Task → Analyzer → JSON Schema → Coder → HTML → Validator → PASS/FAIL

text

The core hypothesis:

> **Structure + Deterministic Verification = More Reliable Output**

Unlike typical LLM-based code generators, HDAFA separates the **probabilistic**
step (generation) from the **deterministic** step (verification). The Validator
uses zero AI — only algorithmic checks — so its verdicts are reproducible and
auditable.

---

## 🏗️ Architecture

| Agent | Role | Input | Output |
|-------|------|-------|--------|
| **Requirements Analyzer** | Parses natural-language task | Task description | JSON Schema |
| **HTML/CSS Coder** | Generates the web page | JSON Schema | Complete HTML |
| **Deterministic Validator** | Verifies the output | HTML + Schema | PASS/FAIL + coverage |

### Design Principles

1. **Hyper-Atomicity** — Each agent performs exactly one task.
2. **Deterministic Outer Shell** — Verification is algorithmic, not AI-based.
3. **Ephemeral Agents** — No shared state between invocations.
4. **Closed-Loop Verification** — No output passes without validation.
5. **Intelligence Stratification** — Lighter models for atomic tasks.

---

## 📊 Key Results

Evaluated on **14 web generation tasks** across 5 categories
(services, e-commerce, landing pages, personal portfolios, edge cases),
using `gemini-3.5-flash-lite` with `temperature=0.0`.

| System | Pass Rate | Avg Coverage | Avg Retries | Avg Time |
|--------|:---------:|:------------:|:-----------:|:--------:|
| Single-Agent | 100.0% | 85.0% | 0.00 | 9.8s |
| Single+Validator | 92.9% | 84.8% | 0.14 | 11.0s |
| Multi-No-Validator | 100.0% | 100.0% | 0.00 | 11.8s |
| **HDAFA (Ours)** | **100.0%** | **100.0%** | **0.00** | **10.8s** |

### Key Findings

1. **Pass Rate alone is insufficient.** All systems achieve ~100% on universal
   structural checks — this metric does not capture content completeness.
2. **The Analyzer is the critical component.** Systems with an Analyzer achieve
   **100% section coverage**; systems without it average **85%** (a 15-point gap).
3. **Validator alone does not improve results.** `Single+Validator` performs
   *worse* on pass rate (92.9% vs 100%) without improving coverage.
4. **HDAFA achieves the best combination.** It matches Multi-No-Validator on
   quality while maintaining competitive execution time.
5. **Edge cases expose the largest gap.** On a 12-section page, Single-Agent
   drops to 50% coverage while HDAFA stays at 100%.

---

## 📁 Repository Structure
hdafa/
├── README.md # This file
├── LICENSE # MIT License
├── requirements.txt # Python dependencies
├── .gitignore
│
├── agents/ # The three atomic agents
│ ├── init.py
│ ├── analyzer.py # Agent 1: Requirements → JSON Schema
│ ├── coder.py # Agent 2: Schema → HTML/CSS
│ └── validator.py # Agent 3: Deterministic checks (no AI)
│
├── benchmark/ # Reproducing paper results
│ ├── run_baselines.py # Runs 14 tasks × 4 systems
│ └── analyze_results.py # Produces summary tables + chart
│
├── examples/ # Usage examples
│ ├── sample_task.py # Single-task pipeline demo
│ └── sample_outputs/
│ ├── restaurant.html
│ ├── clothing_store.html
│ └── coffee_shop.html
│
├── results/ # Generated outputs
│ ├── hdafa_baselines_gemini.csv # Raw benchmark results
│ ├── results_summary.csv # Table 5.3 in paper
│ ├── results_by_category.csv # Table 5.4 in paper
│ └── results_chart.png # Figure in paper
│
└── paper/
└── HDAFA_Final_Paper.pdf # Published paper

text

---

## 🚀 Installation

### 1. Clone the repository


git clone https://github.com/MostafaFathi-afrotoh/hdafa.git
cd hdafa
2. Install dependencies
bash
pip install -r requirements.txt
3. Set up your Gemini API key
Get a key from Google AI Studio, then:

bash
export GEMINI_API_KEY="your-key-here"
🧪 Quick Start
Single-task demo
bash
python examples/sample_task.py
This will:

Take a task description (e.g., "صفحة مطعم شرقي مع قائمة وحجز طاولة").

Run the full HDAFA pipeline (Analyzer → Coder → Validator).

Save the generated HTML and a JSON validation report.

Example output
json
{
  "final_verdict": "PASS",
  "score": "10/10",
  "coverage": 100.0,
  "retries": 0,
  "failed": []
}
🔬 Reproducing the Paper Results
Step 1 — Run the full benchmark
bash
cd benchmark
python run_baselines.py
Runtime: ~11 minutes (14 tasks × 4 systems).

Output: results/hdafa_baselines_gemini.csv

Note: Task 15 (صفحة بقبود صارمة (600 سطر)) is skipped if
schema generation fails. This is documented in the paper's Limitations section.

Step 2 — Generate summary tables and chart
bash
python analyze_results.py
Output:

results/results_summary.csv — Table 5.3 in paper

results/results_by_category.csv — Table 5.4 in paper

results/results_chart.png — Figure in paper

Step 3 — Verify against the paper
Compare your generated CSVs with the ones in results/. Both should match
exactly if you use the same model (gemini-3.5-flash-lite) and temperature=0.0.

🧩 Extending HDAFA
Add a new agent
Create agents/your_agent.py.

Export its main function in agents/__init__.py.

Wire it into benchmark/run_baselines.py.

Add new deterministic checks
Edit agents/validator.py::structural_checks() — no LLM call needed.

Add a new task
Append to the TASKS list in benchmark/run_baselines.py:

python
TASKS = [
    ("خدمات", "صفحة مطعم شرقي مع قائمة وحجز طاولة"),
    # ...
    ("فئتك", "وصف المهمة الجديدة"),
]
⚠️ Limitations
Scope: HTML/CSS only. No JavaScript, no backend, no business logic.

Model-dependent: Results are tied to gemini-3.5-flash-lite.

Sample size: 14 tasks; larger-scale evaluation is future work.

Visual quality: Not evaluated. The Validator checks structure and
content presence, not aesthetics.

Coverage bias: Section coverage is measured against a schema generated
by the same Analyzer used in HDAFA — see Section 7.3 of the paper.

🛠️ Tech Stack
Component	Technology
Language	Python 3.11+
LLM	Google Gemini (gemini-3.5-flash-lite)
Validation	Regex + JSON (zero LLM)
Analysis	pandas, matplotlib
Runtime	Google Colab / local Python
📚 Citation
If you use HDAFA in your research, please cite:

bibtex
@misc{youssef2026hdafa,
  title  = {HDAFA: A Hyper-Deterministic Atomic Agentic Architecture
            for Verifiable Code Generation},
  author = {Youssef, Mustafa Fathy AbdelTawab},
  year   = {2026},
  url    = {https://github.com/MostafaFathi-afrotoh/hdafa},
  note   = {Independent Research}
}
🤝 Contributing
Contributions are welcome. To propose changes:

Fork the repository.

Create a feature branch: git checkout -b feature/your-feature.

Commit your changes: git commit -m "Add your feature".

Push and open a Pull Request.

Please ensure your code:

Passes the existing benchmark without regression.

Adds unit tests for new Validator checks.

Updates this README if behavior changes.

📄 License
This project is licensed under the MIT License — see LICENSE for details.

📬 Contact
Author: Mustafa Fathy AbdelTawab Youssef

Email: afracosh12@gmail.com

LinkedIn: mustafa-fathy-abdeltawab

ORCID: 0009-0000-4920-9333

HDAFA is not magic — it is architectural discipline.
Put the probabilistic model inside a deterministic box,
make each agent do one thing, and never let output pass without verification.

