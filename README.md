# 🚨 IncidentX
### AI-Powered IT Incident Response Agent

IncidentX is a Python-based IT incident response application that analyzes system logs, identifies errors, detects probable root causes, assesses incident severity, and recommends remediation actions.

## Features
- Upload JSON, CSV, and TXT log files.
- Detect and classify errors automatically.
- Identify probable root causes.
- Assess incident severity.
- Generate remediation recommendations.
- Generate downloadable incident reports.

## Technologies Used
- Python
- Streamlit
- Pandas
- JSON

## Installation

Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

## Project Structure

```text
IncidentX/
├── app.py
├── log_processor.py
├── error_classifier.py
├── correlation_engine.py
├── severity_engine.py
├── knowledge_base.py
├── report_generator.py
├── knowledge_base.json
├── sample_logs.json
├── requirements.txt
├── README.md
└── reports/
```

## Developer
Sounab Adak