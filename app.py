
import streamlit as st
import pandas as pd
import json

from log_processor import process_logs
from error_classifier import detect_events
from correlation_engine import correlate_incidents
from severity_engine import assess_severity
from knowledge_base import retrieve_recommendations
from report_generator import generate_report


st.set_page_config(
    page_title="IncidentX",
    page_icon="🚨",
    layout="wide"
)


st.title("🚨 IncidentX")
st.subheader("AI-Powered IT Incident Response Agent")

st.write(
    "Upload system logs or describe an incident "
    "to identify errors, probable root causes "
    "and remediation recommendations."
)


# Input section

st.header("1. Incident Input")

input_method = st.radio(
    "Choose input method",
    ["Upload Log File", "Incident Description"]
)


df = None

if input_method == "Upload Log File":

    uploaded_file = st.file_uploader(
        "Upload TXT, JSON or CSV",
        type=["txt", "json", "csv"]
    )

    if uploaded_file:

        try:
            df = process_logs(uploaded_file)

        except Exception as e:
            st.error(f"Unable to process file: {e}")


else:

    description = st.text_area(
        "Describe the incident",
        placeholder=(
            "Example: Database connection failed "
            "followed by multiple API timeouts."
        )
    )

    if description.strip():

        df = pd.DataFrame([
            {
                "timestamp": "User provided",
                "service": "unknown",
                "level": "ERROR",
                "message": description
            }
        ])


# Analysis section

if df is not None and not df.empty:

    st.header("2. Log Analysis")

    st.dataframe(df, use_container_width=True)

    if st.button("🔍 Analyze Incident"):

        # Detect errors
        analyzed_df = detect_events(df)

        # Correlate errors
        category_counts, root_causes = (
            correlate_incidents(analyzed_df)
        )

        # Calculate severity
        severity = assess_severity(
            analyzed_df,
            category_counts,
            root_causes
        )

        # Retrieve recommendations
        categories = list(category_counts.keys())

        recommendations = retrieve_recommendations(
            categories
        )

        # Generate report
        report = generate_report(
            analyzed_df,
            severity,
            category_counts,
            root_causes,
            recommendations
        )

        st.session_state["report"] = report
        st.session_state["analyzed_df"] = analyzed_df

    # Display results after analysis

    if "report" in st.session_state:

        report = st.session_state["report"]

        st.header("3. Incident Analysis Results")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Total Logs",
            report["total_logs"]
        )

        col2.metric(
            "Detected Errors",
            report["detected_errors"]
        )

        col3.metric(
            "Severity",
            report["severity"]
        )

        st.subheader("Detected Error Categories")

        st.json(report["category_counts"])

        st.subheader("Probable Root Cause")

        if report["root_causes"]:

            for cause in report["root_causes"]:

                st.warning(
                    f"Probable Cause: "
                    f"{cause['probable_cause']}"
                )

                st.write(cause["reason"])

        else:
            st.info(
                "No correlated root cause identified."
            )

        st.subheader("Recommended Remediation")

        for item in report["recommendations"]:

            st.write(f"**{item['category']}**")

            for action in item["actions"]:
                st.write(f"- {action}")

        st.subheader("Incident Report")

        st.json(report)

        st.download_button(
            "Download Incident Report",
            data=json.dumps(
                report,
                indent=4,
                default=str
            ),
            file_name=f"{report['incident_id']}.json",
            mime="application/json"
        )

        st.success(
            "Incident analysis completed successfully!"
        )

else:

    st.info(
        "Upload a log file or enter an incident description "
        "to begin analysis."
    )
