import boto3, os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

def analyze_metrics():
    instance_id = os.getenv("INSTANCE_ID")
    region = os.getenv("AWS_REGION")

    if not instance_id:
        return {"metrics": "Skipped (no INSTANCE_ID)"}

    cw = boto3.client("cloudwatch", region_name=region)

    cpu = cw.get_metric_statistics(
        Namespace="AWS/EC2",
        MetricName="CPUUtilization",
        Dimensions=[{"Name": "InstanceId", "Value": instance_id}],
        StartTime=datetime.utcnow() - timedelta(minutes=30),
        EndTime=datetime.utcnow(),
        Period=300,
        Statistics=["Maximum"],
    )

    values = [d["Maximum"] for d in cpu.get("Datapoints", [])]
    peak = max(values) if values else 0

    return {"cpu_peak": peak}

