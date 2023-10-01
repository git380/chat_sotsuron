import json
import boto3

s3 = boto3.resource('s3')


def lambda_handler(event, context):
    # テキストを取得
    text = event['body']

    # 過去のチャット履歴を取得
    chat_history = {}
    # バケット名,オブジェクト名を指定
    s3_obj = s3.Bucket('websockethistory').Object(f'{text}.json')
    try:
        # 対象のjsonを取得し中身を取り出す
        response = s3_obj.get()
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
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps(chat_history.decode('utf-8'))
    }
