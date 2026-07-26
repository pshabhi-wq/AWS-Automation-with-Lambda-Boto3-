import os
import logging
from datetime import datetime, timezone, timedelta
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)
ec2_client = boto3.client('ec2')

def lambda_handler(event, context):
    volume_id = os.environ.get('VOLUME_ID')
    retention_days = int(os.environ.get('RETENTION_DAYS', '30'))

    # Step 1: Create new tagged snapshot
    now = datetime.now(timezone.utc)
    snap = ec2_client.create_snapshot(
        VolumeId=volume_id,
        Description=f"Automated backup for {volume_id} on {now.isoformat()}",
        TagSpecifications=[{
            'ResourceType': 'snapshot',
            'Tags': [
                {'Key': 'CreatedBy', 'Value': 'Lambda-Backup'},
                {'Key': 'VolumeId', 'Value': volume_id}
            ]
        }]
    )
    new_snap_id = snap['SnapshotId']
    print(f"CREATED SNAPSHOT: {new_snap_id} for Volume: {volume_id}")

    # Step 2: Cleanup snapshots older than retention limit
    cutoff = now - timedelta(days=retention_days)
    existing_snaps = ec2_client.describe_snapshots(
        OwnerIds=['self'],
        Filters=[
            {'Name': 'tag:CreatedBy', 'Values': ['Lambda-Backup']},
            {'Name': 'volume-id', 'Values': [volume_id]}
        ]
    ).get('Snapshots', [])

    deleted_snaps = []
    for s in existing_snaps:
        if s['StartTime'] < cutoff:
            s_id = s['SnapshotId']
            ec2_client.delete_snapshot(SnapshotId=s_id)
            deleted_snaps.append(s_id)
            print(f"DELETED SNAPSHOT: {s_id}")

    return {'statusCode': 200, 'body': {'Created': new_snap_id, 'Deleted': deleted_snaps}}