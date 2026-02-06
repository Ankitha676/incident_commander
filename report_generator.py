def generate_markdown_report(metrics, logs, deploy, decision, narrative: str):
    md = f"""
# 🚨 Autonomous Incident Report

## 📈 Metrics
- p99 Latency: {metrics['p99_latency']} ms
- Anomaly Detected: {metrics['anomaly']}

## 🧪 Logs
- Error Count: {logs['error_count']}
- Sample Errors: {logs.get('samples', [])}

## 🚀 Deployments
- Recent deployment: {deploy['recent_deploy']}

## 🧠 Decision
- Root Cause: {decision['root_cause']}
- Confidence: {decision['confidence']}
- Recommended Action: {decision['action']}

## 📘 Narrative Summary
{narrative}
"""
    print(md)
    with open("incident_report.md", "w") as f:
        f.write(md)

