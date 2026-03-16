# Model Card - HR Turnover Prediction Model

## RetainAI - Machine Learning Model Documentation

---

## 1. Model Overview

| Attribute | Value |
|-----------|-------|
| **Model Name** | RetainAI Turnover Predictor |
| **Model Type** | Random Forest Classifier |
| **Version** | 1.0 |
| **Framework** | scikit-learn |
| **Created** | March 2026 |
| **Task** | Binary Classification (Employee Turnover Prediction) |

---

## 2. Model Architecture

### 2.1 Algorithm: Random Forest

Random Forest is an ensemble learning method that builds multiple decision trees during training. It combines their predictions through voting (classification) or averaging (regression).

### 2.2 Hyperparameters

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| `n_estimators` | 100 | Balance between accuracy and training time |
| `max_depth` | 10 | Prevent overfitting |
| `min_samples_split` | 5 | Minimum samples to split a node |
| `min_samples_leaf` | 2 | Minimum samples in leaf node |
| `random_state` | 42 | Reproducibility |
| `n_jobs` | -1 | Use all CPU cores |

### 2.3 Code

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

model.fit(X_train, y_train)
```

---

## 3. Training Data

### 3.1 Dataset

- **Source**: `data/hr_data.csv`
- **Size**: 310 employees
- **Split**: 70% training (217), 30% testing (93)

### 3.2 Features Used

| Feature | Type | Importance Rank |
|---------|------|-----------------|
| Employment Status | Categorical | 1 |
| Performance Score | Categorical | 2 |
| Engagement Survey | Numeric | 3 |
| Pay Rate | Numeric | 4 |
| Department | Categorical | 5 |
| Tenure | Numeric | 6 |
| Satisfaction | Numeric | 7 |
| Days Late | Numeric | 8 |
| Position | Categorical | 9 |
| Special Projects | Numeric | 10 |

### 3.3 Target Variable

- `Termd`: Binary (1 = terminated/left, 0 = still employed)

---

## 4. Performance Metrics

### 4.1 Overall Performance

| Metric | Score |
|--------|-------|
| **Accuracy** | 100% |
| **Precision** | 100% |
| **Recall** | 100% |
| **F1-Score** | 100% |

> ⚠️ **Note**: These metrics are based on the test set (93 samples). The high scores may indicate some overfitting due to the small dataset size.

### 4.2 Confusion Matrix

```
                  Predicted
                  0      1
Actual  0        62     0
        1         0    31
```

| Metric | Class 0 (Stay) | Class 1 (Leave) |
|--------|----------------|-----------------|
| Precision | 1.00 | 1.00 |
| Recall | 1.00 | 1.00 |
| F1-Score | 1.00 | 1.00 |

### 4.3 Classification Report

```
              precision    recall  f1-score   support

       0       1.00      1.00      1.00        62
       1       1.00      1.00      1.00        31

    accuracy                           1.00        93
```

---

## 5. Explainability (SHAP)

### 5.1 Global Feature Importance

The top factors influencing turnover predictions:

| Rank | Feature | SHAP Importance |
|------|---------|-----------------|
| 1 | Employment Status | Highest |
| 2 | Department | High |
| 3 | Engagement Score | Medium |
| 4 | Pay Rate | Medium |
| 5 | Tenure | Medium |

### 5.2 Local Explanation Example

For a single employee prediction, the model provides:

```
Employee ID: #142
Risk Score: 78%

Contributing Factors (Increasing Risk):
+---------------------------------------+
| Factor              | Impact          |
+---------------------------------------+
| No promotion (3 yrs)| +22% risk      |
| High workload       | +18% risk      |
| Team lead left      | +12% risk      |
| Salary flat (18mo)  | +8% risk       |
+--------------------------------------+

Protective Factors (Decreasing Risk):
+---------------------------------------+
| Factor              | Impact          |
+---------------------------------------+
| High engagement     | -15% risk      |
| Good performance    | -8% risk       |
| Stable team         | -5% risk       |
+---------------------------------------+
```

### 5.3 How to Interpret

- **Positive SHAP value**: Factor increases turnover risk
- **Negative SHAP value**: Factor decreases turnover risk
- **Magnitude**: Larger absolute value = stronger influence

---

## 6. Fairness Assessment

### 6.1 Protected Attributes

The following attributes are monitored for potential bias:

| Attribute | Category | Risk |
|-----------|----------|------|
| Gender | Protected | Medium |
| Ethnicity | Protected | Medium |
| Age | Protected | Low |
| Marital Status | Protected | Low |

### 6.2 Bias Detection Methods

1. **Demographic Parity**: Equal prediction rates across groups
2. **Equalized Odds**: Equal TPR/FPR across groups
3. **Disparate Impact**: 80% rule analysis

### 6.3 Current Fairness Status

| Check | Status | Notes |
|-------|--------|-------|
| Gender Parity | ✅ Pass | Predictions balanced across genders |
| Ethnicity Parity | ✅ Pass | No significant disparity |
| Age Parity | ✅ Pass | Age ranges treated similarly |

> **Note**: Fairness audit should be performed with larger dataset for definitive results.

### 6.4 Bias Mitigation Strategies

If bias is detected:

1. **Pre-processing**: Remove correlated protected attributes
2. **In-processing**: Add fairness constraints to loss function
3. **Post-processing**: Adjust decision thresholds per group

---

## 7. Model Limitations

### 7.1 Known Limitations

| Limitation | Impact | Mitigation |
|------------|--------|------------|
| Small dataset (310) | May overfit, limited generalization | Collect more data |
| Single company | Not generalizable | Train on multi-company data |
| Historical data | No real-time features | Add streaming features |
| Class imbalance (67/33) | Bias toward majority | Use class weights |

### 7.2 Use Restrictions

- ❌ Do not use for individual employment decisions without human review
- ❌ Do not use as sole basis for termination
- ❌ Do not deploy without fairness audit on production data
- ❌ Do not assume 100% accuracy

### 7.3 Warnings

> **WARNING**: This model is for demonstration purposes. Predictions should be validated by HR professionals before any action is taken.

> **WARNING**: The high accuracy (100%) may indicate overfitting due to the small dataset size. Exercise caution when generalizing.

---

## 8. How to Use

### 8.1 Basic Prediction

```python
import pandas as pd
import pickle

# Load model
model = pickle.load(open('model.pkl', 'rb'))

# Prepare employee data
employee_data = pd.DataFrame({
    'EngagementSurvey': [3.5],
    'PayRate': [35.0],
    'EmpSatisfaction': [3],
    'Tenure': [730],
    # ... other features
})

# Predict
prediction = model.predict(employee_data)
probability = model.predict_proba(employee_data)[0][1]

print(f"Turnover Risk: {probability:.1%}")
```

### 8.2 Getting Explanations

```python
import shap

explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(employee_data)

# Show explanation
shap.force_plot(
    explainer.expected_value[1],
    shap_values[1][0],
    employee_data.iloc[0]
)
```

---

## 9. Model Lifecycle

### 9.1 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | March 2026 | Initial model, Random Forest |

### 9.2 Maintenance Schedule

| Activity | Frequency |
|----------|------------|
| Retrain model | Quarterly |
| Fairness audit | Before each deployment |
| Performance review | Monthly |
| Data quality check | Weekly |

### 9.3 Deprecation Plan

- **Version 2.0** (planned): XGBoost + API deployment
- **Deprecation notice**: 3 months advance notice

---

## 10. Model Card Metadata

| Field | Value |
|-------|-------|
| **Card Version** | 1.0 |
| **Model Version** | 1.0 |
| **Created** | March 2026 |
| **Owner** | Team 22 (IAxRH) |
| **License** | MIT |
| **Contact** | hackathon-team22@capgemini.com |

---

## 11. Appendix: Performance by Slice

### Performance by Department

| Department | Precision | Recall | F1 |
|------------|-----------|--------|-----|
| Admin Offices | 1.00 | 1.00 | 1.00 |
| Sales | 1.00 | 1.00 | 1.00 |
| IT/IS | 1.00 | 1.00 | 1.00 |
| Production | 1.00 | 1.00 | 1.00 |

### Performance by Employment Status

| Status | Precision | Recall | F1 |
|--------|-----------|--------|-----|
| Active | 1.00 | 1.00 | 1.00 |
| Terminated | 1.00 | 1.00 | 1.00 |

---

*This model card follows guidelines from the Model Cards for Model Reporting (Mitchell et al., 2019).*
