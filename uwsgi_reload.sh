#!/bin/bash
uwsgi --stop uwsgi.pid
sleep 2
uwsgi --ini uwsgi.ini
