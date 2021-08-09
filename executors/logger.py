import logging
import os.path
import time
import consts

logger = logging.getLogger()

logger.setLevel(logging.ERROR)
rq = time.strftime('%Y%m%d', time.localtime(time.time()))

if(not os.path.isdir(consts.LOG_PATH)):
	os.mkdir(consts.LOG_PATH)

log_name = consts.LOG_PATH + rq + '.log'
logfile = log_name

fh = logging.FileHandler(logfile, mode='a')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
fh.setFormatter(formatter)

logger.addHandler(fh)