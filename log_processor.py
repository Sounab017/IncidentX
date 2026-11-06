
import pandas as pd
import json


def process_logs(uploaded_file):

    filename = uploaded_file.name.lower()

    if filename.endswith(".json"):
        data = json.load(uploaded_file)

        if isinstance(data, dict):
            data = data.get("logs", [])

        df = pd.DataFrame(data)

    elif filename.endswith(".csv"):
        df = pd.read_csv(uploaded_file)

    elif filename.endswith(".txt"):
        content = uploaded_file.read().decode("utf-8")

        rows = []

        for line in content.splitlines():
            if line.strip():
                rows.append({"message": line.strip()})

        df = pd.DataFrame(rows)

    else:
        raise ValueError("Unsupported file format")

    # Standardise column names
    df.columns = [
        str(column).strip().lower()
        for column in df.columns
    ]

    # Standardise alternative field names
    aliases = {
        "time": "timestamp",
        "date": "timestamp",
        "log": "message",
        "error": "message",
        "service_name": "service",
        "severity": "level"
    }

    df = df.rename(columns=aliases)

    # Ensure required columns exist
    for column in ["timestamp", "service", "level", "message"]:
        if column not in df.columns:
            df[column] = "Unknown"

    df = df.fillna("Unknown")

    df["level"] = df["level"].astype(str).str.upper()

    df["message"] = df["message"].astype(str)

    return df[
        ["timestamp", "service", "level", "message"]
    ]
