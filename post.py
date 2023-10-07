import json
import boto3


def lambda_handler(event, context):
    # テキストを取得
    text = event['body']

    # 過去のチャット履歴(json)を取得
    chat_history = '{}'
    # バケット名,オブジェクト名を指定
    obj = boto3.resource('s3').Bucket('websocethistories').Object(f'{text}.json')
    try:
        # 対象のjsonを取得する
        chat_history = obj.get()['Body'].read()
    except:
        print('ファイルがありません')

    # レスポンスを作成
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST'
        },
        'body': chat_history
    }
