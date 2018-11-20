var blnIsFirstTime = true;
var intCounterColor = 0;
var maxloop = 200;
var ws;
var socketurl;
var lastprice;
if (location.protocol === 'https:') {
    socketurl = "wss://" + window.location.hostname + ":8000/explorer/wshandler/";
} else {
    socketurl = "ws://" + window.location.hostname + ":8000/explorer/wshandler/";
}

$(function () {

        function connectsocket(stype) {
            var intcounter = 0;
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
                updateHeader(header);
                block = msg.block;
                txs = msg.txs;
                console.log(block);
                autoGenerateBlock(block)
            };

            ws.onerror = function () {
                console.log("->socket error");
            }
            ;
            ws.onclose = function () {
                console.log("->disconnected..");
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

