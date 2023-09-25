import json
import boto3

dynamodb = boto3.resource('dynamodb')


def lambda_handler(event, context):
    # ApiGatewayManagementApi オブジェクトの初期化
    apigw = boto3.client(
        'apigatewaymanagementapi',
        endpoint_url=f'https://{event["requestContext"]["domainName"]}/{event["requestContext"]["stage"]}'
    )

    # テーブルを取得
    table = dynamodb.Table('作成したDynamoDBの名前')

    # eventのbody(送信されたチャットの内容)を取得
    message = event['body']
    # 受信したJSONデータをPythonオブジェクトに変換
    data = json.loads(message)
    # dataオブジェクトのdataに送信内容が含まれる。
    message_data = data.get('data')
    print(message_data)
    # テーブルから接続中のコネクションIDを取得
    connection_ids = table.scan(ProjectionExpression='id').get('Items')
    for connection_id in connection_ids:
        print(connection_id)
        # コネクションIDを指定してクライアントにデータをPOST
        apigw.post_to_connection(ConnectionId=connection_id['id'], Data=message)
    return {}
