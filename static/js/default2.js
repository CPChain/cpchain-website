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
                $('#info ul li:nth-child(1)').html('height:' + msg.height);
                $('#info ul li:nth-child(2)').html('transactions:' + msg.txs_count);

                //blocks

                $('#block_0 li:nth-child(1) a').attr('href', '/explorer/block/' + msg.b0.number);
                $('.number0').text(msg.b0.number);
                $('.miner0').text(msg.b0.miner);
                $('.txs0').text(msg.b0.txs);
                $('#block_0 li:nth-child(2) a').attr('href', '/explorer/address/' + msg.b0.miner);
                $('#block_0 li:nth-child(3) a').attr('href', 'txs?block=' + msg.b0.number);
                $('.time0').text(msg.b0['time']);

                $('#block_1:first a').attr('href', '/explorer/block/' + msg.b1.number);
                $('.number1').text(msg.b1.number);
                $('.miner1').text(msg.b1.miner);
                $('.txs1').text(msg.b1.txs);
                $('#block_1 li:nth-child(2) a').attr('href', '/explorer/address/' + msg.b1.miner);
                $('#block_1 li:nth-child(3) a').attr('href', 'txs?block=' + msg.b1.number);
                $('.time1').text(msg.b1['time']);

                $('#block_2:first a').attr('href', '/explorer/block/' + msg.b2.number);
                $('.number2').text(msg.b2.number);
                $('.miner2').text(msg.b2.miner);
                $('.txs2').text(msg.b2.txs);
                $('#block_2 li:nth-child(2) a').attr('href', '/explorer/address/' + msg.b2.miner);
                $('#block_2 li:nth-child(3) a').attr('href', 'txs?block=' + msg.b2.number);
                $('.time2').text(msg.b2['time']);

                $('#block_3:first a').attr('href', '/explorer/block/' + msg.b3.number);
                $('.number3').text(msg.b3.number);
                $('.miner3').text(msg.b3.miner);
                $('.txs3').text(msg.b3.txs);
                $('#block_3 li:nth-child(2) a').attr('href', '/explorer/address/' + msg.b3.miner);
                $('#block_3 li:nth-child(3) a').attr('href', 'txs?block=' + msg.b3.number)
                $('.time3').text(msg.b3['time']);

                $('#block_4:first a').attr('href', '/explorer/block/' + msg.b4.number);
                $('.number4').text(msg.b4.number);
                $('.miner4').text(msg.b4.miner);
                $('.txs4').text(msg.b4.txs);
                $('#block_4 li:nth-child(2) a').attr('href', '/explorer/address/' + msg.b4.miner);
                $('#block_4 li:nth-child(3) a').attr('href', 'txs?block=' + msg.b4.number)
                $('.time4').text(msg.b4['time']);

                //txs

                $('#tx_0 li:first a').attr('href', '/explorer/tx/' + msg.t0.txhash);
                $('#txhash0').text(msg.t0.txhash);
                $('#from0').text(msg.t0.from);
                $('#tx_0 li:nth-child(2) a').attr('href', '/explorer/address/' + msg.t0.from);
                $('#to0').text(msg.t0.to);
                $('#tx_0 li:nth-child(3) a').attr('href', '/explorer/address/' + msg.t0.to);
                $('#time0').text(msg.t0['time']);

                $('#tx_1 li:first a').attr('href', '/explorer/tx/' + msg.t1.txhash);
                $('#txhash1').text(msg.t1.txhash);
                $('#from1').text(msg.t1.from);
                $('#tx_1 li:nth-child(2) a').attr('href', '/explorer/address/' + msg.t1.from);
                $('#to1').text(msg.t1.to);
                $('#tx_1 li:nth-child(3) a').attr('href', '/explorer/address/' + msg.t1.to);
                $('#time1').text(msg.t1['time']);

                $('#tx_2 li:nth-child(1) a').attr('href', '/explorer/tx/' + msg.t2.txhash);
                $('#txhash2').text(msg.t2.txhash);
                $('#tx_2 li:nth-child(2) a').attr('href', '/explorer/address/' + msg.t2.from);
                $('#from2').text(msg.t2.from);
                $('#tx_2 li:nth-child(3) a').attr('href', '/explorer/address/' + msg.t2.to);
                $('#to2').text(msg.t2.to);
                $('#time2').text(msg.t2['time']);

                $('#tx_3 li:first a').attr('href', '/explorer/tx/' + msg.t3.txhash);
                $('#txhash3').text(msg.t3.txhash);
                $('#tx_3 li:nth-child(2) a').attr('href', '/explorer/address/' + msg.t3.from);
                $('#from3').text(msg.t3.from);
                $('#tx_3 li:nth-child(3) a').attr('href', '/explorer/address/' + msg.t3.to);
                $('#to3').text(msg.t3.to);
                $('#time3').text(msg.t3['time']);

                $('#tx_4 li:first a').attr('href', '/explorer/tx/' + msg.t4.txhash);
                $('#txhash4').text(msg.t4.txhash);
                $('#from4').text(msg.t4.from);
                $('#tx_4 li:nth-child(2) a').attr('href', '/explorer/address/' + msg.t4.from);
                $('#to4').text(msg.t4.to);
                $('#tx_4 li:nth-child(3) a').attr('href', '/explorer/address/' + msg.t4.to);
                $('#time4').text(msg.t4['time']);

            };
            ws.onerror = function (evt) {
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
            }
        });


    }
)
;

