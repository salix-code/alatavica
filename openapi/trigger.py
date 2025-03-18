import os


import os
import sys
import time
import signal



def daemonize():
    # 1. 创建子进程
    pid = os.fork()
    if pid > 0:
        sys.exit(0)  # 退出父进程

    # 2. 创建新的会话
    os.setsid()

    # 3. 再次创建子进程
    pid = os.fork()
    if pid > 0:
        sys.exit(0)  # 退出第一个子进程

    # 4. 重定向标准输入、输出、错误到 /dev/null
    sys.stdout.flush()
    sys.stderr.flush()
    with open('/dev/null', 'r') as f:
        os.dup2(f.fileno(), sys.stdin.fileno())
    with open('/dev/null', 'a+') as f:
        os.dup2(f.fileno(), sys.stdout.fileno())
        os.dup2(f.fileno(), sys.stderr.fileno())

    # 5. 设置工作目录
    os.chdir('/')

    # 6. 设置文件创建掩码
    os.umask(0)

class FTicker:
    def __init__(self):
        pass
    def request_last(self):
        pass
    def load_from_local(self):
        pass
    def buy(self):
        pass
    def sell(self):
        pass

class FDecideHelper:
    def __init__(self):
        pass
    def ensure_buy(self):
        pass
    def ensure_sell(self):
        pass
    def tick(self):
        pass

def run():
    ticker = FTicker()
    decider = FDecideHelper()
    ticker.load_from_local()
    while True:
        ticker.request_last()
        decider.tick()
        if decider.ensure_buy():
            ticker.buy()
        elif decider.ensure_sell():
            ticker.sell()
        time.sleep(2)



def stop(signum, frame):
    print("Daemon is stopping...")
    sys.exit(0)

if __name__ == "__main__":
    daemonize()
    signal.signal(signal.SIGTERM, stop)  # 捕获终止信号
    run()

