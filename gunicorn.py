
import gevent.monkey

gevent.monkey.patch_all()

import multiprocessing
import os

if not os.path.exists('log'):
    os.mkdir('log')

debug = True
# loglevel = 'debug'
bind = '0.0.0.0:50000'
# pidfile = 'log/gunicorn.pid'
# logfile = 'log/debug.log'
# errorlog = 'log/error.log'
# accesslog = 'log/access.log'
timeout = 10000



# 启动的进程数
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'gunicorn.workers.ggevent.GeventWorker'

x_forwarded_for_header = 'X-FORWARDED-FOR'




























