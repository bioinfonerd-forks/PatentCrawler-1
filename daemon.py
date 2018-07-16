import os
import re
import subprocess
import sys
from time import sleep
from utils import notify

def check_alive():
    pids = []
    raw = subprocess.getoutput('ps -ef | grep crawler.py').split('\n')
    for r in raw:
        if r.find('grep') == -1:
            pids.append(int(re.split(r' +', r)[1]))

    while True:
        sleep(60)
        if pids == []:
            notify('全挂了')
            sys.exit(1)

        for pid in pids:
            try:
                os.kill(pid, 0)
            except OSError:
                notify('PID %s 不见了' % pid)
                pids.remove(pid)

def kill_all():
    pids = []
    raw = subprocess.getoutput('ps -ef | grep crawler.py').split('\n')
    for r in raw:
        if r.find('grep') == -1:
            pids.append(int(re.split(r' +', r)[1]))
    for pid in pids:
        os.system('kill %s' % pid)

def list_all():
    raw = subprocess.getoutput('ps -ef | grep crawler.py').split('\n')
    for r in raw:
        if r.find('grep') == -1:
            print(int(re.split(r' +', r)[1]))

if __name__ == '__main__':
    if sys.argv[1] == '--list':
        list_all()
    elif sys.argv[1] == '--kill':
        kill_all()
