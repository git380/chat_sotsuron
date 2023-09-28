let webSocket; // WebSocketを格納する変数

// 参加ボタンが押されたときにWebSocketを開始
function startWebSocket() {
    webSocket = new WebSocket("wss://hogehoge.execute-api.ap-northeast-1.amazonaws.com/production");

    // WebSocketの接続が開いたときの処理
    webSocket.onopen = () => {
        console.log("WebSocketが開かれました。");
        // ここで何か追加の初期化処理を行うことができます
        document.getElementById('bms_send_btn').disabled = false; // 参加後に送信ボタンを有効にする
        // json履歴受け取り
        fetch('chat_history.json')
            .then(data => data.json())
            .then(function (chatHistory) {
                for (const key in chatHistory) {
                    handleMessage(JSON.parse(chatHistory[key]));
                }
            });
    };

    // メッセージを受信したときの処理
    webSocket.onmessage = (event) => {
        handleMessage(JSON.parse(event.data));
    };

    // WebSocketの接続が閉じたときの処理
    webSocket.onclose = () => {
        console.log("WebSocketが閉じられました。");
        // ここで再接続などの処理を行うことができます
    };
}

// メッセージを処理する関数
function handleMessage(indata) {
    const idInput = document.getElementById("idInput");
    const to_client = document.getElementById("toInput");
    if ((indata.to_client === to_client.value && indata.client_id === idInput.value) || (indata.to_client === idInput.value && indata.client_id === to_client.value)) {
        const chat = document.getElementById("chat");
        const messageId = indata.messageId;

        // すでに表示されているメッセージを検索
        const existingMessage = document.getElementById(`message-${messageId}`);

        if (existingMessage) {
            // すでに表示されているメッセージがあれば、内容を更新
            // 未読・既読
            const readStatus = existingMessage.querySelector("p.read-status");
            if (readStatus) {
                if (indata.checked) {
                    readStatus.textContent = "既読";
                } else {
                    readStatus.textContent = "未読";
                }
            }
            // チェックボックス
            const checkbox = existingMessage.querySelector("input[type='checkbox']");
            if (checkbox) {
                checkbox.checked = indata.checked;
            }
        } else {
            // 新しいメッセージを作成
            const message = document.createElement("p");//pタグ作成
            // idにmessageIDを設定
            message.id = `message-${messageId}`;
            // 表示内容
            if (indata.client_id === idInput.value) {
                message.textContent = "自分 | チャット:" + indata.message;
            } else {
                const toName = document.getElementById("toNameInput");
                message.textContent = toName.value + "さん | " + "チャット:" + indata.message;
            }

            const checkbox = document.createElement("input");
            // 未読・既読機能
            if (idInput.value === indata.client_id) {
                const check = document.createElement("p");
                if (indata.checked) {
                    check.textContent = "既読"
                } else {
                    check.textContent = "未読"
                }
                // 未読・既読ステータスを識別するためのクラスを追加
                check.classList.add("read-status");
                // 未読・既読をpタグの後に追加
                message.appendChild(check);
            } else {
                // チェックボックスを作成
                checkbox.type = "checkbox";
                checkbox.checked = indata.checked;
                // チェックボックスをpタグの後に追加
                message.appendChild(checkbox);
            }

            // チェックボックスが変更されたときの処理
            checkbox.addEventListener("change", function () {
                // チェックボックスの状態を代入
                indata["checked"] = checkbox.checked
                // JSONに戻してサーバへ送信
                webSocket.send(JSON.stringify(indata));
            });

            // messageをdivタグのchatの後に追加
            chat.appendChild(message);
        }
    }
}

// 送信ボタンが押されると、入力された文字を送る
function sendMessage() {
    const messageInput = document.getElementById("message");
    const message = messageInput.value;
    const idInput = document.getElementById("idInput");
    const clientId = idInput.value;
    const toInput = document.getElementById("toInput");
    const to_client = toInput.value;
    // JavaScriptオブジェクトを作成
    const data = {
        "messageId": Date.now(),
        "client_id": clientId,
        "message": message,
        "to_client": to_client,
        "checked": false  // チェックボックスの初期状態
    };
    // JSONへ変換
    const jsonData = JSON.stringify(data);
    // 送信
    webSocket.send(jsonData);
    messageInput.value = "";
}
