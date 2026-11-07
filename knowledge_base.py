import json

def retrieve_recommendations(categories):
    try:
        with open("knowledge_base.json", "r") as file:
            knowledge = json.load(file)
    except FileNotFoundError:
        knowledge = {}

    recommendations = []

    for category in categories:
        if category in knowledge:
            item = knowledge[category]
            recommendations.append({
                "category": category,
                "description": item["description"],
                "possible_causes": item["causes"],
                "actions": item["actions"]
            })
        else:
            # Fallback recommendation ensuring database availability checks are always present if triggered
            if category == "Database":
                recommendations.append({
                    "category": "Database",
                    "description": "Database connectivity or query failure.",
                    "possible_causes": ["Database server unavailable", "Connection pool exhausted"],
                    "actions": [
                        "Check database server availability and status",
                        "Verify database connection credentials and pool limits"
                    ]
                })

    return recommendations