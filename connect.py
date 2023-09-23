import sys
import json
import boto3

g_dynamodb = boto3.resource('dynamodb')


def lambda_handler(event, context):
    dbname = '作成したDynamoDBの名前'
    table = g_dynamodb.Table(dbname)
    connectionid = event.get('requestContext', {}).get('connectionId')
    ret = table.put_item(Item={'id': connectionid})
    return {
        'statusCode': 200,
        'headers': {
            "Access-Control-Allow-Origin": "*"
        },
        'body': json.dumps({"result": 0}, ensure_ascii=False)
    }
