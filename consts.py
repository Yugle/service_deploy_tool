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

if("Windows" in platform.platform()):
    ADB_PATH = WORK_NAMESPACE + "\\lib\\adb\\adb.exe"
    ADB_PATH = f"\"{ADB_PATH}\" "
else:
    ADB_PATH = "adb "

CACHE = "./cache/"
PROFILE = CACHE + "DHMSConf.json"
if(not os.path.exists(CACHE)):
    os.mkdir(CACHE)

SERVICES = ["visualdiagnosis", "sessiongo", "tum_producer", "tum_controller"]
SERVICE_NAME = ["可视化诊断服务", "振动文件上传服务", "数据采集服务", "tum_controller"]

SERVICE_PROFILE = ["/private/DHMSConf.json", "/private/conf/parser.json", "/private/conf/parser.json", "/private/conf/parser.json"]

TMP_PATH = "/root/temple/"
SERVICE_PATH = "/system/bin/"
CONF_PATH = ["/private/", "/private/conf/", "/private/conf/", "/private/conf/"]
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
    "restart_dhms_daemon": "/system/bin/restart_dhms_daemon"
}

VERSION = "V0.1"
TELNET_INTERVAL = 0.5
WAITING_INTERVAL = 50
