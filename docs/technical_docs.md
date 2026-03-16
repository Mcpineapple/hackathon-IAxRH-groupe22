# Technical Documentation

## RetainAI - HR Turnover Prediction System

---

## 1. System Overview

RetainAI is an explainable AI (XAI) system designed for HR turnover prediction. It combines machine learning with SHAP (SHapley Additive exPlanations) to provide transparent, actionable insights while maintaining strict privacy and fairness standards.

### Core Technologies

| Component | Technology | Version |
|-----------|------------|---------|
| Language | Python | 3.9+ |
| ML Framework | scikit-learn | 1.3+ |
| XAI Library | SHAP | 0.42+ |
| Data Processing | pandas, numpy | Latest |
| Visualization | matplotlib, seaborn | Latest |

---

## 2. Data Pipeline

### 2.1 Data Sources

- **Primary**: `data/hr_data.csv` (310 employees, 35 features)
- **Features include**: demographics, employment history, performance metrics, engagement scores

### 2.2 Data Processing Steps

```
Raw Data → Cleaning → Feature Engineering → Encoding → Model Training
```

1. **Data Cleaning**
   - Handle missing values
   - Remove duplicate records
   - Standardize date formats

2. **Feature Engineering**
   - Tenure calculation (days since hire)
   - Salary banding
   - Performance score categorization
   - Overtime indicator

3. **Encoding**
   - Label encoding for categorical variables
   - One-hot encoding for department/position
   - Binary encoding for yes/no features

### 2.3 Target Variable

- `Termd`: Binary (1 = terminated/left, 0 = still employed)
- Derived from employment status and termination date

---

## 3. Model Architecture

### 3.1 Algorithm: Random Forest Classifier

```python
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)
```

### 3.2 Why Random Forest?

- **Interpretability**: Feature importance built-in
- **Robustness**: Handles missing data, outliers well
- **No scaling required**: Works with mixed feature types
- **XAI compatibility**: SHAP values computed easily

### 3.3 Hyperparameters

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| n_estimators | 100 | Balance accuracy vs. training time |
| max_depth | 10 | Prevent overfitting |
| min_samples_split | 5 | Minimum samples to split node |
| min_samples_leaf | 2 | Minimum samples in leaf |
| random_state | 42 | Reproducibility |

---

## 4. Explainable AI (XAI) Implementation

### 4.1 SHAP Integration

```python
import shap

# Create SHAP explainer
explainer = shap.TreeExplainer(model)

# Compute SHAP values
shap_values = explainer.shap_values(X_test)

# For a single prediction
shap.force_plot(
    explainer.expected_value[1],
    shap_values[1][0],
    X_test.iloc[0]
)
```

### 4.2 Explanation Types

1. **Global Feature Importance**
   - Mean absolute SHAP values across all predictions
   - Identifies top factors influencing turnover

2. **Local Explanation (Per-Employee)**
   - Individual prediction breakdown
   - "Why this employee is at risk"

3. **Feature Direction**
   - Positive contribution = increases risk
   - Negative contribution = decreases risk

### 4.3 Example Output

```
Employee: Sarah M.
Risk Score: 78%

Top Risk Factors:
- No promotion in 32 months (+15% risk)
- Workload increased 40% (+12% risk)
- Team lead departed (+8% risk)
- Salary unchanged 18 months (+6% risk)

Protective Factors:
- High engagement score (-10% risk)
- Good performance rating (-5% risk)
```

---

## 5. Privacy Implementation

### 5.1 Data Anonymization

```python
# Before model training
df_anonymized = df.copy()

# Remove PII
df_anonymized.drop(columns=['Employee_Name', 'EmpID', 'SSN'], inplace=True)

# Replace with tokens
df_anonymized['Employee_Token'] = range(len(df))
```

### 5.2 Privacy Measures

| Measure | Implementation |
|---------|----------------|
| PII Removal | Names, IDs removed before training |
| Data Minimization | Only relevant features used |
| Access Control | Training data stored separately |
| Encryption | Sensitive fields encrypted at rest |

### 5.3 GDPR Compliance

- **Purpose limitation**: Data used only for turnover prediction
- **Storage limitation**: Data retention policy enforced
- **Consent awareness**: Employee notification recommended
- **Right to explanation**: SHAP provides interpretable output

---

## 6. Fairness Auditing

### 6.1 Protected Attributes

- Gender
- Age
- Ethnicity
- Marital status
- Disability status

### 6.2 Bias Detection Methods

1. **Demographic Parity**: Equal prediction rates across groups
2. **Equalized Odds**: Equal true/false positive rates
3. **Disparate Impact**: 80% rule analysis

### 6.3 Bias Mitigation

```python
# Example: Check gender bias
from sklearn.metrics import confusion_matrix

# Compare predictions by gender
male_predictions = model.predict(X_test[male_mask])
female_predictions = model.predict(X_test[female_mask])

# Calculate disparate impact
male_positive_rate = sum(male_predictions) / len(male_predictions)
female_positive_rate = sum(female_predictions) / len(female_predictions)

disparate_impact = female_positive_rate / male_positive_rate
# If < 0.8, flag for review
```

---

## 7. Code Structure

### 7.1 Main Notebook Sections

1. **Setup & Dependencies** - Package installation
2. **Data Loading & Exploration** - Initial analysis
3. **Data Preprocessing** - Cleaning and feature engineering
4. **Model Training** - Random Forest training
5. **Model Evaluation** - Metrics and confusion matrix
6. **SHAP Explanations** - Global and local explainability
7. **Fairness Audit** - Bias detection
8. **Visualization** - Charts and dashboards

### 7.2 Key Functions

```python
def preprocess_data(df):
    """Clean and prepare data for modeling."""
    pass

def train_model(X_train, y_train):
    """Train Random Forest classifier."""
    pass

def explain_prediction(model, employee_data, explainer):
    """Generate SHAP explanation for single employee."""
    pass

def check_fairness(model, X_test, y_test, protected_attr):
    """Audit model for demographic bias."""
    pass
```

---

## 8. Evaluation Metrics

### 8.1 Classification Metrics

| Metric | Formula | Interpretation |
|--------|---------|----------------|
| Accuracy | (TP + TN) / Total | Overall correctness |
| Precision | TP / (TP + FP) | Of predicted positives, how many are correct |
| Recall | TP / (TP + FN) | Of actual positives, how many caught |
| F1-Score | 2 × (Precision × Recall) / (Precision + Recall) | Harmonic mean of precision/recall |

### 8.2 Results

```
Classification Report:
              precision    recall  f1-score   support

       0       1.00      1.00      1.00        62
       1       1.00      1.00      1.00        31

    accuracy                           1.00        93
```

---

## 9. Limitations & Future Work

### 9.1 Current Limitations

- **Single-timepoint prediction**: No longitudinal analysis
- **Small dataset**: 310 employees limits generalization
- **Class imbalance**: More non-terminated employees
- **No real-time data**: Static dataset only

### 9.2 Future Enhancements

- [ ] API deployment for real-time predictions
- [ ] Longitudinal tracking (time-series)
- [ ] Integration with HRIS systems (Workday, SAP)
- [ ] Automated fairness reporting dashboard
- [ ] Employee self-service portal
- [ ] A/B testing framework

---

## 10. References

- [SHAP Documentation](https://shap.readthedocs.io/)
- [scikit-learn Random Forest](https://scikit-learn.org/stable/modules/ensemble.html#random-forests)
- [AI Fairness 360](https://aif360.res.ibm.com/) - IBM fairness toolkit
- [GDPR Text](https://gdpr.eu/) - Official GDPR regulations

---

*Last updated: March 2026*
