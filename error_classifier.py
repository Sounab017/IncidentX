
import re


ERROR_PATTERNS = {
    "Database": [
        r"database",
        r"connection refused",
        r"connection pool",
        r"sql error",
        r"too many connections"
    ],

    "API": [
        r"api timeout",
        r"http 5\d\d",
        r"gateway timeout",
        r"service unavailable",
        r"request timeout"
    ],

    "Network": [
        r"network",
        r"dns",
        r"packet loss",
        r"connection reset",
        r"host unreachable"
    ],

    "Memory": [
        r"out of memory",
        r"memory exhausted",
        r"oom",
        r"heap exhausted"
    ],

    "CPU": [
        r"high cpu",
        r"cpu overload",
        r"cpu utilization"
    ],

    "Authentication": [
        r"unauthorized",
        r"authentication failed",
        r"invalid credentials",
        r"access denied"
    ],

    "Disk": [
        r"disk full",
        r"no space left",
        r"disk failure",
        r"storage exhausted"
    ]
}


def classify_error(message):

    message = str(message).lower()

    categories = []

    for category, patterns in ERROR_PATTERNS.items():

        for pattern in patterns:

            if re.search(pattern, message):

                categories.append(category)
                break

    return categories if categories else ["Unknown"]


def detect_events(df):

    df = df.copy()

    df["category"] = df["message"].apply(
        classify_error
    )

    df["is_error"] = (
        df["level"].isin(["ERROR", "CRITICAL", "FATAL"])
        | df["category"].apply(
            lambda categories: "Unknown" not in categories
        )
    )

    df["is_warning"] = df["level"].isin(
        ["WARNING", "WARN"]
    )

    return df
