import os
import platform

def getResourcePath():
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
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
PROFILE = CACHE + "profile.json"
if(not os.path.exists(CACHE)):
    os.mkdir(CACHE)

REMOTE_PATH = "/root/phil_test/upload_test/"
SERVICE_PATH = "/system/bin/"
SHELL = {
    "test_login": "test_login",
    "ls": "ls",
    "cd": "cd ",
    "find": "find ",
    "mkdir -p": "mkdir -p ",
    "rm": "rm ",
    "stat": "stat ",
    "md5sum": "md5sum ",
    "getRuntime": "ps -ef pid,name,etime | grep ",
    "df -h": "df -h ",
    "cat": "cat "
}
