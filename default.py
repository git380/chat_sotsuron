import json
import boto3
import botocore

dynamodb = boto3.resource('dynamodb')
apigw = boto3.client('apigatewaymanagementapi', endpoint_url=F"この後出てくるAPI Gatewayの接続URL")
# 接続URL例 … https://hogehoge.execute-api.ap-northeast-1.amazonaws.com/production (@マーク以降は不要)


def lambda_handler(event, context):
    dbname = '作成したDynamoDBの名前'
    table = dynamodb.Table(dbname)
    post_data = json.loads(event.get('body', '{}')).get('data')
    print(post_data)
    # テーブルから接続中のコネクションIDを取得
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
            # コネクションIDを指定してクライアントにデータをPOST
            apigw.post_to_connection(ConnectionId=item['id'], Data=post_data)
        except botocore.exceptions.ClientError as e:
            print('Failed')
            print(e.response)
    return {}
