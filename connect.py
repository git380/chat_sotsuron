import boto3

dynamodb = boto3.resource('dynamodb')


def lambda_handler(event, context):
    # テーブルを取得
    table = dynamodb.Table('作成したDynamoDBの名前')
    # コネクションIDを取得
    connection_id = event['requestContext']['connectionId']
    print(f'Connection ID: {connection_id}')
    # テーブルにコネクションIDを新規登録
    table.put_item(Item={'id': connection_id})
    return {}
