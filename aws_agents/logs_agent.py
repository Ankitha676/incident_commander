import boto3, os, time
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

def analyze_logs():
    region = os.getenv("AWS_REGION")
    log_group = os.getenv("LOG_GROUP")

    logs = boto3.client("logs", region_name=region)

    # STEP 1: get log group creation time
    try:
        lg = logs.describe_log_groups(logGroupNamePrefix=log_group)
        if not lg["logGroups"]:
            return {"error_count": 0, "errors": ["Log group exists but no logs yet"]}

        creation_time_ms = lg["logGroups"][0]["creationTime"]
        creation_time = datetime.utcfromtimestamp(creation_time_ms / 1000)

    except Exception as e:
        return {"error_count": 0, "errors": [str(e)]}

    # STEP 2: safe query window (after log group creation)
    start_time = max(
        creation_time,
        datetime.utcnow() - timedelta(minutes=5)
    )

    end_time = datetime.utcnow()

    query = """
    fields @timestamp, @message
    | filter @message like /ERROR|Exception|timeout|failed|connection/
    | sort @timestamp desc
    | limit 20
    """

    try:
        q = logs.start_query(
            logGroupName=log_group,
            startTime=int(start_time.timestamp()),
            endTime=int(end_time.timestamp()),
            queryString=query,
        )
    except Exception as e:
        return {"error_count": 0, "errors": [f"Query failed: {str(e)}"]}

    query_id = q["queryId"]

    while True:
        res = logs.get_query_results(queryId=query_id)
        if res["status"] == "Complete":
            break
        time.sleep(1)

    errors = []
    for row in res["results"]:
        for field in row:
            if field["field"] == "@message":
                errors.append(field["value"])

    return {
        "error_count": len(errors),
        "errors": errors[:5]
    }

