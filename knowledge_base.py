
import json


def retrieve_recommendations(categories):

    with open("knowledge_base.json", "r") as file:
        knowledge = json.load(file)

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

    return recommendations
