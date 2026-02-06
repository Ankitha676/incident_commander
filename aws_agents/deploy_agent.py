import boto3
from datetime import datetime, timedelta
import os

def analyze_deployments():
    region = os.getenv("AWS_REGION", "us-east-1")
    ct = boto3.client("cloudtrail", region_name=region)

    start = datetime.utcnow() - timedelta(minutes=30)

    events = ct.lookup_events(
        LookupAttributes=[{"AttributeKey": "EventName", "AttributeValue": "UpdateService"}],
        StartTime=start
    )

    return {"recent_deploy": bool(events["Events"]), "events": events["Events"]}

