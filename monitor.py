#!/usr/bin/env python
import subprocess
import sys


def db_monitor_start():
    subprocess.run("nohup python3 db_monitor.py &", shell=True)
    subprocess.run("nohup python3 rnode_update.py &", shell=True)


def db_monitor_stop():
    subprocess.run('pkill -f -9 db_monitor', shell=True)
    subprocess.run('pkill -f -9 rnode_update', shell=True)


def restart():
    db_monitor_stop()
    db_monitor_start()


if __name__ == '__main__':
    if sys.argv[1] == 'start':
        db_monitor_start()
    elif sys.argv[1] == 'stop':
        db_monitor_stop()
    elif sys.argv[1] == 'restart':
        restart()
    else:
        pass
