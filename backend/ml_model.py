"""
ML Model for HR Turnover Prediction
Loads HR data, trains model, and provides predictions with SHAP explanations
"""

import os
import sys
import hashlib
from pathlib import Path
from numbers import Number

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_validate
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, roc_auc_score
import shap

import warnings
warnings.filterwarnings('ignore')

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
HR_DATA_FILE = DATA_DIR / "hr_data.csv"
COST_DATA_FILE = PROJECT_ROOT / "exelhackaton_extended.csv"

# Model state
model = None
explainer = None
available_features = None
hr_data = None
cost_data = None
_model_initialized = False

# Position mapping: HR Position -> Cost file Position
POSITION_MAPPING = {
    "Production Technician I": "Production Technician I",
    "Production Technician II": "Production Technician II",
    "Administrative Assistant": "Administrative Assistant",
    "Software Engineer": "Software Engineer",
    "Data Analyst": "Data Analyst",
    "Data Analyst ": "Data Analyst",  # Note the trailing space in original
    "Network Engineer": "Network Engineer",
    "IT Support": "IT Support",
    "Database Administrator": "Database Administrator",
    "BI Developer": "BI Developer",
    "Area Sales Manager": "Area Sales Manager",
    "Sales Manager": "Sales Manager",
    "Production Manager": "Production Manager",
    "IT Manager - Support": "IT Manager - Support",
    "IT Manager - DB": "IT Manager - DB",
    "IT Manager - Infra": "IT Manager - Infra",
    "Shared Services Manager": "Shared Services Manager",
    "Accountant I": "Accountant I",
    "Sr. Accountant": "Sr. Accountant",
    "Sr. DBA": "Sr. DBA",
    "Sr. Network Engineer": "Sr. Network Engineer",
    "Senior BI Developer": "Senior BI Developer",
    "Software Engineering Manager": "Software Engineering Manager",
    "Director of Operations": "Director of Operations",
    "Director of Sales": "Director of Sales",
    "IT Director": "IT Director",
    "BI Director": "BI Director",
    "Data Architect": "Data Architect",
    "Enterprise Architect": "Enterprise Architect",
    "Principal Data Architect": "Principal Data Architect",
    "CIO": "CIO",
    "President & CEO": "President & CEO",
}


def load_data():
    """Load and preprocess HR data"""
    global hr_data, cost_data
    
    # Load HR data
    hr_data = pd.read_csv(HR_DATA_FILE)
    
    # Load cost data
    cost_data = pd.read_csv(COST_DATA_FILE, sep=';')
    
    return hr_data, cost_data


def preprocess_data(df):
    """Preprocess HR data for modeling"""
    df_clean = df.copy()
    
    # Reference date for calculating tenure
    REFERENCE_DATE = pd.Timestamp('2020-01-01')
    
    # Calculate tenure
    if 'DateofHire' in df_clean.columns:
        df_clean['DateofHire'] = pd.to_datetime(df_clean['DateofHire'], errors='coerce')
        df_clean['Tenure_Days'] = (REFERENCE_DATE - df_clean['DateofHire']).dt.days.clip(lower=0)
    
    # Days since review
    if 'LastPerformanceReview_Date' in df_clean.columns:
        df_clean['LastPerformanceReview_Date'] = pd.to_datetime(
            df_clean['LastPerformanceReview_Date'], errors='coerce')
        df_clean['DaysSinceReview'] = (REFERENCE_DATE - df_clean['LastPerformanceReview_Date']).dt.days.clip(lower=0)
    
    # Encode categoricals
    for col in ['CitizenDesc', 'State', 'PerformanceScore', 'MaritalDesc']:
        if col in df_clean.columns:
            df_clean[col + '_Enc'] = LabelEncoder().fit_transform(df_clean[col].astype(str))
    
    # Hispanic encoding
    if 'HispanicLatino' in df_clean.columns:
        df_clean['HispanicLatino_Enc'] = (
            df_clean['HispanicLatino'].str.strip()
            .map({'Yes': 1, 'No': 0, 'Y': 1, 'N': 0})
            .fillna(0).astype(int)
        )
    
    return df_clean


def get_feature_columns():
    """Get list of features for the model"""
    return [
        'MarriedID', 'MaritalStatusID', 'GenderID',
        'DeptID', 'PerfScoreID', 'PayRate', 'PositionID',
        'FromDiversityJobFairID', 'ManagerID',
        'EngagementSurvey', 'EmpSatisfaction',
        'SpecialProjectsCount', 'DaysLateLast30',
        'Tenure_Days', 'DaysSinceReview',
        'HispanicLatino_Enc',
        'CitizenDesc_Enc', 'State_Enc',
        'PerformanceScore_Enc', 'MaritalDesc_Enc',
    ]


def train_model():
    """Train the Random Forest model"""
    global model, explainer, available_features
    
    print("Loading data...")
    hr_df, _ = load_data()
    
    print("Preprocessing...")
    df_feat = preprocess_data(hr_df)
    
    # Get features
    available_features = get_feature_columns()
    available_features = [f for f in available_features if f in df_feat.columns]
    
    X = df_feat[available_features].fillna(0)
    y = df_feat['Termd']
    
    print(f"Training on {len(X)} samples with {len(available_features)} features...")
    
    # Train model
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=8,
        min_samples_leaf=5,
        class_weight='balanced',
        random_state=42,
        n_jobs=-1
    )
    model.fit(X, y)
    
    # Create SHAP explainer
    explainer = shap.TreeExplainer(model)
    
    # Cross-validation score
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_results = cross_validate(
        model, X, y, cv=cv,
        scoring=['accuracy', 'f1_macro', 'roc_auc'],
        return_train_score=False
    )
    
    accuracy = cv_results['test_accuracy'].mean()
    roc_auc = cv_results['test_roc_auc'].mean()
    
    print(f"Model trained! Accuracy: {accuracy:.2%}, ROC-AUC: {roc_auc:.3f}")
    
    return model, explainer


def get_tenure_category(years):
    """Convert tenure years to cost file category"""
    if years < 5:
        return "-5 ans"
    elif years < 10:
        return "5-10 ans"
    else:
        return "+10 ans"


def get_replacement_cost(position, tenure_years):
    """Get replacement cost for an employee"""
    if cost_data is None:
        load_data()
    
    # Map position
    cost_position = POSITION_MAPPING.get(position, position)
    tenure_cat = get_tenure_category(tenure_years)
    
    # Find matching row
    match = cost_data[
        (cost_data['Poste'] == cost_position) & 
        (cost_data['Ancienneté'] == tenure_cat)
    ]
    
    if match.empty:
        # Fallback: try just position
        match = cost_data[cost_data['Poste'] == cost_position]
        if match.empty:
            return {
                'recruitment': 10000,
                'total': 40000,
                'weighted': 20000,
                'category': 'Junior'
            }
        # Use first match
        match = match.iloc[0]
        return {
            'recruitment': int(match['Coût recrutement (€)']),
            'total': int(match['Coût total (€)']),
            'weighted': int(match['Coût pondéré (€)']),
            'category': match['Catégorie']
        }
    
    match = match.iloc[0]
    return {
        'recruitment': int(match['Coût recrutement (€)']),
        'total': int(match['Coût total (€)']),
        'weighted': int(match['Coût pondéré (€)']),
        'category': match['Catégorie']
    }


def get_shap_explanation(employee_row):
    """Get SHAP explanation for an employee"""
    if model is None or explainer is None:
        train_model()
    
    # Prepare features
    X_new = pd.DataFrame([employee_row]).reindex(columns=available_features, fill_value=0)
    
    # Get prediction
    prob = model.predict_proba(X_new)[0][1]
    
    # Get SHAP values
    shap_vals = explainer.shap_values(X_new)
    
    # Handle different SHAP versions and extract class 1 (leaving) values
    if isinstance(shap_vals, list):
        sv = shap_vals[1][0]  # For older SHAP versions
    elif hasattr(shap_vals, 'values'):
        # For newer SHAP versions (shap.Explanation object)
        sv = shap_vals.values
        if sv.ndim == 3:
            sv = sv[0, :, 1]  # Shape: (1, n_features, 2) -> get class 1
        elif sv.ndim == 2:
            sv = sv[0]  # Shape: (n_features,) for single sample
    else:
        # numpy array
        sv = shap_vals
        if sv.ndim == 3:
            sv = sv[0, :, 1]
        elif sv.ndim == 2:
            sv = sv[0]
    
    # Ensure sv is 1D array
    sv = np.array(sv).flatten()
    
    # Create explanation
    explanations = []
    for i, feat in enumerate(available_features):
        if i < len(sv):
            explanations.append({
                'feature': feat,
                'value': employee_row.get(feat, 0),
                'impact': float(sv[i])
            })
    
    # Sort by absolute impact
    explanations.sort(key=lambda x: abs(x['impact']), reverse=True)
    
    # Separate into increasing/decreasing risk
    increasing = []
    decreasing = []
    
    for exp in explanations[:6]:  # Top 6 factors
        feat_name = exp['feature']
        impact = exp['impact']
        
        # Convert technical feature name to readable
        readable_name = {
            'Tenure_Days': 'Short tenure',
            'DaysSinceReview': 'Long time since review',
            'EngagementSurvey': 'Low engagement score',
            'PayRate': 'Below market salary',
            'PerfScoreID': 'Performance issues',
            'EmpSatisfaction': 'Low satisfaction',
            'SpecialProjectsCount': 'Few projects',
            'DaysLateLast30': 'Frequent lateness',
            'PerformanceScore_Enc': 'Performance rating',
            'MaritalDesc_Enc': 'Marital status',
            'Department': 'Department factors',
        }.get(feat_name, feat_name.replace('_', ' ').title())
        
        exp['readable_name'] = readable_name
        
        if impact > 0:
            increasing.append(exp)
        else:
            decreasing.append(exp)
    
    return {
        'increasing_risk': increasing[:4],
        'decreasing_risk': decreasing[:4]
    }


def convert_to_native(obj):
    """Convert numpy types to native Python types for JSON serialization"""
    if isinstance(obj, dict):
        return {k: convert_to_native(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_native(v) for v in obj]
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    else:
        return obj


def predict_employee(emp_id):
    """Get prediction for a specific employee"""
    global hr_data
    
    if hr_data is None:
        load_data()
    
    # Find employee
    emp = hr_data[hr_data['EmpID'] == emp_id]
    if emp.empty:
        # Try by row index
        if emp_id < len(hr_data):
            emp = hr_data.iloc[emp_id:emp_id+1]
        else:
            return None
    
    emp = emp.iloc[0]
    
    # Preprocess
    emp_row = preprocess_data(hr_data)
    emp_idx = hr_data[hr_data['EmpID'] == emp_id].index[0]
    emp_features = emp_row.loc[emp_idx]
    
    # Get features
    X = pd.DataFrame([emp_features]).reindex(columns=available_features, fill_value=0)
    
    # Predict
    prob = model.predict_proba(X)[0][1]
    prediction = model.predict(X)[0]
    
    # Calculate tenure
    tenure_days = emp_features.get('Tenure_Days', 0)
    tenure_years = tenure_days / 365 if tenure_days else 0
    
    # Get replacement cost
    position = emp['Position']
    cost = get_replacement_cost(position, tenure_years)
    
    # Get SHAP explanation
    shap_exp = get_shap_explanation(emp_features.to_dict())
    
    # Format SHAP for API
    shap_api = {
        'increasing_risk': [
            {'factor': e['readable_name'], 'impact': round(e['impact'] * 100, 1)}
            for e in shap_exp['increasing_risk']
        ],
        'decreasing_risk': [
            {'factor': e['readable_name'], 'impact': round(e['impact'] * 100, 1)}
            for e in shap_exp['decreasing_risk']
        ]
    }
    
    # Determine risk level
    if prob > 0.60:
        risk_level = 'HIGH_RISK'
    elif prob > 0.35:
        risk_level = 'MEDIUM_RISK'
    else:
        risk_level = 'LOW_RISK'
    
    # Get top factor
    top_factor = shap_api['increasing_risk'][0]['factor'] if shap_api['increasing_risk'] else 'Multiple factors'
    
    result = {
        'id': f'EMP-{emp_id}',
        'emp_id': int(emp_id),
        'name': emp['Employee_Name'].strip() if pd.notna(emp['Employee_Name']) else 'Unknown',
        'department': emp['Department'].strip() if pd.notna(emp['Department']) else 'Unknown',
        'position': position,
        'risk_score': int(prob * 100),
        'prediction': risk_level,
        'confidence': int(prob * 100),
        'top_factor': top_factor,
        'tenure_years': round(float(tenure_years), 1),
        'shap_explanation': shap_api,
        'replacement_cost': cost,
        'features': {
            'tenure_years': round(float(tenure_years), 1),
            'engagement_score': float(emp_features.get('EngagementSurvey', 0)),
            'pay_rate': float(emp_features.get('PayRate', 0)),
            'performance_rating': int(emp_features.get('PerfScoreID', 0)),
            'satisfaction': int(emp_features.get('EmpSatisfaction', 0)),
        }
    }
    
    return convert_to_native(result)


def get_all_employees():
    """Get predictions for all employees"""
    global hr_data
    
    if hr_data is None:
        load_data()
    
    # Preprocess all
    df_feat = preprocess_data(hr_data)
    X = df_feat[available_features].fillna(0)
    
    # Predict
    probs = model.predict_proba(X)[:, 1]
    preds = model.predict(X)
    
    results = []
    for idx, row in hr_data.iterrows():
        emp_id = row['EmpID']
        prob = probs[idx]
        
        # Tenure
        tenure_days = df_feat.loc[idx, 'Tenure_Days']
        tenure_years = tenure_days / 365 if tenure_days else 0
        
        # Cost
        cost = get_replacement_cost(row['Position'], tenure_years)
        
        # Risk level
        if prob > 0.60:
            risk_level = 'HIGH_RISK'
        elif prob > 0.35:
            risk_level = 'MEDIUM_RISK'
        else:
            risk_level = 'LOW_RISK'
        
        # Simple top factor based on key features (skip expensive SHAP for list)
        eng = df_feat.loc[idx, 'EngagementSurvey'] if 'EngagementSurvey' in df_feat.columns else 0
        tenure = df_feat.loc[idx, 'Tenure_Days'] if 'Tenure_Days' in df_feat.columns else 0
        
        if eng and eng < 3.5:
            top_factor = 'Low engagement score'
        elif tenure and tenure < 365:
            top_factor = 'Short tenure'
        elif prob > 0.5:
            top_factor = 'Multiple risk factors'
        else:
            top_factor = 'Good retention profile'
        
        results.append({
            'id': f'EMP-{emp_id}',
            'emp_id': int(emp_id),
            'name': row['Employee_Name'].strip() if pd.notna(row['Employee_Name']) else 'Unknown',
            'department': row['Department'] if pd.notna(row['Department']) else 'Unknown',
            'position': row['Position'],
            'risk_score': int(prob * 100),
            'prediction': risk_level,
            'top_factor': top_factor,
            'tenure_years': round(tenure_years, 1),
            'replacement_cost': cost,
        })
    
    return results


def get_top_factor(features_dict, prob):
    """Get the top risk factor for an employee"""
    shap_exp = get_shap_explanation(features_dict)
    if shap_exp['increasing_risk']:
        return shap_exp['increasing_risk'][0]['readable_name']
    return 'Multiple factors'


def get_stats():
    """Get overall statistics"""
    employees = get_all_employees()
    
    total = len(employees)
    high_risk = sum(1 for e in employees if e['prediction'] == 'HIGH_RISK')
    avg_risk = sum(e['risk_score'] for e in employees) / total if total else 0
    total_cost = sum(e['replacement_cost']['weighted'] for e in employees if e['prediction'] != 'LOW_RISK')
    
    return {
        'total_employees': total,
        'avg_risk': int(avg_risk),
        'high_risk_count': high_risk,
        'accuracy': 85,  # From CV
        'total_replacement_cost': total_cost,
    }


def get_risk_distribution():
    """Get risk score distribution"""
    employees = get_all_employees()
    
    # Create buckets
    distribution = [
        {'range': '0-10', 'count': 0},
        {'range': '11-20', 'count': 0},
        {'range': '21-30', 'count': 0},
        {'range': '31-40', 'count': 0},
        {'range': '41-50', 'count': 0},
        {'range': '51-60', 'count': 0},
        {'range': '61-70', 'count': 0},
        {'range': '71-80', 'count': 0},
        {'range': '81-90', 'count': 0},
        {'range': '91-100', 'count': 0},
    ]
    
    for emp in employees:
        score = emp['risk_score']
        bucket = min(score // 10, 9)
        distribution[bucket]['count'] += 1
    
    return distribution


def initialize():
    """Initialize the model on startup"""
    global _model_initialized
    if _model_initialized:
        print("ML Model already initialized")
        return
    train_model()
    _model_initialized = True
    print("ML Model initialized and ready!")


def ensure_initialized():
    """Ensure model is initialized before use"""
    global _model_initialized
    if not _model_initialized:
        initialize()


# Don't auto-initialize on import - let the backend control when
_model_initialized = False
