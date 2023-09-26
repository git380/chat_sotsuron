import json

json_history = '{}'


while True:
    message_id = int(input('message_id: '))  # 同じid番号にしたらバグる
    aaa = {"messageId": message_id, "message": input('message: ')}
    message = json.dumps(aaa)

    # json -> 辞書
    chat_history = json.loads(json_history)
    # jsonキーがint型で重複した場合jsonが壊れるのでString[str(message_id)]に変換する必要がある。
    chat_history[message_id] = message
    # 辞書 -> json
    json_history = json.dumps(chat_history)
    print(json_history)
