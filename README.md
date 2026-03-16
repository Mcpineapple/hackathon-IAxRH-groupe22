# RetainAI - HR Turnover Prediction with Explainable AI

> **Trusted AI Solution for Human Resources**
> 
> *Capgemini x ESILV AI Cyber Hackathon - 2026*

---

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Theme: XAI + Privacy](https://img.shields.io/badge/Theme-XAI%20%2B%20Privacy-blue)](https://hackathon.capgemini.com)

---

## Project Overview

**RetainAI** is an explainable AI solution that helps HR departments identify employees at risk of leaving—while providing transparent, human-understandable reasons for every prediction.

### The Problem

- **25% of employees leave annually** — often without warning
- Traditional HR tools provide risk scores without explanations ("black box")
- Employee data is sensitive; privacy regulations (GDPR) must be respected
- AI can inherit historical biases, perpetuating unfair treatment

### Our Solution

RetainAI combines **machine learning** with **explainability (SHAP)**, **privacy-by-design**, and **fairness auditing** to deliver predictions HR can trust—and employees can feel protected by.

---

## Objectives

| Objective | Description |
|-----------|-------------|
| **Predict Turnover** | Identify employees at risk of resignation with high accuracy |
| **Explain Predictions** | Provide human-understandable reasons (not just numbers) |
| **Protect Privacy** | Implement GDPR-compliant data handling from the ground up |
| **Ensure Fairness** | Audit model for demographic bias before deployment |

---

## Scope

### What's Included

- **ML Model**: Random Forest classifier trained on HR data
- **XAI Integration**: SHAP values for feature-level explanations
- **Privacy Layer**: Anonymization and data encryption protocols
- **Fairness Check**: Bias detection across protected attributes
- **Demo Notebook**: Interactive Jupyter notebook with full workflow

### What's Not Included

- Production deployment infrastructure
- Real-time API integration with HR systems
- User-facing dashboard (notebook demo only)
- Longitudinal prediction (single-timepoint only)

---

## Target Persona

### Primary: HR Directors & People Analytics Teams

**Who they are:**
- Mid-to-senior level HR professionals
- Familiar with basic metrics but not ML/AI
- Responsible for retention strategies and workforce planning

**Their pain points:**
- Cannot explain why an employee might leave
- Worried about data privacy and legal compliance
- Skeptical of "black box" AI recommendations

**How we help:**
- Plain-language explanations: *"No promotion in 3 years + overtime hours = elevated risk"*
- Built-in privacy badges reassure employees
- Fairness verification proves equitable treatment

---

## Quick Start

### Prerequisites

- Python 3.9+
- Jupyter Notebook or JupyterLab
- 4GB RAM minimum

### Installation

```bash
# Clone the repository
git clone https://github.com/your-org/hackathon-IAxRH-groupe22.git
cd hackathon-IAxRH-groupe22

# Install dependencies
pip install pandas numpy scikit-learn shap lime matplotlib seaborn jupyter
```

### Running the Demo

```bash
# Launch Jupyter
jupyter notebook hr_turnover_prediction.ipynb
```

The notebook contains:
1. Data loading and preprocessing
2. Model training and evaluation
3. SHAP explanations for individual predictions
4. Fairness auditing
5. Visualization of results

---

## Project Structure

```
hackathon-IAxRH-groupe22/
├── README.md                 # This file
├── hr_turnover_prediction.ipynb  # Main demo notebook
├── PITCH_STORY.md            # Pitch narrative for presentation
├── docs/
│   ├── technical_docs.md     # Technical implementation details
│   ├── architecture.md        # System architecture with diagram
│   ├── data_card.md          # Dataset documentation
│   └── model_card.md         # Model performance & usage
├── executive_summary.md      # Business-focused summary
├── slides/                   # Presentation slides (placeholder)
├── data/
│   ├── hr_data.csv          # HR dataset
│   └── hr_text_data.csv     # Text data (if applicable)
└── outputs/
    └── shap_importance.png   # Feature importance visualization
```

---

## Key Features

### 1. Explainable Predictions (SHAP)

Every prediction includes:
- **Feature contribution**: Which factors contributed most?
- **Direction**: Is this factor increasing or decreasing risk?
- **Human-readable**: No technical jargon—clear action items

### 2. Privacy by Design

- Data anonymization (names → tokens)
- No PII stored in model training
- GDPR-compliant data handling
- Employee consent awareness

### 3. Fairness Auditing

- Bias detection across gender, age, ethnicity
- Model comparison for disparate impact
- Regular fairness reports

---

## Model Performance

| Metric | Score |
|--------|-------|
| Accuracy | ~85% |
| Precision | ~80% |
| Recall | ~78% |
| F1-Score | ~79% |

*Full metrics in [model_card.md](docs/model_card.md)*

---

## Documentation

| Document | Purpose |
|----------|---------|
| [Technical Docs](docs/technical_docs.md) | Implementation details, code structure |
| [Architecture](docs/architecture.md) | System design, data flow, security |
| [Data Card](docs/data_card.md) | Dataset source, processing, limitations |
| [Model Card](docs/model_card.md) | Model type, metrics, interpretation guide |
| [Executive Summary](executive_summary.md) | Business case, impact, key benefits |

---

## Presentation

Slides are available in the `slides/` directory. The presentation covers:
- Problem statement
- Solution overview
- Demo walkthrough
- Impact and benefits

---

## License

MIT © 2026 Capgemini x ESILV Hackathon Team 22

---

## Contact

For questions about this project:
- **Team**: Group 22 (IAxRH)
- **Theme**: Cybersecurity + Explainable AI
- **Hackathon**: Capgemini x ESILV 2026
