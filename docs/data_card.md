# Data Card - HR Turnover Dataset

## RetainAI - Dataset Documentation

---

## 1. Dataset Overview

| Attribute | Value |
|-----------|-------|
| **Name** | HR Employee Data |
| **Source** | Internal HR records (simulated) |
| **Format** | CSV |
| **Size** | 310 employees, 35 features |
| **Version** | 1.0 |
| **Last Updated** | 2024 |

---

## 2. Data Schema

### 2.1 Identifiers

| Column | Type | Description | PII |
|--------|------|-------------|-----|
| `Employee_Name` | String | Full name | ✅ Yes |
| `EmpID` | Integer | Employee ID | ✅ Yes |
| `EmpStatusID` | Integer | Employment status code | No |

### 2.2 Demographics

| Column | Type | Description | PII |
|--------|------|-------------|-----|
| `MarriedID` | Binary | Married flag (1/0) | No |
| `MaritalStatusID` | Integer | Marital status code | No |
| `MaritalDesc` | String | Marital status text | No |
| `GenderID` | Binary | Gender (0/1) | No |
| `Sex` | String | Gender text (M/F) | No |
| `DOB` | Date | Date of birth | ✅ Yes |
| `HispanicLatino` | String | Ethnicity indicator | No |
| `RaceDesc` | String | Race/ethnicity | No |
| `CitizenDesc` | String | Citizenship status | No |

### 2.3 Employment

| Column | Type | Description |
|--------|------|-------------|
| `Department` | String | Department name |
| `Position` | String | Job title |
| `PositionID` | Integer | Position code |
| `ManagerName` | String | Direct manager |
| `ManagerID` | Integer | Manager ID |
| `PayRate` | Float | Hourly pay rate |
| `EmploymentStatus` | String | Active/Terminated |
| `DateofHire` | Date | Start date |
| `DateofTermination` | Date | End date (if applicable) |
| `TermReason` | String | Reason for leaving |
| `Termd` | Binary | **Target variable** (1=left, 0=active) |
| `RecruitmentSource` | String | Source of hire |

### 2.4 Performance

| Column | Type | Description |
|--------|------|-------------|
| `PerfScoreID` | Integer | Performance score code |
| `PerformanceScore` | String | Performance rating text |
| `EmpSatisfaction` | Integer | Satisfaction (1-5) |
| `EngagementSurvey` | Float | Engagement score |
| `SpecialProjectsCount` | Integer | Number of special projects |
| `DaysLateLast30` | Integer | Lateness indicator |

### 2.5 Location

| Column | Type | Description |
|--------|------|-------------|
| `State` | String | Work state |
| `Zip` | Integer | ZIP code |

---

## 3. Target Variable

### Definition: `Termd` (Termination)

| Value | Meaning | Count |
|-------|---------|-------|
| 0 | Still employed | 207 |
| 1 | Terminated/Left | 103 |
| **Total** | | **310** |

### Class Distribution

```
Employed (0):  ████████████████████ 66.8%
Terminated (1): ████████████ 33.2%
```

⚠️ **Note**: The dataset is slightly imbalanced with more active employees than terminated.

---

## 4. Data Collection

### 4.1 Source System

- Primary: HRIS (Human Resources Information System)
- Format: Manual export to CSV

### 4.2 Collection Period

- Hire dates: 2008 - 2019
- Termination dates: 2010 - 2019
- Data snapshot: January 2019

### 4.3 Consent & Ethics

- **Status**: Synthetic/simulated data
- **Note**: For hackathon demonstration purposes
- **Real-world requirement**: Employee consent required for production use

---

## 5. Data Processing

### 5.1 Preprocessing Steps

```
┌──────────────────┐
│   Raw CSV Load   │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│   Remove PII     │  ← Employee_Name, EmpID
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│   Handle Nulls   │  ← Fill or drop
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│   Date Parsing   │  ← DOB, Hire/ Termination dates
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│   Feature Eng.  │  ← Tenure, salary bands
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│   Encoding       │  ← LabelEncoder for categories
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│   Train/Test    │  ← 70/30 split
└──────────────────┘
```

### 5.2 Feature Engineering

| Feature | Source | Description |
|---------|--------|-------------|
| `tenure_days` | DateofHire | Days since hire |
| `salary_band` | PayRate | Binned salary range |
| `overtime_indicator` | DaysLateLast30 | High overtime flag |
| `promotion_needed` | PerfScoreID + Tenure | Promotion indicator |

---

## 6. Privacy Measures

### 6.1 PII Handling

| PII Type | Action |
|----------|--------|
| Names | Removed (tokenized) |
| Employee IDs | Removed |
| Dates of Birth | Age banding applied |
| Addresses (ZIP) | Only state retained |
| Manager Names | Anonymized |

### 6.2 GDPR Compliance

| Requirement | Implementation |
|-------------|----------------|
| **Purpose Limitation** | Data used only for turnover prediction |
| **Data Minimization** | Only relevant features used in model |
| **Storage Limitation** | Training data discarded after model fit |
| **Anonymization** | Direct identifiers removed |

### 6.3 Security

- **Storage**: Local file system (demo)
- **Access**: Jupyter notebook only
- **Transmission**: Not applicable (local processing)

---

## 7. Data Quality

### 7.1 Completeness

| Metric | Value |
|--------|-------|
| Total Rows | 310 |
| Missing Values | < 5% |
| Duplicate Rows | 0 |

### 7.2 Validity

| Check | Status |
|-------|--------|
| Valid dates | ✅ Pass |
| Valid categories | ✅ Pass |
| Numeric ranges | ✅ Pass |
| Consistency | ✅ Pass |

### 7.3 Known Issues

| Issue | Impact | Mitigation |
|-------|--------|------------|
| Class imbalance | Model bias toward majority class | Consider SMOTE or class weights |
| Single company | Limited generalization | Need multi-company data |
| Historical data only | No real-time features | Future: API integration |

---

## 8. Usage Restrictions

### 8.1 Intended Use

- ✅ HR turnover analysis
- ✅ Predictive modeling
- ✅ Explainable AI research
- ✅ Fairness auditing

### 8.2 Not Approved For

- ❌ Real employment decisions (without human oversight)
- ❌ Discriminatory purposes
- ❌ Individual-level hiring/firing decisions
- ❌ Sale or distribution to third parties

### 8.3 Disclaimer

> This dataset is for demonstration and research purposes only. It contains simulated data and should not be used for actual HR decisions without proper validation and legal review.

---

## 9. Access & Reproduction

### 9.1 Data Location

```
/data/hr_data.csv
```

### 9.2 Loading the Data

```python
import pandas as pd

df = pd.read_csv('data/hr_data.csv')
print(f"Shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")
```

### 9.3 Reproducibility

- Random seed: 42
- Train/test split: 70/30
- Model random state: 42

---

## 10. Data Card Metadata

| Field | Value |
|-------|-------|
| **Card Version** | 1.0 |
| **Created** | March 2026 |
| **Last Updated** | March 2026 |
| **Owner** | Team 22 (IAxRH) |
| **Contact** | hackathon-team22@capgemini.com |
| **License** | MIT |

---

## 11. Appendix: Feature Summary

| Category | Count |
|----------|-------|
| Identifiers | 2 |
| Demographics | 9 |
| Employment | 11 |
| Performance | 6 |
| Location | 2 |
| **Total Features** | **35** |

---

*This data card follows the format recommended by the Data Cards Playbook (MIT Media Lab).*
