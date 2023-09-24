import boto3

dynamodb = boto3.resource('dynamodb')


def lambda_handler(event, context):
    # テーブルを取得
    dbname = '作成したDynamoDBの名前'
    table = dynamodb.Table(dbname)
    # コネクションIDを取得
    connection_id = event.get('requestContext', {}).get('connectionId')
    # テーブルにコネクションIDを新規登録
    table.put_item(Item={'id': connection_id})
    return {}
