# Architecture Documentation

## RetainAI - System Architecture

---

## 1. High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           RETAINAI SYSTEM                                   │
│                    Explainable HR Turnover Prediction                       │
└─────────────────────────────────────────────────────────────────────────────┘

                           ┌─────────────────┐
                           │   USER LAYER    │
                           │                 │
                           │  HR Director    │
                           │  Analytics Team │
                           └────────┬────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        PRESENTATION LAYER                                   │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    Jupyter Notebook Demo                              │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │   │
│  │  │  Dashboard  │  │  Prediction │  │ Explanation │  │ Fairness   │   │   │
│  │  │   View      │  │    Panel    │  │    Panel    │  │   Report   │   │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘   │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
└────────────────────────────────┬────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        PROCESSING LAYER                                     │
│                                                                              │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────────────┐  │
│  │  PREPROCESSING  │───▶│     MODEL       │───▶│       XAI ENGINE        │  │
│  │                 │    │                 │    │                         │  │
│  │  - Data Clean   │    │  Random Forest  │    │  SHAP Explainer         │  │
│  │  - Encoding     │    │  Classifier     │    │  - Global Importance    │  │
│  │  - Anonymization│   │                 │    │  - Local Explanations   │  │
│  │  - Feature Eng  │    │  n_estimators=100│   │  - Feature Directions   │  │
│  └─────────────────┘    └─────────────────┘    └─────────────────────────┘  │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    FAIRNESS AUDIT LAYER                               │   │
│  │                                                                       │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                │   │
│  │  │   Gender    │  │    Ethnic   │  │   Other     │                │   │
│  │  │   Bias      │  │    Bias     │  │   Bias      │                │   │
│  │  │  Detection  │  │  Detection  │  │  Detection  │                │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘                │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
└────────────────────────────────┬────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          DATA LAYER                                          │
│                                                                              │
│  ┌─────────────────────┐              ┌─────────────────────┐               │
│  │    RAW DATA         │              │   PROCESSED DATA    │               │
│  │                     │              │                      │               │
│  │  hr_data.csv        │──────▶│      │  Anonymized Features │               │
│  │  (Names, IDs,       │   Clean    │  (No PII)             │               │
│  │   sensitive info)   │             │                       │               │
│  └─────────────────────┘              └─────────────────────┘               │
│                                                                              │
└────────────────────────────────┬────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                       SECURITY & PRIVACY LAYER                               │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                                                                       │   │
│  │    🔒 PRIVACY BY DESIGN                                              │   │
│  │    ━━━━━━━━━━━━━━━━━━━━━━━━━                                         │   │
│  │                                                                       │   │
│  │    ┌─────────────┐  ┌─────────────┐  ┌─────────────┐               │   │
│  │    │   Data      │  │   PII       │  │   Access    │               │   │
│  │    │   Anonym-   │  │   Remov-    │  │   Control   │               │   │
│  │    │   ization   │  │   al        │  │             │               │   │
│  │    │   (Names→   │  │   (SSN,     │  │   (Role-    │               │   │
│  │    │   Tokens)   │  │   Address)  │  │    based)   │               │   │
│  │    └─────────────┘  └─────────────┘  └─────────────┘               │   │
│  │                                                                       │   │
│  │    ┌─────────────────────────────────────────────────────────────┐   │   │
│  │    │                   GDPR COMPLIANCE                           │   │   │
│  │    │  • Purpose Limitation   • Storage Limitation                │   │   │
│  │    │  • Data Minimization     • Consent Awareness                │   │   │
│  │    └─────────────────────────────────────────────────────────────┘   │   │
│  │                                                                       │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            DATA FLOW                                         │
└─────────────────────────────────────────────────────────────────────────────┘

     ┌─────────────┐
     │   HR Data   │
     │   Source    │
     └──────┬──────┘
            │
            ▼
     ┌─────────────┐
     │   Import    │
     │   (pandas)  │
     └──────┬──────┘
            │
            ▼
     ┌─────────────────────────────────────────┐
     │         PREPROCESSING STAGE             │
     │  ┌───────────────────────────────────┐  │
     │  │ 1. Remove PII (names, IDs)       │  │
     │  │ 2. Handle missing values          │  │
     │  │ 3. Encode categorical variables   │  │
     │  │ 4. Feature engineering            │  │
     │  │ 5. Create train/test split       │  │
     │  └───────────────────────────────────┘  │
     └──────┬──────────────────────────────────┘
            │
            ▼
     ┌─────────────────────────────────────────┐
     │          MODEL TRAINING STAGE           │
     │  ┌───────────────────────────────────┐  │
     │  │  Random Forest Classifier         │  │
     │  │  - n_estimators: 100              │  │
     │  │  - max_depth: 10                  │  │
     │  │  - cross-validation               │  │
     │  └───────────────────────────────────┘  │
     └──────┬──────────────────────────────────┘
            │
            ▼
     ┌─────────────────────────────────────────┐
     │         EVALUATION STAGE                 │
     │  ┌───────────────────────────────────┐  │
     │  │  - Classification Report          │  │
     │  │  - Confusion Matrix               │  │
     │  │  - Accuracy, Precision, Recall    │  │
     │  └───────────────────────────────────┘  │
     └──────┬──────────────────────────────────┘
            │
            ▼
     ┌─────────────────────────────────────────┐
     │         XAI EXPLANATION STAGE           │
     │  ┌───────────────────────────────────┐  │
     │  │  SHAP TreeExplainer               │  │
     │  │  - Global feature importance      │  │
     │  │  - Local prediction explanations  │  │
     │  │  - Force plots                    │  │
     │  └───────────────────────────────────┘  │
     └──────┬──────────────────────────────────┘
            │
            ▼
     ┌─────────────────────────────────────────┐
     │         FAIRNESS AUDIT STAGE            │
     │  ┌───────────────────────────────────┐  │
     │  │  Bias Detection                    │  │
     │  │  - Gender parity check             │  │
     │  │  - Equalized odds                  │  │
     │  │  - Disparate impact (80% rule)    │  │
     │  └───────────────────────────────────┘  │
     └──────┬──────────────────────────────────┘
            │
            ▼
     ┌─────────────┐
     │   Output    │
     │  Reports    │
     └─────────────┘
```

---

## 3. Component Details

### 3.1 Data Ingestion

| Component | Description |
|-----------|-------------|
| **Source** | CSV file (hr_data.csv) |
| **Format** | Tabular, 310 rows × 35 columns |
| **Frequency** | Static (not real-time) |
| **Validation** | Schema validation on import |

### 3.2 Preprocessing Module

| Function | Description |
|----------|-------------|
| `clean_data()` | Remove duplicates, handle nulls |
| `anonymize()` | Replace names with tokens |
| `encode_features()` | Label/one-hot encoding |
| `engineer_features()` | Tenure, salary bands |

### 3.3 Model Component

| Parameter | Value |
|-----------|-------|
| Algorithm | Random Forest |
| Estimators | 100 |
| Max Depth | 10 |
| Min Samples Split | 5 |
| Min Samples Leaf | 2 |
| Train/Test Split | 70/30 |

### 3.4 XAI Engine

| Feature | Description |
|---------|-------------|
| **Explainer Type** | TreeExplainer (optimized for tree models) |
| **Output** | SHAP values per feature |
| **Visualization** | Force plots, beeswarm, waterfall |
| **Local Explanation** | Per-employee breakdown |
| **Global Explanation** | Aggregated feature importance |

### 3.5 Fairness Layer

| Check | Protected Attribute |
|-------|---------------------|
| Demographic Parity | Gender |
| Equalized Odds | Ethnicity |
| Disparate Impact | Age group |

---

## 4. Security Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        SECURITY LAYER                                       │
│                     (Defense in Depth)                                      │
└─────────────────────────────────────────────────────────────────────────────┘

  ┌────────────────────────────────────────────────────────────────────┐
  │ LAYER 1: DATA PROTECTION                                            │
  │                                                                     │
  │  ┌────────────────┐    ┌────────────────┐    ┌────────────────┐   │
  │  │   Encryption  │    │  Anonymization │    │  Tokenization  │   │
  │  │   at Rest     │    │    (PII)       │    │   (Names)      │   │
  │  │               │    │                │    │                │   │
  │  │  🔐 AES-256  │    │   ✓ Removed   │    │   ✓ Applied   │   │
  │  └────────────────┘    └────────────────┘    └────────────────┘   │
  └────────────────────────────────────────────────────────────────────┘
                                    │
  ┌────────────────────────────────────────────────────────────────────┐
  │ LAYER 2: ACCESS CONTROL                                            │
  │                                                                     │
  │  ┌────────────────┐    ┌────────────────┐    ┌────────────────┐   │
  │  │     RBAC      │    │   Audit Log   │    │  Data Minim-   │   │
  │  │  (Role-based) │    │   (Tracking)  │    │  ization       │   │
  │  │               │    │                │    │                │   │
  │  │  HR: Read    │    │  ✓ All access │    │  ✓ Only used  │   │
  │  │  Admin: Write │    │    recorded   │    │    features   │   │
  │  └────────────────┘    └────────────────┘    └────────────────┘   │
  └────────────────────────────────────────────────────────────────────┘
                                    │
  ┌────────────────────────────────────────────────────────────────────┐
  │ LAYER 3: PRIVACY COMPLIANCE (GDPR)                                 │
  │                                                                     │
  │  ┌────────────────────────────────────────────────────────────┐   │
  │  │                                                             │   │
  │  │   Purpose Limitation     Data Retention Policy            │   │
  │  │   └─ Turnover prediction only  └─ 2 years max            │   │
  │  │                                                             │   │
  │  │   Consent Awareness         Right to Explanation          │   │
  │  │   └─ Employees notified     └─ SHAP provides this        │   │
  │  │                                                             │   │
  │  └────────────────────────────────────────────────────────────┘   │
  └────────────────────────────────────────────────────────────────────┘
```

---

## 5. Deployment Topology

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     DEPLOYMENT TOPOLOGY                                      │
│                   (Current: Notebook Demo)                                   │
└─────────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────┐
  │                    LOCAL MACHINE                             │
  │                                                             │
  │  ┌─────────────────────────────────────────────────────┐   │
  │  │                  JUPYTER NOTEBOOK                     │   │
  │  │                                                      │   │
  │  │  ┌────────────┐  ┌────────────┐  ┌────────────┐     │   │
  │  │  │   Code    │  │  Output   │  │  Kernel   │     │   │
  │  │  │  Cells   │  │  Display  │  │  (Python) │     │   │
  │  │  └────────────┘  └────────────┘  └────────────┘     │   │
  │  │                                                      │   │
  │  │  ┌──────────────────────────────────────────────┐   │   │
  │  │  │            Local Dependencies               │   │   │
  │  │  │  • scikit-learn  • pandas   • SHAP          │   │   │
  │  │  │  • matplotlib    • seaborn  • numpy         │   │   │
  │  │  └──────────────────────────────────────────────┘   │   │
  │  └─────────────────────────────────────────────────────┘   │
  │                                                             │
  │  ┌─────────────────────────────────────────────────────┐   │
  │  │                   LOCAL STORAGE                      │   │
  │  │                                                      │   │
  │  │   /data/hr_data.csv      (Raw data)                 │   │
  │  │   /outputs/              (Generated charts)         │   │
  │  │                                                      │   │
  │  └─────────────────────────────────────────────────────┘   │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘
```

---

## 6. Future Architecture (Production)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    PRODUCTION ARCHITECTURE (FUTURE)                          │
└─────────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │                         CLOUD / ON-PREM                                   │
  │                                                                          │
  │  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐     │
  │  │   API Gateway    │  │   Load Balancer  │  │   Auth Service   │     │
  │  │   (REST API)     │  │                  │  │   (OAuth2/JWT)   │     │
  │  └────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘     │
  │           │                      │                      │               │
  │           └──────────────────────┼──────────────────────┘               │
  │                                  │                                       │
  │                                  ▼                                       │
  │  ┌─────────────────────────────────────────────────────────────────┐     │
  │  │                      MODEL SERVICE                               │     │
  │  │  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐       │     │
  │  │  │  Prediction   │  │  Explanation  │  │  Fairness     │       │     │
  │  │  │  Endpoint    │  │  Endpoint     │  │  Endpoint     │       │     │
  │  │  └───────────────┘  └───────────────┘  └───────────────┘       │     │
  │  └─────────────────────────────────────────────────────────────────┘     │
  │                                  │                                       │
  │           ┌──────────────────────┼──────────────────────┐               │
  │           │                      │                      │               │
  │           ▼                      ▼                      ▼               │
  │  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐     │
  │  │   HRIS Database  │  │   Model Store   │  │   Audit Logs    │     │
  │  │   (Workday/SAP) │  │   (Artifacts)   │  │   (Security)    │     │
  │  └──────────────────┘  └──────────────────┘  └──────────────────┘     │
  │                                                                          │
  └─────────────────────────────────────────────────────────────────────────┘
```

---

## 7. Integration Points

| Integration | Status | Description |
|-------------|--------|-------------|
| Jupyter Notebook | ✅ Complete | Interactive demo |
| HRIS System (Workday) | 🔜 Future | Real-time data sync |
| HRIS System (SAP) | 🔜 Future | Real-time data sync |
| BI Dashboard | 🔜 Future | Tableau/PowerBI |
| API Service | 🔜 Future | RESTful endpoints |

---

## 8. Infrastructure Requirements

### For Demo (Current)

| Resource | Specification |
|----------|---------------|
| CPU | 2+ cores |
| RAM | 4 GB |
| Storage | 1 GB |
| OS | Windows/Mac/Linux |

### For Production (Future)

| Resource | Specification |
|----------|---------------|
| CPU | 4+ cores |
| RAM | 16 GB |
| Storage | 10 GB (SSD) |
| Cloud | AWS/GCP/Azure |
| Database | PostgreSQL |

---

*Last updated: March 2026*
