import json
import boto3


def lambda_handler(event, context):
    # テキストを取得
    text = event['body']

    # 過去のチャット履歴を取得
    chat_history = {}
    # バケット名,オブジェクト名を指定
    obj = boto3.resource('s3').Bucket('websocethistories').Object(f'{text}.json')
    try:
        # 対象のjsonを取得し中身を取り出す
        response = obj.get()
        # json -> 辞書型へ変換
        chat_history = response['Body'].read()
    except:
        print('ファイルがありません')

    # レスポンスを作成
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': 'http://localhost:63342',
            'Access-Control-Allow-Methods': 'OPTIONS,POST'
        },
        'body': json.dumps(chat_history.decode('utf-8'))
    }
