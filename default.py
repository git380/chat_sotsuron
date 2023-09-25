import json
import boto3

dynamodb = boto3.resource('dynamodb')


def lambda_handler(event, context):
    # ApiGatewayManagementApi オブジェクトの初期化
    domain = event["requestContext"]["domainName"]
    stage = event["requestContext"]["stage"]

    apigw = boto3.client('apigatewaymanagementapi', endpoint_url=f'https://{domain}/{stage}')

    # テーブルを取得
    dbname = '作成したDynamoDBの名前'
    table = dynamodb.Table(dbname)
    # eventのbody(送信されたチャットの内容)を取得
    post_data = json.loads(event.get('body', '{}')).get('data')
    print(post_data)
    # テーブルから接続中のコネクションIDを取得
    items = table.scan(ProjectionExpression='id').get('Items')
    for item in items:
        print(item)
        # コネクションIDを指定してクライアントにデータをPOST
        apigw.post_to_connection(ConnectionId=item['id'], Data=post_data)
    return {}
