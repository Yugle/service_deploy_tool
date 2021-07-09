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
    ADB_PATH = WORK_NAMESPACE + "\\lib\\adb\\adb.exe "
else:
    ADB_PATH = "adb "