var ws;
var socketurl;
if (location.protocol === 'https:') {
    socketurl = "wss://" + window.location.host + "/explorer/wshandler/";
} else {
    socketurl = "ws://" + window.location.host + "/explorer/wshandler/";
}

$(function () {

        function connectsocket(stype) {
            ws = new WebSocket(socketurl);
            ws.onopen = function () {
                console.log("->Connected..");
                if (ws.readyState == WebSocket.OPEN) {
                    ws.send('{"event": "' + stype + '"}');
                } else {
                    console.log("->Connection is closed");
                    toggleSwitchDisplay(false);
                }
            };
            ws.onmessage = function (evt) {
                var msg = evt.data;
                msg = JSON.parse(msg);
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
                console.log("->socket error");
            };
            ws.onclose = function () {
                console.log("->disconnected..");
                connectsocket('gs');
            };
        }

        connectsocket('gs');

        function toggleSwitchDisplay(blnStatus) {
            if (blnStatus == false) {
                $("#togglesocket").prop("checked", false);
            } else {
                $("#togglesocket").prop("checked", true);
            }
        }

        $('#togglesocket').change(function () {
            if ($(this).is(":checked")) {
                connectsocket("gs");
            } else {
                ws.close();
                console.log('->Connection is closed')
            }
        });


    }
)
;

