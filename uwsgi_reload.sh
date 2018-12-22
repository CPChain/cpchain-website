#!/bin/bash

cd "$(dirname "${BASH_SOURCE[0]}")"

mode="socket"

if [ $1 ]; then
    mode=$1
fi

if [ $mode != "socket" ]; then
    if [ $mode != "http" ]; then
        echo "Mode $1 is error, socket or http"
        exit
    fi
fi

socket="127.0.0.1:8080"
http="0.0.0.0:8000"

if [ -f uwsgi.pid ]; then
    uwsgi --stop uwsgi.pid
    sleep 3
fi

echo "[Mode]$mode"
if [ $mode == "socket" ]; then
    uwsgi --ini uwsgi.ini --http-websockets --socket $socket
else
    uwsgi --ini uwsgi.ini --http-websockets --http $http
fi
echo "Now You can access http://127.0.0.1:8000/"

