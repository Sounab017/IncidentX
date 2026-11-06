
from collections import Counter


DEPENDENCIES = {
    "Database": ["API"],
    "Network": ["Database", "API"],
    "Memory": ["API", "Database"],
    "CPU": ["API", "Database"],
    "Disk": ["Database", "API"],
    "Authentication": ["API"]
}


def correlate_incidents(df):

    errors = df[df["is_error"] == True].copy()

    category_counts = Counter()

    for categories in errors["category"]:
        for category in categories:
            if category != "Unknown":
                category_counts[category] += 1

    root_causes = []

    for cause, dependent_services in DEPENDENCIES.items():

        if category_counts[cause] == 0:
            continue

        related = [
            service for service in dependent_services
            if category_counts[service] > 0
        ]

        if related:

            root_causes.append({
                "probable_cause": cause,
                "related_errors": related,
                "reason": (
                    f"{cause} errors were detected alongside "
                    f"related {', '.join(related)} errors. "
                    "The first category may be an upstream cause."
                )
            })

    return category_counts, root_causes
