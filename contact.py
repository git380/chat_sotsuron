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
            # dataオブジェクトには'messageId', 'client_id', 'message'が含まれる
            message_id = data.get('message_id', '')
            client_id = data.get('client_id', '')
            received_message = data.get('message', '')
            checked = data.get('checked', {})  # チェック状態を取得
            print(f"ID:{message_id}　受信ID：{client_id}　メッセージ:{received_message}　チェック状態:{checked}")
            # JSONのチャット履歴を追加
            with open('contact_history.json', 'r', encoding='utf-8') as json_file_r:
                contact_history = json.load(json_file_r)
            if str(message_id) in contact_history.keys():
                # チェック状態更新
                history = json.loads(contact_history[str(message_id)])
                history['checked'].update(checked)
                message = json.dumps(history)
                print(f"chat_history更新：{history}")
            # JSONチャット履歴を辞書に追加(キーはStringに変換)
            contact_history[str(message_id)] = message
            with open('contact_history.json', 'w', encoding='utf-8') as json_file_w:
                json.dump(contact_history, json_file_w, ensure_ascii=False, indent=4)
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
