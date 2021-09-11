#-*- coding:utf-8 -*-
import os.path
import logging
import time

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
log_path = os.getcwd() + '/logs/'
if not os.path.exists(log_path):
    os.mkdir(log_path)

log_name = log_path + rq + '.log'

fh = logging.FileHandler(log_name,mode='w')
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)
