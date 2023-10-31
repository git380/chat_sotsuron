import asyncio
import json

import websockets

# クライアントの管理用のセット
clients = set()


# クライアントからのメッセージを受信するコルーチン
async def handle_client(websocket):  # 接続が確立された
    print("クライアントが接続しました。")
    try:
        # 新しいクライアントのWebSocket接続をclientsセットに追加
        clients.add(websocket)

        async for message in websocket:
            # 受信したJSONデータをPythonオブジェクトに変換
            data = json.loads(message)

            # JSONのチャット履歴を追加
            with open('freechat_history.json', 'r', encoding='utf-8') as json_file_r:
                chat_history = json.load(json_file_r)
            # JSONチャット履歴をリストに追加
            chat_history.append(data)
            # チャット履歴をJSONで保存
            with open('freechat_history.json', 'w', encoding='utf-8') as json_file_w:
                json.dump(chat_history, json_file_w, ensure_ascii=False, indent=4)

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
