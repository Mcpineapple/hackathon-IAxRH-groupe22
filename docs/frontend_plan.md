# RetainAI Frontend Plan - Tech Demo

## Project: RetainAI - HR Turnover Prediction with Explainable AI  
**Capgemini x ESILV Hackathon 2026**

---

## 1. UI/UX Approach

### Design Philosophy
- **Trust-First Design**: The interface must immediately communicate transparency and explainability—these are the key differentiators
- **Professional & Clean**: Suitable for HR Directors and People Analytics teams; avoid "tech-bro" aesthetics
- **Data-Informed, Human-Centered**: Every prediction is accompanied by clear, actionable explanations

### Visual Style

| Element | Specification |
|---------|---------------|
| **Color Palette** | Deep navy (#1e3a5f), clean white (#ffffff), soft gray (#f4f6f8), accent teal (#0d9488), risk red (#dc2626), safe green (#16a34a), warning amber (#d97706) |
| **Typography** | Inter or system-ui for readability; clean sans-serif hierarchy |
| **Spacing** | 8px base unit; generous whitespace to reduce cognitive load |
| **Cards & Elevation** | Subtle shadows, rounded corners (8px), clear visual hierarchy |
| **Accessibility** | WCAG AA compliant (4.5:1 contrast minimum) |

### Key UX Principles

1. **Explainability Always Visible**: SHAP explanations are not hidden behind clicks—they're prominent
2. **Risk is Nuanced**: Use continuous scales, not binary "at risk / safe" labels
3. **Privacy is Visible**: Compliance badges are prominently displayed, not buried in footer
4. **Fairness is Auditable**: Fairness metrics are accessible and clearly explained

---

## 2. Page Structure

### Pages Required

| Page | Purpose | Priority |
|------|---------|----------|
| **Dashboard** | Overview of workforce risk, key metrics, recent alerts | Required |
| **Employee Detail** | Individual prediction with full SHAP explanation | Required |
| **Fairness Audit** | Bias detection results across protected groups | Required |
| **Privacy Center** | Compliance status, data handling info | Required |

---

## 3. Dashboard Page

### Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  HEADER: Logo | Navigation (Dashboard | Fairness | Privacy)    │
├─────────────────────────────────────────────────────────────────┤
│  HERO: "Workforce Risk Overview" + Stats Cards                  │
├───────────────────────────────┬─────────────────────────────────┤
│  RISK DISTRIBUTION CHART      │  HIGH RISK EMPLOYEES TABLE       │
│  (Bar/Area chart showing      │  (Employee name, Dept, Risk %,   │
│   risk score distribution)    │   Top factors)                  │
├───────────────────────────────┴─────────────────────────────────┤
│  FOOTER: Privacy Compliance Badges                               │
└─────────────────────────────────────────────────────────────────┘
```

### Components

#### Header
- Logo: "RetainAI" with shield icon (trust)
- Navigation: Dashboard | Fairness Audit | Privacy Center
- Subtle "Demo Mode" indicator

#### Stats Cards (4 cards in row)
1. **Total Employees Monitored**: Count with trend arrow
2. **Average Risk Score**: Percentage with color coding (green/amber/red)
3. **High Risk Count**: Number with alert badge
4. **Model Accuracy**: Percentage with info tooltip

#### Risk Distribution Chart
- Histogram or area chart showing distribution of risk scores (0-100%)
- Color gradient: green (0-30%), amber (31-70%), red (71-100%)
- Interactive: hover shows count in that range

#### High Risk Table
- Columns: Employee ID (anonymized), Department, Risk Score, Top Factor, Action
- Max 10 rows, sortable by risk score
- Click row → navigates to Employee Detail
- Risk score displayed as colored progress bar

#### Footer / Compliance Bar
- Badge: "GDPR Compliant"
- Badge: "Fairness Audited"
- Badge: "Human-in-the-Loop Required"

---

## 4. Employee Detail Page

### Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  HEADER: Back to Dashboard | Employee ID: #EMP-2847            │
├─────────────────────────────────────────────────────────────────┤
│  RISK SCORE HERO                                                │
│  ┌─────────────────────────┐  ┌────────────────────────────┐   │
│  │  78%                    │  │  PREDICTION: HIGH RISK    │   │
│  │  TURNOVER RISK         │  │  Confidence: 82%           │   │
│  │  [===RED PROGRESS===]  │  │  Based on 10 features      │   │
│  └─────────────────────────┘  └────────────────────────────┘   │
├─────────────────────────────────────────────────────────────────┤
│  SHAP EXPLANATION SECTION (THE KEY DIFFERENTIATOR)              │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  WHY THIS EMPLOYEE IS AT RISK                           │   │
│  │                                                         │   │
│  │  ↑ Increases Risk:                                      │   │
│  │    • No promotion in 3+ years     ████████████ +22%    │   │
│  │    • Overtime hours > 20/week     ██████████   +18%    │   │
│  │    • Low engagement score (3.2)   ███████     +12%    │   │
│  │                                                         │   │
│  │  ↓ Decreases Risk:                                       │   │
│  │    • High tenure (5+ years)      ██████      -15%     │   │
│  │    • Good performance review     ████        -8%      │   │
│  │                                                         │   │
│  │  [ Waterfall chart visualization ]                      │   │
│  └─────────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────────┤
│  EMPLOYEE FEATURES TABLE                                         │
│  (All input features with values - collapsible)                  │
├─────────────────────────────────────────────────────────────────┤
│  PRIVACY BADGE | RECOMMENDATION PANEL                            │
│  "This prediction is based on job-related factors only"         │
└─────────────────────────────────────────────────────────────────┘
```

### Components

#### Risk Score Hero
- Large circular gauge or progress bar showing 0-100%
- Color coded: Green (0-30), Amber (31-70), Red (71-100)
- Prediction label: "LOW RISK" / "MEDIUM RISK" / "HIGH RISK"
- Confidence percentage

#### SHAP Explanation Panel (Primary Feature)
- **Title**: "Why This Prediction"
- Two columns:
  - **Increasing Risk** (red factors): ranked by impact
  - **Decreasing Risk** (green factors): ranked by impact
- Each factor shown with:
  - Plain-language description
  - Horizontal bar showing impact magnitude
  - Numeric contribution (+/- %)
- **Visualization**: Waterfall chart or force plot style

#### Feature Details (Collapsible)
- Table of all input features used
- Values for this employee
- Data quality indicator

#### Recommendation Panel
- Contextual suggestions: "Consider promotion discussion"
- Disclaimer: "For HR review only - not a termination recommendation"

---

## 5. Fairness Audit Page

### Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  HEADER: "Fairness Audit" | "Last audited: Today" | [Re-run]  │
├─────────────────────────────────────────────────────────────────┤
│  OVERVIEW STATS                                                  │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐            │
│  │Gender    │ │Ethnicity │ │ Age      │ │Marital   │            │
│  │Parity ✓  │ │Parity ✓  │ │Parity ⚠  │ │Parity ✓  │            │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘            │
├─────────────────────────────────────────────────────────────────┤
│  DETAILED METRICS BY GROUP                                       │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Gender Analysis                                          │   │
│  │  ┌────────────────┬─────────────┬─────────────┐          │   │
│  │  │ Group          │ Precision   │ Recall       │          │   │
│  │  ├────────────────┼─────────────┼─────────────┤          │   │
│  │  │ Male           │ 95%         │ 92%         │          │   │
│  │  │ Female         │ 93%         │ 94%         │          │   │
│  │  │ Non-binary     │ N/A*        │ N/A*        │          │   │
│  │  └────────────────┴─────────────┴─────────────┘          │   │
│  │  * Insufficient sample size                               │   │
│  │  Disparate Impact Ratio: 0.94 (threshold: 0.80) ✓        │   │
│  └──────────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────────┤
│  [ Similar sections for Ethnicity, Age, Marital Status ]       │
├─────────────────────────────────────────────────────────────────┤
│  METHODOLOGY FOOTER                                              │
│  "Audit methodology: Demographic Parity, Equalized Odds"       │
└─────────────────────────────────────────────────────────────────┘
```

### Components

#### Status Cards
- One card per protected attribute
- Status indicator: ✓ (pass), ⚠ (warning), ✗ (fail)
- Click to expand detailed metrics

#### Metrics Table
- Group name
- Precision, Recall, F1 for each subgroup
- Disparate impact ratio (80% rule)
- Status badges

#### Charts
- Grouped bar chart comparing precision/recall across groups
- Radar chart for multi-group fairness overview

#### Warnings & Notes
- Sample size warnings where data is insufficient
- Explanation of metrics in plain language

---

## 6. Privacy Center Page

### Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  HEADER: "Privacy & Compliance"                                 │
├─────────────────────────────────────────────────────────────────┤
│  COMPLIANCE STATUS HERO                                          │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  🛡️ GDPR COMPLIANT    ✅ DATA ENCRYPTED    ✅ AUDITED   │  │
│  └──────────────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────────────┤
│  DATA HANDLING INFO                                              │
│  ┌────────────────────────┐  ┌────────────────────────────┐   │
│  │  ANONYMIZATION         │  │  CONSENT TRACKING          │   │
│  │  Employee names are   │  │  All predictions tied to   │   │
│  │  replaced with IDs    │  │  consent records           │   │
│  │  before model input   │  │                             │   │
│  └────────────────────────┘  └────────────────────────────┘   │
├─────────────────────────────────────────────────────────────────┤
│  WHAT WE DON'T USE                                               │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  🚫 Facial recognition data                                │  │
│  │  🚫 Social media activity                                 │  │
│  │  🚫 Health records                                        │  │
│  │  🚫 Personal communications                               │  │
│  └──────────────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────────────┤
│  EMPLOYEE RIGHTS                                                  │
│  • Right to explanation for any prediction                      │
│  • Right to request data deletion                               │
│  • Right to opt-out of predictions                              │
└─────────────────────────────────────────────────────────────────┘
```

### Components

#### Compliance Badges
- Large, prominent badges for key compliance indicators
- Click to expand details

#### Info Cards
- Anonymization explanation
- Consent tracking
- Data retention policy

#### Restrictions List
- Clear list of what's NOT used
- Builds trust by being transparent

---

## 7. Wireframe Components (Reusable)

### Risk Score Gauge
```
      ╭─────────────╮
     │              │
     │   78%        │  ← Large number, color coded
     │              │
      ╰─────────────╯
```
- Circular progress or horizontal bar
- Color: #16a34a (green), #d97706 (amber), #dc2626 (red)

### SHAP Factor Bar
```
No promotion in 3+ years  ████████████████░░░  +22%
```
- Left-aligned label
- Filled bar with remaining empty
- Numeric percentage on right

### Compliance Badge
```
┌─────────────────┐
│  🛡️ GDPR       │
│  COMPLIANT      │
└─────────────────┘
```
- Icon + text
- Subtle background
- Rounded corners

### Employee Row
```
┌──────────────────────────────────────────────────────────┐
│ EMP-2847 │ Engineering │ ████████░░ 78% │ No promo │ → │
└──────────────────────────────────────────────────────────┘
```
- Compact, scannable
- Risk bar inline
- Clickable → detail page

---

## 8. Interaction Flows

### Flow 1: View High-Risk Employee
1. User sees dashboard with risk distribution
2. Notices high-risk table entry
3. Clicks employee row
4. Lands on Employee Detail with SHAP explanation
5. Reviews factors and recommendation

### Flow 2: Check Fairness
1. User clicks "Fairness Audit" in nav
2. Sees overview status cards
3. Clicks "Age" card for details
4. Reviews metrics table and charts
5. Notes warning about small sample size

### Flow 3: Verify Privacy
1. User clicks "Privacy Center"
2. Reviews compliance badges
3. Checks "What We Don't Use" section
4. Confirms GDPR compliance

---

## 9. Technical Stack Recommendation

### For Hackathon Demo (Quick MVP)

| Layer | Technology |
|-------|------------|
| **Frontend** | Single HTML file with vanilla JS + CSS |
| **Charts** | Chart.js or simple SVG |
| **Data** | Mock JSON data (simulating API response) |
| **Hosting** | GitHub Pages or local file |

### For Production (Future)

| Layer | Technology |
|-------|------------|
| **Framework** | React or Vue 3 |
| **Styling** | Tailwind CSS |
| **Charts** | Recharts or D3.js |
| **State** | React Query |
| **API** | FastAPI backend |

---

## 10. Demo Data Structure

```json
{
  "employees": [
    {
      "id": "EMP-2847",
      "department": "Engineering",
      "risk_score": 78,
      "prediction": "HIGH_RISK",
      "confidence": 82,
      "shap_explanation": {
        "increasing_risk": [
          {"factor": "No promotion in 3+ years", "impact": 22},
          {"factor": "Overtime > 20 hours/week", "impact": 18},
          {"factor": "Low engagement score (3.2)", "impact": 12}
        ],
        "decreasing_risk": [
          {"factor": "High tenure (5+ years)", "impact": -15},
          {"factor": "Good performance review", "impact": -8}
        ]
      }
    }
  ],
  "fairness": {
    "gender": {"status": "pass", "disparate_impact": 0.94},
    "ethnicity": {"status": "pass", "disparate_impact": 0.91},
    "age": {"status": "warning", "disparate_impact": 0.78},
    "marital_status": {"status": "pass", "disparate_impact": 0.96}
  },
  "compliance": {
    "gdpr_compliant": true,
    "data_encrypted": true,
    "last_audit": "2026-03-17"
  }
}
```

---

## 11. Visual Checkpoints

| Checkpoint | Description |
|------------|-------------|
| Dashboard loads in < 2s | Quick demo means fast load |
| Risk scores are color-coded | Immediate visual parsing |
| SHAP explanations are prominent | Key differentiator visible at glance |
| Compliance badges visible | Trust signals visible |
| Fairness page is understandable | Non-technical users can interpret |
| Mobile responsive | Works on tablet for demo |

---

## 12. Success Criteria for Demo

- [ ] Demo tells a clear story: "We predict risk AND explain why"
- [ ] Non-technical HR user can understand the interface
- [ ] SHAP explanation is the visual highlight
- [ ] Privacy/fairness sections demonstrate responsible AI
- [ ] Clean, professional aesthetic fits enterprise context

---

**Plan Created**: March 2026  
**For**: RetainAI Tech Demo - Capgemini x ESILV Hackathon  
**Author**: UI Designer Agent
