# Serverless File Processing Pipeline - AWS
import json, boto3, os

sqs = boto3.client('sqs')

def handler(event, context):
    for record in event['Records']:
        sqs.send_message(
            QueueUrl=os.environ['SQS_QUEUE_URL'],
            MessageBody=json.dumps({
                'bucket': record['s3']['bucket']['name'],
                'key':    record['s3']['object']['key'],
                'size':   record['s3']['object']['size'],
            })
        )