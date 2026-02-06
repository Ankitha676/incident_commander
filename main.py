from aws_agents.logs_agent import analyze_logs
from aws_agents.metrics_agent import analyze_metrics
from llm_agent import ask_llm_summary

def run_incident_commander():
    logs = analyze_logs()
    metrics = analyze_metrics()

    context = f"""
INCIDENT ANALYSIS

Logs:
{logs}

Metrics:
{metrics}

Determine root cause and remediation.
"""

    summary = ask_llm_summary(context)

    with open("incident_report.md", "w") as f:
        f.write(summary)

    print("Incident report generated")

if __name__ == "__main__":
    run_incident_commander()

