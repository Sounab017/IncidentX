import json
import os
from datetime import datetime

def generate_report(
    df,
    severity,
    category_counts,
    root_causes,
    recommendations
):
    incident_id = datetime.now().strftime("INC-%Y%m%d-%H%M%S")

    report = {
        "incident_id": incident_id,
        "generated_at": datetime.now().isoformat(),
        "severity": severity,
        "total_logs": len(df),
        "detected_errors": int(df["is_error"].sum()),
        "category_counts": dict(category_counts),
        "root_causes": root_causes,
        "evidence": df[df["is_error"]].drop(columns=["category"], errors="ignore").to_dict(orient="records"),
        "recommendations": recommendations,
        "status": "Root Cause Identified - Remediation Required"
    }

    os.makedirs("reports", exist_ok=True)
    filename = f"reports/{incident_id}.json"

    with open(filename, "w") as file:
        json.dump(report, file, indent=4, default=str)

    return report