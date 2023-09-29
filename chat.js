let webSocket; // WebSocketを格納する変数

// 参加ボタンが押されたときにWebSocketを開始
function startWebSocket() {
    webSocket = new WebSocket("wss://hogehoge.execute-api.ap-northeast-1.amazonaws.com/production");

    // WebSocketの接続が開いたときの処理
    webSocket.onopen = () => {
        console.log('WebSocketが開かれました。');
        // ここで何か追加の初期化処理を行うことができます
        document.getElementById('bms_send_btn').disabled = false; // 参加後に送信ボタンを有効にする
        // json履歴受け取り
        fetch('chat_history.json')
            .then(data => data.json())
            .then(chatHistory => {
                for (const key in chatHistory) {
                    handleMessage(JSON.parse(chatHistory[key]));
                }
            });
    };

    // メッセージを受信したときの処理
    webSocket.onmessage = event => handleMessage(JSON.parse(event.data));

    // WebSocketの接続が閉じたときの処理
    webSocket.onclose = () => console.log('WebSocketが閉じられました。');
}

// メッセージを処理する関数
function handleMessage(data) {
    const idInput = document.getElementById('idInput').value;
    const toInput = document.getElementById('toInput').value;
    const isMyMessage = data['client_id'] === idInput;
    // 自分が相手に送信した or 相手が自分に送信した
    if ((isMyMessage && data['to_client'] === toInput) || (data['client_id'] === toInput && data['to_client'] === idInput)) {
        // すでに表示されているメッセージを検索
        const existingMessage = document.getElementById(`message-${data['message_id']}`);

        // 更新 or 作成
        if (existingMessage) {
            // 表示されている内容を更新
            // 未読・既読
            const readStatus = existingMessage.querySelector('p.read-status');
            if (readStatus) {
                readStatus.textContent = data['checked'] ? '既読' : '未読';
            }
        } else {
            // 新しいメッセージを作成
            const message = document.createElement('p');//pタグ作成
            // idにmessage_idを設定
            message.id = `message-${data['message_id']}`;
            // 表示内容
            if (isMyMessage) {
                message.textContent = '自分 | チャット:' + data['message'];
            } else {
                const toName = document.getElementById('toNameInput');
                message.textContent = toName.value + 'さん | ' + 'チャット:' + data['message'];
            }

            // 未読・既読機能
            if (isMyMessage) {
                const check = document.createElement('p');
                check.textContent = data['checked'] ? '既読' : '未読';
                // 未読・既読ステータスを識別するためのクラスを追加
                check.classList.add('read-status');
                // 未読・既読をpタグの後に追加
                message.appendChild(check);
            } else {
                const checkbox = document.createElement('input');
                // チェックボックスを作成
                checkbox.type = 'checkbox';
                checkbox.checked = data['checked'];
                // チェックボックスをpタグの後に追加
                message.appendChild(checkbox);
                // チェックボックスが変更されたときの処理
                checkbox.addEventListener('change', () => {
                    // チェックボックスの状態を代入
                    data['checked'] = checkbox.checked;
                    // JSONに戻してサーバへ送信
                    webSocket.send(JSON.stringify(data));
                });
            }
            // messageをdivタグのchatの後に追加
            document.getElementById('chat').appendChild(message);
        }
    }
}

// 送信ボタンが押されると、入力された文字を送る
function sendMessage() {
    const messageInput = document.getElementById('message');
    // JavaScriptオブジェクトを作成
    const data = {
        'message_id': Date.now(),
        'client_id': document.getElementById('idInput').value,
        'to_client': document.getElementById('toInput').value,
        'message': messageInput.value,
        'checked': false  // チェックボックスの初期状態
    };
    // JSONへ変換して送信
    webSocket.send(JSON.stringify(data));
    messageInput.value = '';
}
