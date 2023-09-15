import asyncio
import json

import websockets

# クライアントの管理用のセット
clients = set()
# チャット履歴(リスト)
chat_history = []


# クライアントからのメッセージを受信するコルーチン
async def handle_client(websocket):  # 接続が確立された
    print("クライアントが接続しました。")
    try:
        # 過去のチャット履歴を送信
        for message in chat_history:  # リストの中身(JSON)をすべて送信する
            await websocket.send(json.dumps(message))

        # 新しいクライアントのWebSocket接続をclientsセットに追加
        clients.add(websocket)

        async for message in websocket:
            # 受信したJSONデータをPythonオブジェクトに変換
            data = json.loads(message)
            # dataオブジェクトには'message'と'gpt'が含まれる
            client_id = data.get('client_id', '')
            received_message = data.get('message', '')
            print(f"受信ID：{client_id}　メッセージ:{received_message}")
            # JSONチャット履歴をリストに追加
            chat_history.append(message)
            # クライアントからのメッセージをすべてのクライアントにブロードキャスト
            for client in clients:
                await client.send(message)

    finally:  # クライアントが切断された
        print(f"接続が切断されました。")
        # クライアントのWebSocket接続をclientsセットから削除
        clients.remove(websocket)


# WebSocketサーバーを起動
start_server = websockets.serve(handle_client, "localhost", 8765)
print("サーバー起動中...")

# イベントループの開始
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
