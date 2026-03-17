"""
RetainAI Backend - HR Turnover Prediction API
FastAPI backend serving mock data for the RetainAI demo frontend
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
import random

# Create FastAPI app
app = FastAPI(
    title="RetainAI API",
    description="HR Turnover Prediction with Explainable AI - Backend API",
    version="1.0.0"
)

# Enable CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock data for employees
MOCK_EMPLOYEES = [
    {
        "id": "EMP-2847",
        "name": "John D.",
        "department": "Engineering",
        "risk_score": 78,
        "prediction": "HIGH_RISK",
        "confidence": 82,
        "top_factor": "No promotion in 3+ years",
        "shap_explanation": {
            "increasing_risk": [
                {"factor": "No promotion in 3+ years", "impact": 22},
                {"factor": "Overtime > 20 hours/week", "impact": 18},
                {"factor": "Low engagement score (3.2)", "impact": 12},
                {"factor": "Recent manager change", "impact": 8}
            ],
            "decreasing_risk": [
                {"factor": "High tenure (5+ years)", "impact": -15},
                {"factor": "Good performance review", "impact": -8},
                {"factor": "Competitive salary", "impact": -5}
            ]
        },
        "features": {
            "tenure_years": 5,
            "promotion_years_ago": 3,
            "overtime_hours": 22,
            "engagement_score": 3.2,
            "performance_rating": 4,
            "salary_percentile": 65
        }
    },
    {
        "id": "EMP-1923",
        "name": "Sarah M.",
        "department": "Sales",
        "risk_score": 65,
        "prediction": "MEDIUM_RISK",
        "confidence": 74,
        "top_factor": "Below target sales Q4",
        "shap_explanation": {
            "increasing_risk": [
                {"factor": "Below target sales Q4", "impact": 20},
                {"factor": "No promotion in 2 years", "impact": 15},
                {"factor": "Increasing sick days", "impact": 10}
            ],
            "decreasing_risk": [
                {"factor": "Strong team relationships", "impact": -12},
                {"factor": "High salary (80th percentile)", "impact": -10},
                {"factor": "Recently completed training", "impact": -6}
            ]
        },
        "features": {
            "tenure_years": 3,
            "promotion_years_ago": 2,
            "overtime_hours": 15,
            "engagement_score": 3.8,
            "performance_rating": 3,
            "salary_percentile": 80
        }
    },
    {
        "id": "EMP-3456",
        "name": "Michael R.",
        "department": "Marketing",
        "risk_score": 42,
        "prediction": "MEDIUM_RISK",
        "confidence": 68,
        "top_factor": "Moderate engagement score",
        "shap_explanation": {
            "increasing_risk": [
                {"factor": "Moderate engagement score (3.5)", "impact": 14},
                {"factor": "No role change in 4 years", "impact": 10}
            ],
            "decreasing_risk": [
                {"factor": "Recent promotion (6 months)", "impact": -18},
                {"factor": "High team satisfaction", "impact": -12},
                {"factor": "Good work-life balance", "impact": -8}
            ]
        },
        "features": {
            "tenure_years": 4,
            "promotion_years_ago": 0.5,
            "overtime_hours": 8,
            "engagement_score": 3.5,
            "performance_rating": 4,
            "salary_percentile": 55
        }
    },
    {
        "id": "EMP-4102",
        "name": "Emily W.",
        "department": "Human Resources",
        "risk_score": 23,
        "prediction": "LOW_RISK",
        "confidence": 89,
        "top_factor": "Recently promoted",
        "shap_explanation": {
            "increasing_risk": [
                {"factor": "Slightly below avg engagement", "impact": 8}
            ],
            "decreasing_risk": [
                {"factor": "Recently promoted (3 months)", "impact": -22},
                {"factor": "High tenure (7 years)", "impact": -18},
                {"factor": "Excellent performance rating", "impact": -15},
                {"factor": "Strong manager relationship", "impact": -12}
            ]
        },
        "features": {
            "tenure_years": 7,
            "promotion_years_ago": 0.25,
            "overtime_hours": 5,
            "engagement_score": 4.1,
            "performance_rating": 5,
            "salary_percentile": 72
        }
    },
    {
        "id": "EMP-2891",
        "name": "David K.",
        "department": "Engineering",
        "risk_score": 85,
        "prediction": "HIGH_RISK",
        "confidence": 91,
        "top_factor": "Multiple risk factors detected",
        "shap_explanation": {
            "increasing_risk": [
                {"factor": "No promotion in 4+ years", "impact": 28},
                {"factor": "High overtime (>25 hrs/week)", "impact": 22},
                {"factor": "Low engagement (2.8)", "impact": 18},
                {"factor": "Manager conflict reported", "impact": 15},
                {"factor": "Salary below market rate", "impact": 12}
            ],
            "decreasing_risk": [
                {"factor": "Strong technical skills", "impact": -8}
            ]
        },
        "features": {
            "tenure_years": 6,
            "promotion_years_ago": 4,
            "overtime_hours": 27,
            "engagement_score": 2.8,
            "performance_rating": 4,
            "salary_percentile": 35
        }
    },
    {
        "id": "EMP-1567",
        "name": "Lisa T.",
        "department": "Finance",
        "risk_score": 31,
        "prediction": "LOW_RISK",
        "confidence": 76,
        "top_factor": "Good overall metrics",
        "shap_explanation": {
            "increasing_risk": [
                {"factor": "Limited career growth", "impact": 10}
            ],
            "decreasing_risk": [
                {"factor": "High tenure (8 years)", "impact": -20},
                {"factor": "Above market salary", "impact": -15},
                {"factor": "Excellent performance", "impact": -12},
                {"factor": "Strong team bonds", "impact": -8}
            ]
        },
        "features": {
            "tenure_years": 8,
            "promotion_years_ago": 2,
            "overtime_hours": 10,
            "engagement_score": 4.3,
            "performance_rating": 5,
            "salary_percentile": 85
        }
    },
    {
        "id": "EMP-3245",
        "name": "James P.",
        "department": "Operations",
        "risk_score": 56,
        "prediction": "MEDIUM_RISK",
        "confidence": 71,
        "top_factor": "Average engagement levels",
        "shap_explanation": {
            "increasing_risk": [
                {"factor": "Average engagement (3.4)", "impact": 16},
                {"factor": "No promotion in 3 years", "impact": 14},
                {"factor": "Workload concerns", "impact": 10}
            ],
            "decreasing_risk": [
                {"factor": "Competitive compensation", "impact": -12},
                {"factor": "Stable team", "impact": -10},
                {"factor": "Recent training investment", "impact": -6}
            ]
        },
        "features": {
            "tenure_years": 4,
            "promotion_years_ago": 3,
            "overtime_hours": 12,
            "engagement_score": 3.4,
            "performance_rating": 3,
            "salary_percentile": 60
        }
    },
    {
        "id": "EMP-2089",
        "name": "Amanda L.",
        "department": "Engineering",
        "risk_score": 72,
        "prediction": "HIGH_RISK",
        "confidence": 79,
        "top_factor": "Job hopping concern",
        "shap_explanation": {
            "increasing_risk": [
                {"factor": "Multiple job changes (3 in 5 yrs)", "impact": 25},
                {"factor": "Below market salary", "impact": 18},
                {"factor": "Low engagement (3.0)", "impact": 14},
                {"factor": "No recent training", "impact": 8}
            ],
            "decreasing_risk": [
                {"factor": "Strong technical background", "impact": -10},
                {"factor": "Good performance rating", "impact": -8}
            ]
        },
        "features": {
            "tenure_years": 2,
            "promotion_years_ago": 1,
            "overtime_hours": 18,
            "engagement_score": 3.0,
            "performance_rating": 4,
            "salary_percentile": 42
        }
    },
    {
        "id": "EMP-4521",
        "name": "Robert H.",
        "department": "Sales",
        "risk_score": 88,
        "prediction": "HIGH_RISK",
        "confidence": 93,
        "top_factor": "Critical retention risk",
        "shap_explanation": {
            "increasing_risk": [
                {"factor": "Counter-offer from competitor", "impact": 30},
                {"factor": "No promotion in 5 years", "impact": 24},
                {"factor": "Highest performer - flight risk", "impact": 20},
                {"factor": "Below 25th percentile salary", "impact": 16},
                {"factor": "Recent manager departure", "impact": 10}
            ],
            "decreasing_risk": [
                {"factor": "Lives locally (low mobility)", "impact": -6}
            ]
        },
        "features": {
            "tenure_years": 6,
            "promotion_years_ago": 5,
            "overtime_hours": 20,
            "engagement_score": 3.6,
            "performance_rating": 5,
            "salary_percentile": 22
        }
    },
    {
        "id": "EMP-3892",
        "name": "Jennifer C.",
        "department": "Marketing",
        "risk_score": 15,
        "prediction": "LOW_RISK",
        "confidence": 94,
        "top_factor": "Exceptional engagement",
        "shap_explanation": {
            "increasing_risk": [],
            "decreasing_risk": [
                {"factor": "Exceptional engagement (4.8)", "impact": -25},
                {"factor": "Recently promoted", "impact": -20},
                {"factor": "Top performer", "impact": -18},
                {"factor": "Strong career path", "impact": -15},
                {"factor": "Excellent team culture", "impact": -10}
            ]
        },
        "features": {
            "tenure_years": 3,
            "promotion_years_ago": 0.5,
            "overtime_hours": 6,
            "engagement_score": 4.8,
            "performance_rating": 5,
            "salary_percentile": 78
        }
    }
]

# Risk distribution data
RISK_DISTRIBUTION = [
    {"range": "0-10", "count": 245},
    {"range": "11-20", "count": 312},
    {"range": "21-30", "count": 198},
    {"range": "31-40", "count": 156},
    {"range": "41-50", "count": 134},
    {"range": "51-60", "count": 98},
    {"range": "61-70", "count": 104},
    {"range": "71-80", "count": 67},
    {"range": "81-90", "count": 23},
    {"range": "91-100", "count": 10}
]

# Fairness audit data
FAIRNESS_DATA = {
    "last_audit": "2026-03-17",
    "gender": {
        "status": "pass",
        "disparate_impact": 0.94,
        "precision_male": 95,
        "precision_female": 93,
        "recall_male": 92,
        "recall_female": 94
    },
    "ethnicity": {
        "status": "pass",
        "disparate_impact": 0.91
    },
    "age": {
        "status": "warning",
        "disparate_impact": 0.78,
        "note": "Small sample size for 55+ group"
    },
    "marital_status": {
        "status": "pass",
        "disparate_impact": 0.96
    }
}

# Compliance data
COMPLIANCE_DATA = {
    "gdpr_compliant": True,
    "data_encrypted": True,
    "last_audit": "2026-03-17",
    "anonymization": True,
    "consent_tracking": True
}

# Stats data
STATS_DATA = {
    "total_employees": 1247,
    "avg_risk": 34,
    "high_risk_count": 89,
    "accuracy": 85,
    "trend": "+2%"
}


@app.get("/")
async def serve_frontend():
    """Serve the frontend index.html"""
    # Try to find index.html in various possible locations
    possible_paths = [
        Path("/home/tristan/Dev/hackathon-IAxRH-groupe22/index.html"),
        Path("/home/tristan/Dev/hackathon-IAxRH-groupe22/frontend/index.html"),
        Path("./index.html"),
        Path("../index.html"),
        Path("/home/tristan/Dev/hackathon-IAxRH-groupe22/backend/index.html"),
    ]
    
    for path in possible_paths:
        if path.exists():
            return FileResponse(path)
    
    # If no index.html found, return a helpful message
    return JSONResponse({
        "message": "RetainAI API is running",
        "endpoints": {
            "stats": "/api/stats",
            "employees": "/api/employees",
            "employee_detail": "/api/employees/{id}",
            "risk_distribution": "/api/risk-distribution",
            "fairness": "/api/fairness",
            "compliance": "/api/compliance"
        },
        "note": "No index.html found. Please create a frontend and place it at index.html"
    })


@app.get("/api/stats")
async def get_stats():
    """Get dashboard statistics"""
    return STATS_DATA


@app.get("/api/employees")
async def get_employees(department: str = None, risk_level: str = None):
    """
    Get list of employees with risk scores
    Optional filters: department, risk_level (HIGH_RISK, MEDIUM_RISK, LOW_RISK)
    """
    employees = MOCK_EMPLOYEES.copy()
    
    if department:
        employees = [e for e in employees if e["department"].lower() == department.lower()]
    
    if risk_level:
        employees = [e for e in employees if e["prediction"] == risk_level.upper()]
    
    # Return summary data (without full SHAP details for list view)
    return {
        "employees": [
            {
                "id": e["id"],
                "name": e["name"],
                "department": e["department"],
                "risk_score": e["risk_score"],
                "prediction": e["prediction"],
                "top_factor": e["top_factor"]
            }
            for e in employees
        ],
        "total": len(employees)
    }


@app.get("/api/employees/{employee_id}")
async def get_employee_detail(employee_id: str):
    """Get individual employee detail with SHAP explanation"""
    # Find employee by ID (case-insensitive)
    for emp in MOCK_EMPLOYEES:
        if emp["id"].upper() == employee_id.upper():
            return emp
    
    raise HTTPException(status_code=404, detail=f"Employee {employee_id} not found")


@app.get("/api/risk-distribution")
async def get_risk_distribution():
    """Get risk score distribution for histogram chart"""
    return {"distribution": RISK_DISTRIBUTION}


@app.get("/api/fairness")
async def get_fairness():
    """Get fairness audit results"""
    return FAIRNESS_DATA


@app.get("/api/compliance")
async def get_compliance():
    """Get privacy compliance status"""
    return COMPLIANCE_DATA


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "RetainAI API"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
