import json
import boto3


def lambda_handler(event, context):
    s3 = boto3.resource('s3').Bucket('websocethistories')
    s3.Object('chat_history.json').put(Body=json.dumps({}))
    s3.Object('status_history.json').put(Body=json.dumps({}))
    s3.Object('contact_history.json').put(Body=json.dumps({}))
    s3.Object('freechat_history.json').put(Body=json.dumps([]))

    return {}
