import os
import platform

def getResourcePath():
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return base_path

WORK_NAMESPACE = getResourcePath()
IMG_PATH = "./resource/img/"
LOG_PATH = WORK_NAMESPACE + "/log/"

if("Windows" in platform.platform()):
    ADB_PATH = WORK_NAMESPACE + "\\lib\\adb\\adb.exe"
    ADB_PATH = f"\"{ADB_PATH}\" "
else:
    ADB_PATH = "adb "

START_SHELL = WORK_NAMESPACE + "\\lib\\start.sh"
CRON_FILE = WORK_NAMESPACE + "\\lib\\cron"

CACHE = "./cache/"
PROFILE = CACHE + "DHMSConf.json"
if(not os.path.exists(CACHE)):
    os.mkdir(CACHE)

SERVICES = ["visualdiagnosis", "sessiongo", "tum_producer", "tum_controller"]
SERVICE_NAME = ["可视化诊断服务", "振动文件上传服务", "数据采集服务", "tum_controller"]

SERVICE_PROFILE = ["/system/bin/etc/visualdiagnosis.yaml", "/private/conf/parser.json", "/private/conf/parser.json", "/private/conf/parser.json"]

TMP_PATH = "/data/temple/"
SERVICE_PATH = "/system/bin/"
CRON_PATH = "/var/spool/cron/crontabs/"
CONF_PATH = ["/system/bin/etc/", "/private/conf/", "/private/conf/", "/private/conf/"]
DAEMON_PROFILE_PATH = "/etc/"
PATH_LIST = [SERVICE_PATH, CONF_PATH, DAEMON_PROFILE_PATH]

SHELL = {
    "test_login": "test_login",
    "ls": "ls",
    "cd": "cd ",
    "find": "find ",
    "mkdir -p": "mkdir -p ",
    "rm": "rm ",
    "rm -rf": "rm -rf ",
    "stat": "stat ",
    "md5sum": "md5sum ",
    "getRuntime": "ps -eo pid,comm,etime | grep ",
    "df -h": "df -h ",
    "cat": "cat ",
    "mv": "mv ",
    "mv -b": "mv -b ",
    "cp": "cp ",
    "dos2unix": "dos2unix ",
    "tar xvf": "tar xvf ",
    "kill": "kill -9 $(pidof ",
    "chmod": "chmod +x ",
    "restart_dhms_daemon": "/system/bin/restart_dhms_daemon",
    "is_process": "ps -ef | grep ",
    "restart crond": "crond restart"
}

VERSION = "V0.1"
TELNET_INTERVAL = 0.5
WAITING_INTERVAL = 50
