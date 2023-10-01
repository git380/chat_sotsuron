import json
import boto3

dynamodb = boto3.resource('dynamodb')
s3 = boto3.resource('s3')


def lambda_handler(event, context):
    # ApiGatewayManagementApi オブジェクトの初期化
    apigw = boto3.client(
        'apigatewaymanagementapi',
        endpoint_url=f'https://{event["requestContext"]["domainName"]}/{event["requestContext"]["stage"]}'
    )

    # テーブルを取得
    table = dynamodb.Table('test_chat')
    # テーブルから接続中のコネクションIDを取得
    clients = table.scan(ProjectionExpression='id').get('Items')

    # eventのbody(送信されたチャットの内容)を取得
    message = event['body']
    # 受信したJSONデータをPythonオブジェクトに変換
    data = json.loads(message)
    # dataオブジェクトには'messageId', 'client_id', 'message'が含まれる
    message_id = data.get('message_id', '')
    client_id = data.get('client_id', '')
    received_message = data.get('message', '')
    checked = data.get('checked', False)  # チェック状態を取得
    print(f"ID:{message_id}　受信ID：{client_id}　メッセージ:{received_message}　チェック状態:{checked}")

    # チャット履歴をAmazon S3で管理
    chat_history = {}
    # バケット名,オブジェクト名を指定
    s3_obj = s3.Bucket('websockethistory').Object('chat_history.json')
    # チャット履歴を読み込む
    try:
        response = s3_obj.get()
        # json -> 辞書型へ変換
        chat_history = json.loads(response['Body'].read())
    except:
        print('ファイルがありません')
    # JSONチャット履歴を辞書に追加
    chat_history[str(message_id)] = message
    # チャット履歴をjsonで保存する
    s3_obj.put(Body=json.dumps(chat_history))

    # クライアントからのメッセージをすべてのクライアントにブロードキャスト
    for client in clients:
        # コネクションIDを指定してクライアントにデータをPOST
        apigw.post_to_connection(ConnectionId=client['id'], Data=message)

    return {}
