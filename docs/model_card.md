# Model Card — RetainAI Turnover Predictor

> **Version:** 1.0 | **Framework:** scikit-learn | **Created:** March 2026 | **Owner:** Team 22 (IAxRH)

---

## 1. Model Objective

**Use case:** Binary classification of employee turnover risk — predicting whether an employee is likely to leave or stay within an organization, to support HR retention strategies.

**Inputs:** Tabular employee data including the following features:

| Feature | Type |
|---|---|
| Employment Status | Categorical |
| Performance Score | Categorical |
| Engagement Survey | Numeric |
| Pay Rate | Numeric |
| Department | Categorical |
| Tenure (days) | Numeric |
| Employee Satisfaction | Numeric |
| Days Late Last 30 | Numeric |
| Position | Categorical |
| Special Projects Count | Numeric |

**Outputs:** Binary prediction (`0` = employee likely to stay, `1` = employee likely to leave) along with a probability score (turnover risk %, e.g. `78%`), and a SHAP-based explanation of contributing factors.

---

## 2. Training Data

**Dataset used:** Internal HR dataset — `data/hr_data.csv` (single company, not publicly available)

**Size & diversity:**

- Total samples: **310 employees**
- Train / test split: **70% training (217 samples) / 30% testing (93 samples)**
- Class distribution: approximately **67% stayed (Class 0) / 33% left (Class 1)**
- Diversity: data covers multiple departments (Admin Offices, Sales, IT/IS, Production) and various employment statuses, pay rates, and tenure lengths

**Known limitations:**

- The dataset comes from a **single company**, limiting representativeness across industries or organizational cultures
- The dataset is **small (310 samples)**, which reduces statistical reliability of fairness audits and performance estimates
- **Class imbalance** (67/33 split) may introduce a bias toward predicting the majority class (stay)
- No demographic breakdown of the training population is available to assess representation across age, gender, or ethnicity subgroups

---

## 3. Performance

**Metrics used:** Accuracy, Precision, Recall, F1-Score (per class and overall)

**Global results (test set, n=93):**

| Metric | Score |
|---|---|
| Accuracy | 100% |
| Precision | 100% |
| Recall | 100% |
| F1-Score | 100% |

>  **Important:** A 100% score across all metrics on a 93-sample test set is a strong indicator of **overfitting**. These results should not be interpreted as reflecting real-world generalization capability.

**Results by subgroup:**

| Subgroup | Precision | Recall | F1 |
|---|---|---|---|
| Class 0 — Stay | 1.00 | 1.00 | 1.00 |
| Class 1 — Leave | 1.00 | 1.00 | 1.00 |
| Admin Offices | 1.00 | 1.00 | 1.00 |
| Sales | 1.00 | 1.00 | 1.00 |
| IT/IS | 1.00 | 1.00 | 1.00 |
| Production | 1.00 | 1.00 | 1.00 |

**Confusion matrix (test set):**

```
                  Predicted Stay   Predicted Leave
Actual Stay             62               0
Actual Leave             0              31
```

---

## 4. Limitations

**Known error risks:**

- The model was trained and evaluated on a single, small dataset; performance on unseen companies or industries is unknown
- Perfect test-set accuracy strongly suggests the model has **memorized training patterns** rather than learning generalizable signals
- The model does not incorporate **real-time or dynamic features** (e.g., recent manager change, current project load), which limits its ability to reflect evolving situations

**Out-of-distribution situations not covered:**

- Employees from industries, company sizes, or cultural contexts not present in the training data
- Extreme or rare cases (e.g., sudden layoffs, company restructuring, health-related departures)
- New employees with insufficient historical data (short tenure)

**Bias risks:**

- **Gender, ethnicity, age, and marital status** are identified as protected attributes and monitored, but the fairness audit is based on the same small dataset and its conclusions are therefore **not statistically robust**
- Class imbalance (67% / 33%) may cause the model to underperform on the minority class (leavers) in real-world conditions where data is noisier
- The top feature (Employment Status) may act as a **proxy variable** that indirectly encodes protected attributes

---

## 5. Risks & Mitigation

**Misuse risks:**

| Risk | Description |
|---|---|
| Over-interpretation | Treating a probability score as a definitive decision rather than a signal for further investigation |
| Out-of-scope use | Applying the model to employment termination, hiring, or promotion decisions |
| Automation bias | HR professionals deferring entirely to model output without independent judgment |
| Discriminatory outcomes | Acting on predictions correlated with protected attributes (gender, ethnicity, age) |

**Controls in place:**

-  **Mandatory human review:** All predictions must be reviewed by an HR professional before any action is taken
-  **SHAP explanations:** Every prediction is accompanied by a local explanation to support interpretability and challenge unjustified outcomes
-  **Fairness monitoring:** Demographic parity, equalized odds, and disparate impact (80% rule) are assessed across gender, ethnicity, age, and marital status
-  **Warning messages:** The model surfaces explicit warnings against use as a sole basis for employment decisions
-  **Bias mitigation strategies defined:** Pre-processing (remove correlated protected attributes), in-processing (fairness constraints), and post-processing (threshold adjustment per group) are documented for use if bias is detected
-  **Quarterly retraining** and monthly performance reviews are scheduled to detect drift

---

## 6. Energy & Frugality

| Indicator | Value |
|---|---|
| Model type | Random Forest (100 trees, max depth 10) |
| Model size | Not measured — estimated **< 10 MB** for a scikit-learn Random Forest at this scale |
| Inference time | Not benchmarked — expected **< 100 ms on CPU** for a single prediction given model size |
| Training energy (CodeCarbon) | Not measured — **to be instrumented** in future versions using [CodeCarbon](https://codecarbon.io/) |
| Estimated CO₂ impact | Not available — dataset size and training time suggest **negligible footprint** compared to deep learning models |

> **Note:** Energy and carbon measurements should be added in version 2.0 using CodeCarbon or a comparable tool. Given the small dataset and shallow tree-based architecture, the environmental footprint is expected to be minimal.

---

## 7. Cybersecurity

**Input validation:**

- Input features should be **validated for type, range, and completeness** before being passed to the model (e.g., numeric fields must be within plausible HR ranges; categorical fields must belong to known categories)
- Malformed or unexpected inputs (null values, out-of-range figures, injected strings in categorical fields) must be caught and rejected at the API or preprocessing layer
- The model does not process free-text inputs, which **eliminates prompt injection risk** for this version — however, if natural language interfaces are added in future versions, anti-injection controls must be implemented

**Secret management:**

- No API keys or credentials are required by the core model (`pickle`-based inference)
- Any future deployment (REST API, cloud endpoint) must store credentials exclusively in **environment variables or a secrets manager** — never hardcoded in source files or committed to version control (Git)
- The model artifact (`model.pkl`) should be treated as a **sensitive file**: access should be restricted, and the file should not be publicly exposed

---
