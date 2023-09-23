import sys
import json
import boto3
import botocore

g_dynamodb = boto3.resource('dynamodb')
g_apigw_management = boto3.client('apigatewaymanagementapi', endpoint_url=F"この後出てくるAPI Gatewayの接続URL")


# 接続URL例 … https://hogehoge.execute-api.ap-northeast-1.amazonaws.com/production (@マーク以降は不要)

def lambda_handler(event, context):
    dbname = '作成したDynamoDBの名前'
    table = g_dynamodb.Table(dbname)
    post_data = json.loads(event.get('body', '{}')).get('data')
    print(post_data)
    domain_name = event.get('requestContext', {}).get('domainName')
    stage = event.get('requestContext', {}).get('stage')
    items = table.scan(ProjectionExpression='id').get('Items')
    if items is None:
        return {
            'statusCode': 500,
            'headers': {
                "Access-Control-Allow-Origin": "*"
            },
            'body': json.dumps({"result": 1}, ensure_ascii=False)
        }
    for item in items:
        try:
            print(item)
            _ = g_apigw_management.post_to_connection(ConnectionId=item['id'], Data=post_data)
        except botocore.exceptions.ClientError as e:
            print('Failed')
            print(e.response)
    return {
        'statusCode': 200,
        'headers': {
            "Access-Control-Allow-Origin": "*"
        },
        'body': json.dumps({"result": 0}, ensure_ascii=False)
    }
