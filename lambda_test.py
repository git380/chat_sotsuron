import requests

# API GatewayのエンドポイントURL
endpoint_url = 'https://ee463ao4za.execute-api.us-east-1.amazonaws.com/get_test_chat_json'
# POSTリクエストを送信
response = requests.post(endpoint_url, data='chat_history')

# レスポンスを表示
if response.status_code == 200:
    response_data = response.json()
    print('レスポンス:', response_data)
else:
    print('エラー: レスポンスコード', response.status_code)
    print(response.text)
