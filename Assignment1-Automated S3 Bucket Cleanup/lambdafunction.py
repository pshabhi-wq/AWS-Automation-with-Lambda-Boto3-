import os
import logging
from datetime import datetime, timezone, timedelta
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    bucket_name = os.environ.get('BUCKET_NAME')
    retention_days = float(os.environ.get('RETENTION_DAYS', '30'))
    
    if not bucket_name:
        return {'statusCode': 400, 'body': 'BUCKET_NAME environment variable missing.'}
    
    cutoff_time = datetime.now(timezone.utc) - timedelta(days=retention_days)
    paginator = s3_client.get_paginator('list_objects_v2')
    deleted_count = 0

    for page in paginator.paginate(Bucket=bucket_name):
        if 'Contents' not in page:
            continue

        to_delete = [{'Key': obj['Key']} for obj in page['Contents'] if obj['LastModified'] < cutoff_time]

        if to_delete:
            resp = s3_client.delete_objects(Bucket=bucket_name, Delete={'Objects': to_delete})
            for deleted in resp.get('Deleted', []):
                print(f"DELETED OBJECT: {deleted['Key']}")
            deleted_count += len(to_delete)

    return {'statusCode': 200, 'body': f"Deleted {deleted_count} stale objects from {bucket_name}."}