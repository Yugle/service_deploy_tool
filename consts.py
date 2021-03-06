import os
import sys
import platform

# 本地路径相关变量
def getResourcePath():
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(os.path.dirname(sys.argv[0]))
    
    return base_path

WORK_NAMESPACE = getResourcePath()

if("Windows" in platform.platform()):
    ADB_PATH = WORK_NAMESPACE + "\\lib\\adb\\adb.exe"
    ADB_PATH = f"\"{ADB_PATH}\" "
    ADB_RUNTIME_OFFSET = -4

    IMG_PATH = "./resource/img/"
    LOG_PATH = "./log/"
    CACHE ="./cache/"

    FONT = "微软雅黑"
    FONT_SIZE_OFFSET = 0

    UPDATE_URL = "http://lan100.dhms.net/download/DHMS_TransUnit/DHMS传输单元服务部署工具.exe"
    UPDATE_FILE_NAME = "latest.exe"

    OPEN_SHELL = "start "
else:
    ADB_PATH = WORK_NAMESPACE + "/lib/adb_mac/adb "
    ADB_RUNTIME_OFFSET = -3

    IMG_PATH = WORK_NAMESPACE + "/resource/img/"
    LOG_PATH = WORK_NAMESPACE + "/log/"
    CACHE = WORK_NAMESPACE + "/cache/"

    FONT = "Arial"
    FONT_SIZE_OFFSET = 2

    UPDATE_URL = "http://lan100.dhms.net/download/DHMS_TransUnit/DHMS传输单元服务部署工具.dmg"
    UPDATE_FILE_NAME = "latest.dmg"

    OPEN_SHELL = "open "

if(not os.path.isdir(CACHE)):
    os.mkdir(CACHE)

PROFILE = CACHE + "DHMSConf.json"

# 远程路径相关变量
SERVICES = ["visualdiagnosis", "sessiongo", "tum_producer", "tum_controller", "python"]
SERVICE_NAME = ["可视化诊断服务", "振动文件上传服务", "数据采集服务", "tum_controller", "Python"]

SERVICE_PROFILE = ["/etc/visualdiagnosis.yaml", "/private/DHMSConf.json", "/private/DHMSConf.json", "/private/DHMSConf.json", ""]

TMP_PATH = "/data/temple/"
SERVICE_PATH = "/system/bin/"
CRON_PATH = "/etc/crontabs"
# CRON_FILE = "/etc/crontabs/root"

CONF_PATH = ["/etc/", "/private/conf/", "/private/conf/", "/private/conf/", ""]
# DAEMON_PROFILE_PATH = ["/private/", "etc"]
DAEMON_PROFILE_PATH = "/private/"
BASE_DAEMON_PROFILE_PATH = "/etc/"
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
    "tar -xvzf": "tar -xvzf ",
    "get_pid": "pidof ",
    "kill_service": "kill -9 $(pidof ",
    "kill": "kill -9 ",
    "chmod": "chmod +x ",
    "restart_dhms_daemon": "/system/bin/restart_dhms_daemon",
    "is_process": "ps -ef | grep ",
    "restart crond": "crond restart",
    "nohup_start": "nohup ",
    "nohup_end": " >/dev/null 2>&1 &"
}

# 其他
VERSION = "V1.0"
COMPANY_NAME = "胖虎"
TELNET_INTERVAL = 0.5
WAITING_INTERVAL = 50
