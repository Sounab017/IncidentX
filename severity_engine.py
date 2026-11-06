
def assess_severity(df, category_counts, root_causes):

    errors = df[df["is_error"] == True]

    total_errors = len(errors)

    affected_services = errors["service"].nunique()

    critical_logs = df[
        df["level"].isin(["CRITICAL", "FATAL"])
    ]

    if (
        len(critical_logs) >= 1
        and affected_services >= 2
    ):
        return "Critical"

    if total_errors >= 10 and affected_services >= 3:
        return "Critical"

    if root_causes and total_errors >= 3:
        return "High"

    if total_errors >= 5:
        return "High"

    if total_errors >= 2:
        return "Medium"

    return "Low"
