#!/usr/bin/env python3
import subprocess
import sys


def db_monitor_start():
    subprocess.run("nohup python3 db_monitor.py &", shell=True)
    subprocess.run("nohup python3 rnode_update.py &", shell=True)

def db_monitor_stop():
    subprocess.run('pkill -9 -f db_monitor', shell=True)
    subprocess.run('pkill -9 -f rnode_update', shell=True)

def restart():
    db_monitor_stop()
    db_monitor_start()


if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == 'start':
            db_monitor_start()
        elif sys.argv[1] == 'stop':
            db_monitor_stop()
    else:
        restart()
