#! /bin/sh

sudo service mongod start
cd ..
sudo ./monitor.py
