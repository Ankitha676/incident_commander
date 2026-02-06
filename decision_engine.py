def decide_root_cause(metrics, logs, deploy):
    if metrics["anomaly"] and logs["error_count"] > 0 and deploy["recent_deploy"]:
        return {
            "root_cause": "Latent configuration fault after recent deployment",
            "action": "Recommend rollback",
            "confidence": "high"
        }
    return {
        "root_cause": "Unknown",
        "action": "Investigate further",
        "confidence": "low"
    }

