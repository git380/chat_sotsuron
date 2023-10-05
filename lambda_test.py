import json

import requests

# API GatewayのエンドポイントURL
endpoint_url = 'https://n5cserh71j.execute-api.us-east-1.amazonaws.com/default/post'
# POSTリクエストを送信
response = requests.post(endpoint_url, data='chat_history')

# レスポンスを表示
if response.status_code == 200:
    response_data = json.loads(response.json())
    print('レスポンス:', response_data)
    for j, i in response_data.items():
        print(i)
else:
    print('エラー: レスポンスコード', response.status_code)
    print(response.text)
