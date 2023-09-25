import boto3

dynamodb = boto3.resource('dynamodb')


def lambda_handler(event, context):
    # テーブルを取得
    dbname = '作成したDynamoDBの名前'
    table = dynamodb.Table(dbname)
    # コネクションIDを取得
    connection_id = event['requestContext']['connectionId']
    print(f'Connection ID: {connection_id}')
    # テーブルからコネクションIDを削除
    table.delete_item(Key={'id': connection_id})
    return {}
