import streamlit as st
import pandas as pd
import json
import plotly.express as px

from log_processor import process_logs
from error_classifier import detect_events
from correlation_engine import correlate_incidents
from severity_engine import assess_severity
from knowledge_base import retrieve_recommendations
from report_generator import generate_report

# Page Config
st.set_page_config(
    page_title="IncidentX | Cyber-AIOps Hub",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Custom CSS
try:
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass

# Header Section
col_h1, col_h2 = st.columns([4, 1])
with col_h1:
    st.title("🛡️ IncidentX // Cyber-AIOps Command")
    st.caption("Autonomous Threat Triage, Upstream Root-Cause Isolation & Automated Remediation")
with col_h2:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("⚡ **Core Status:** `ONLINE [SECURE]`")

st.markdown("---")

# Sidebar - Controls & Inputs
with st.sidebar:
    st.header("⚙️ Telemetry Stream")
    
    input_method = st.radio(
        "Ingestion Source",
        ["Load Sample Logs", "Upload Log File", "Incident Description"]
    )

    df = None

    if input_method == "Upload Log File":
        uploaded_file = st.file_uploader(
            "Upload Logs (.txt, .json, .csv)",
            type=["txt", "json", "csv"]
        )
        if uploaded_file:
            try:
                df = process_logs(uploaded_file)
                st.success(f"Ingested: {uploaded_file.name}")
            except Exception as e:
                st.error(f"Ingestion failed: {e}")

    elif input_method == "Incident Description":
        description = st.text_area(
            "Describe Incident Scenario",
            placeholder="e.g., Database connection pool exhausted causing downstream API gateway timeouts.",
            height=130
        )
        if description.strip():
            df = pd.DataFrame([{
                "timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
                "service": "incident-reporter",
                "level": "ERROR",
                "message": description
            }])

    else:
        # Default pre-loaded sample logs so dashboard is never empty
        df = pd.DataFrame([
            {"timestamp": "2026-11-07 14:00:01", "service": "auth-service", "level": "INFO", "message": "User session initialized successfully."},
            {"timestamp": "2026-11-07 14:00:05", "service": "db-primary", "level": "ERROR", "message": "database connection refused: max connection pool reached."},
            {"timestamp": "2026-11-07 14:00:08", "service": "db-primary", "level": "CRITICAL", "message": "sql error: connection pool exhausted during query execution."},
            {"timestamp": "2026-11-07 14:00:12", "service": "api-gateway", "level": "ERROR", "message": "api timeout: GET /api/v1/orders failed after 30000ms."},
            {"timestamp": "2026-11-07 14:00:15", "service": "payment-service", "level": "ERROR", "message": "gateway timeout waiting for response from upstream database."}
        ])

    st.markdown("---")
    st.subheader("🔧 Engine Config")
    auto_analyze = st.checkbox("Autonomous Live Triage", value=True)

    if df is not None and not df.empty and input_method != "Load Sample Logs":
        run_analysis = st.button("🚀 Execute AI Triage", type="primary", use_container_width=True)
    else:
        run_analysis = True

# Run Analysis Pipeline
if df is not None and not df.empty:
    analyzed_df = detect_events(df)
    category_counts, root_causes = correlate_incidents(analyzed_df)
    severity = assess_severity(analyzed_df, category_counts, root_causes)
    categories = list(category_counts.keys())
    recommendations = retrieve_recommendations(categories)
    report = generate_report(analyzed_df, severity, category_counts, root_causes, recommendations)

    st.session_state["report"] = report
    st.session_state["analyzed_df"] = analyzed_df

# Main Dashboard Interface
if "report" in st.session_state and "analyzed_df" in st.session_state:
    report = st.session_state["report"]
    analyzed_df = st.session_state["analyzed_df"]

    # Cyber Incident Banner
    sev = report["severity"].upper()
    badge_type = f"badge-{sev.lower()}" if sev.lower() in ["critical", "high", "medium", "low"] else "badge-medium"
    
    st.markdown(
        f"""
        <div style="display: flex; justify-content: space-between; align-items: center; background: linear-gradient(135deg, #0A1628 0%, #050B14 100%); padding: 1.2rem 1.8rem; border-radius: 12px; border: 1px solid rgba(0, 240, 255, 0.3); margin-bottom: 1.5rem; box-shadow: 0 0 20px rgba(0, 240, 255, 0.05);">
            <div>
                <span style="color: #00F0FF; font-size: 0.75rem; font-family: monospace; letter-spacing: 0.15em; text-transform: uppercase;">Active Incident ID</span>
                <h2 style="margin: 0; color: #F8FAFC; font-family: monospace; letter-spacing: 0.05em;">{report['incident_id']}</h2>
            </div>
            <div>
                <span class="cyber-badge {badge_type}">TIER: {sev}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Key Metrics Grid
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Telemetry Logs Processed", report["total_logs"])
    m2.metric("Detected Anomalies", report["detected_errors"], delta=f"{int((report['detected_errors']/max(report['total_logs'],1))*100)}% density", delta_color="inverse")
    m3.metric("Error Vectors", len(report["category_counts"]))
    m4.metric("Isolated Root Causes", len(report["root_causes"]))

    st.markdown("<br>", unsafe_allow_html=True)

    # Dashboard Navigation Tabs
    tab_overview, tab_logs, tab_remediation, tab_export = st.tabs([
        "📊 Telemetry Overview", 
        "🔍 Event Evidence Log", 
        "🛠️ Root Cause & Playbooks", 
        "📄 Export & Briefing"
    ])

    # TAB 1: OVERVIEW
    with tab_overview:
        col_left, col_right = st.columns([3, 2])

        with col_left:
            st.subheader("Anomaly Distribution by Domain")
            if report["category_counts"]:
                cat_df = pd.DataFrame(
                    list(report["category_counts"].items()),
                    columns=["Category", "Count"]
                ).sort_values(by="Count", ascending=True)

                fig = px.bar(
                    cat_df,
                    x="Count",
                    y="Category",
                    orientation="h",
                    color="Count",
                    color_continuous_scale="Tealgrn",
                    text_auto=True
                )
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#E2E8F0", family="monospace"),
                    height=320,
                    margin=dict(l=20, r=20, t=20, b=20),
                    coloraxis_showscale=False
                )
                fig.update_xaxes(gridcolor="rgba(51, 65, 85, 0.5)")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No categorical errors identified.")

        with col_right:
            st.subheader("Upstream Root-Cause Isolation")
            if report["root_causes"]:
                for cause in report["root_causes"]:
                    st.error(f"🎯 **Primary Trigger:** {cause['probable_cause']}")
                    st.caption(f"**Cascading Impact:** Affecting `{', '.join(cause['related_errors'])}`")
                    st.write(f"*{cause['reason']}*")
                    st.divider()
            else:
                st.success("No cascading failures isolated.")

    # TAB 2: TELEMETRY & EVIDENCE
    with tab_logs:
        st.subheader("Live Event Log Stream")
        
        f_col1, f_col2 = st.columns([1, 2])
        with f_col1:
            level_filter = st.multiselect(
                "Filter Log Level",
                options=analyzed_df["level"].unique().tolist(),
                default=analyzed_df["level"].unique().tolist()
            )
        with f_col2:
            search_query = st.text_input("Search Telemetry Logs", placeholder="e.g. database, connection, timeout")

        filtered_df = analyzed_df[analyzed_df["level"].isin(level_filter)]
        if search_query:
            filtered_df = filtered_df[filtered_df["message"].str.contains(search_query, case=False, na=False)]

        st.dataframe(
            filtered_df,
            column_config={
                "is_error": st.column_config.CheckboxColumn("Error"),
                "is_warning": st.column_config.CheckboxColumn("Warning"),
                "category": st.column_config.ListColumn("Domains"),
            },
            use_container_width=True,
            height=400
        )

    # TAB 3: REMEDIATION
    with tab_remediation:
        st.subheader("Autonomous Resolution Playbooks")
        if report["recommendations"]:
            for item in report["recommendations"]:
                with st.expander(f"🛠️ **{item['category']} Protocol Playbook**", expanded=True):
                    st.markdown(f"**Domain Analysis:** {item['description']}")
                    
                    st.markdown("**Evaluated Root Causes:**")
                    for c in item["possible_causes"]:
                        st.markdown(f"- `{c}`")

                    st.markdown("**Actionable Resolution Steps:**")
                    for idx, act in enumerate(item["actions"], 1):
                        st.markdown(f"{idx}. **{act}**")
        else:
            st.info("No playbooks required.")

    # TAB 4: EXPORT
    with tab_export:
        st.subheader("Artifact Generation Hub")
        
        ex_col1, ex_col2 = st.columns(2)
        with ex_col1:
            st.markdown("##### Structured JSON Report")
            st.download_button(
                "📥 Download Incident JSON",
                data=json.dumps(report, indent=4, default=str),
                file_name=f"{report['incident_id']}.json",
                mime="application/json",
                use_container_width=True
            )
            st.json(report, expanded=False)

        with ex_col2:
            st.markdown("##### Executive Incident Briefing")
            summary_md = f"""# Incident Post-Mortem: {report['incident_id']}
- **Timestamp:** {report['generated_at']}
- **Assigned Severity:** {report['severity']}
- **Total Anomalies:** {report['detected_errors']}

## Root Cause Summary
"""
            for cause in report.get("root_causes", []):
                summary_md += f"- **{cause['probable_cause']}**: {cause['reason']}\n"

            summary_md += "\n## Action Plan\n"
            for rec in report.get("recommendations", []):
                for act in rec["actions"]:
                    summary_md += f"- [ ] ({rec['category']}) {act}\n"

            st.text_area("Markdown Report", summary_md, height=300)

else:
    st.info("👈 Please load sample logs or upload a log file in the sidebar.")