import logging
from datetime import datetime, timezone
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)
ec2_client = boto3.client('ec2')

def lambda_handler(event, context):
    logger.info(f"Event Received: {event}")
    
    instance_id = event['detail']['instance-id']
    current_date = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    
    principal = event.get('detail', {}).get('userIdentity', {}).get('principalId', 'DevOps-Automation')

    tags = [
        {'Key': 'LaunchDate', 'Value': current_date},
        {'Key': 'Environment', 'Value': 'Development'},
        {'Key': 'ManagedBy', 'Value': 'Lambda-AutoTagger'},
        {'Key': 'Owner', 'Value': principal}
    ]

    ec2_client.create_tags(Resources=[instance_id], Tags=tags)
    msg = f"SUCCESS: Tagged Instance {instance_id} with LaunchDate={current_date} and Owner={principal}"
    print(msg)

    return {'statusCode': 200, 'body': msg}