import json, boto3, os, uuid
from datetime import datetime, timezone

dynamo = boto3.resource('dynamodb')
sns    = boto3.client('sns')
table  = dynamo.Table(os.environ['DYNAMO_TABLE'])

def handler(event, context):
    for record in event['Records']:
        msg = json.loads(record['body'])
        table.put_item(Item={
            'fileId':    str(uuid.uuid4()),
            'key':       msg['key'],
            'sizeBytes': msg['size'],
            'status':    'processed',
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'ttl':       int(datetime.now().timestamp()) + 86400 * 30
        })
        sns.publish(
            TopicArn=os.environ['SNS_TOPIC_ARN'],
            Subject='File processed',
            Message=f"File '{msg['key']}' ({msg['size']} bytes) stored."
        )