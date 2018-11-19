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

                $('#block_0 li:nth-child(1) a').attr('href', 'block/' + msg.b0.number);
                $('.number0').text(msg.b0.number);
                $('.miner0').text(msg.b0.miner);
                $('.txs0').text(msg.b0.txs);
                $('#block_0 li:nth-child(2) a').attr('href', 'address/' + msg.b0.miner);
                $('#block_0 li:nth-child(3) a').attr('href', 'txs?block=' + msg.b0.number);
                $('.time0').text(msg.b0['time']);

                $('#block_1:first a').attr('href', 'block/' + msg.b1.number);
                $('.number1').text(msg.b1.number);
                $('.miner1').text(msg.b1.miner);
                $('.txs1').text(msg.b1.txs);
                $('#block_1 li:nth-child(2) a').attr('href', 'address/' + msg.b1.miner);
                $('#block_1 li:nth-child(3) a').attr('href', 'txs?block=' + msg.b1.number);
                $('.time1').text(msg.b1['time']);

                $('#block_2:first a').attr('href', 'block/' + msg.b2.number);
                $('.number2').text(msg.b2.number);
                $('.miner2').text(msg.b2.miner);
                $('.txs2').text(msg.b2.txs);
                $('#block_2 li:nth-child(2) a').attr('href', 'address/' + msg.b2.miner);
                $('#block_2 li:nth-child(3) a').attr('href', 'txs?block=' + msg.b2.number);
                $('.time2').text(msg.b2['time']);

                $('#block_3:first a').attr('href', 'block/' + msg.b3.number);
                $('.number3').text(msg.b3.number);
                $('.miner3').text(msg.b3.miner);
                $('.txs3').text(msg.b3.txs);
                $('#block_3 li:nth-child(2) a').attr('href', 'address/' + msg.b3.miner);
                $('#block_3 li:nth-child(3) a').attr('href', 'txs?block=' + msg.b3.number);
                $('.time3').text(msg.b3['time']);

                $('#block_4:first a').attr('href', 'block/' + msg.b4.number);
                $('.number4').text(msg.b4.number);
                $('.miner4').text(msg.b4.miner);
                $('.txs4').text(msg.b4.txs);
                $('#block_4 li:nth-child(2) a').attr('href', 'address/' + msg.b4.miner);
                $('#block_4 li:nth-child(3) a').attr('href', 'txs?block=' + msg.b4.number);
                $('.time4').text(msg.b4['time']);

                //txs
                //
                for (var i = 0; i < msg.txs.length; i++){
                    $('#tx_'+i+' li:first a').attr('href', 'tx/' + msg.txs[i].txhash);
                    $('#txhash'+i).text(msg.txs[i].txhash);
                    $('#from'+i).text(msg.txs[i].from);
                    $('#tx_'+i+' li:nth-child(2) a').attr('href', 'address/' + msg.txs[i].from);
                    $('#to'+i).text(msg.txs[i].to);
                    $('#tx_'+i+' li:nth-child(3) a').attr('href', 'address/' + msg.txs[i].to);
                    $('#time'+i).text(msg.txs[i].time);
                }

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

