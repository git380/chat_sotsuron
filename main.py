import asyncio
import websockets

# クライアントの管理用のセット
clients = set()


# クライアントからのメッセージを受信するコルーチン
async def handle_client(websocket):
    # 接続が確立された
    print("クライアントが接続しました。")
    try:
        # 新しいクライアントのWebSocket接続をclientsセットに追加
        clients.add(websocket)
        async for message in websocket:
            print(f"受信内容：{message}")
            # クライアントからのメッセージをすべてのクライアントにブロードキャスト
            for client in clients:
                await client.send(message)
    finally:
        # クライアントが切断された場合、セットから削除
        clients.remove(websocket)
        print(f"接続が切断されました。")


# WebSocketサーバーを起動
start_server = websockets.serve(handle_client, "localhost", 8765)
print("サーバー起動中...")

# イベントループの開始
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
