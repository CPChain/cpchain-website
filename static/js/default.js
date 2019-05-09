var ws;
var socketurl;
if (location.protocol === 'https:') {
    socketurl = "wss://" + window.location.host + "/ws/explorer/";
} else {
    socketurl = "ws://" + window.location.host + "/ws/explorer/";
}

$(function () {
        function connectsocket() {
            ws = new WebSocket(socketurl);
            ws.onopen = function () {
                if (ws.readyState == WebSocket.OPEN) {
                    console.log("->Connected..");
                } else {
                    console.log("->Connection open failed");
                }
            };
            ws.onmessage = function (evt) {
                var msg = evt.data;
                msg = JSON.parse(msg).message;
                msg = JSON.parse(msg)
                console.log(msg)
                // console.log(msg.header)
                //info
                header = msg.header;
                block = msg.block;
                txs = msg.txs;
                // update header
                updateHeader(header);
                //update txs
                explorerTablesApp.txs=[];
                txs.forEach(tx => {
                    autoGenerateTx(tx)
                })
                // update block
                height = block.id;
                current_height = $('#block_id').text().slice(1,);
                if (height > current_height) {
                    autoGenerateBlock(block)
                }
            };

            ws.onerror = function () {
                console.log("->websocket error");
            };
            ws.onclose = function () {
                console.log("->disconnected..");
                reconnect();
            };
        }

        connectsocket();

        function reconnect() {
            setTimeout(function () {
                connectsocket();
            }, 2000);
        }

        window.onbeforeunload = function() {
            ws.close()
        }
    }
)
;
