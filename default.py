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
    # テーブルから接続中のコネクションIDを取得
    clients = table.scan(ProjectionExpression='id').get('Items')

    # eventのbody(送信されたチャットの内容)を取得
    message = event['body']
    # 受信したJSONデータをPythonオブジェクトに変換
    data = json.loads(message)
    # dataオブジェクトには'messageId', 'client_id', 'message'が含まれる
    message_id = data.get('messageId', '')
    client_id = data.get('client_id', '')
    received_message = data.get('message', '')
    checked = data.get('checked', False)  # チェック状態を取得
    print(f"ID:{message_id}　受信ID：{client_id}　メッセージ:{received_message}　チェック状態:{checked}")
    # クライアントからのメッセージをすべてのクライアントにブロードキャスト
    for client in clients:
        # コネクションIDを指定してクライアントにデータをPOST
        apigw.post_to_connection(ConnectionId=client['id'], Data=message)

    return {}
