import boto3
import os

dynamodb = boto3.resource('dynamodb')


def lambda_handler(event, context):
    # テーブルを取得
    dbname = '作成したDynamoDBの名前'
    table = dynamodb.Table(dbname)
    # コネクションIDを取得
    connection_id = event['requestContext']['connectionId']
    print(f'Connection ID: {connection_id}')
    # テーブルにコネクションIDを新規登録
    table.put_item(Item={'id': connection_id})
    return {}
