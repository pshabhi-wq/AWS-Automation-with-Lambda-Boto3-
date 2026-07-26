import os
import logging
from datetime import datetime, timezone
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ce_client = boto3.client('ce', region_name='us-east-1')
sns_client = boto3.client('sns')

def lambda_handler(event, context):
    topic_arn = os.environ.get('SNS_TOPIC_ARN')
    threshold = float(os.environ.get('COST_THRESHOLD', '50.00'))

    now = datetime.now(timezone.utc)
    start_date = now.strftime('%Y-%m-01')
    end_date = now.strftime('%Y-%m-%d')
    
    if start_date == end_date:
        return {'statusCode': 200, 'body': 'First day of month; skipping spend evaluation.'}

    response = ce_client.get_cost_and_usage(
        TimePeriod={'Start': start_date, 'End': end_date},
        Granularity='MONTHLY',
        Metrics=['UnblendedCost']
    )

    amount_str = response['ResultsByTime'][0]['Total']['UnblendedCost']['Amount']
    current_spend = float(amount_str)
    print(f"RETRIEVED MTD SPEND: ${current_spend:.2f} USD")

    if current_spend > threshold and topic_arn:
        alert_msg = f"ALERT: Month-To-Date AWS Spend is ${current_spend:.2f} USD, exceeding threshold of ${threshold:.2f} USD."
        sns_client.publish(
            TopicArn=topic_arn,
            Subject="AWS Budget Alert: Threshold Exceeded",
            Message=alert_msg
        )
        print(f"ALERT SENT to SNS Topic: {topic_arn}")

    return {'statusCode': 200, 'body': f"MTD Spend: ${current_spend:.2f} USD evaluated against ${threshold:.2f}"}