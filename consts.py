import os
import platform

# WORK_NAMESPACE = os.getcwd()
IMG_PATH = "./resource/img/"

if("Windows" in platform.platform()):
    ADB_PATH = "lib\\adb\\adb.exe "
    # ADB_PATH = WORK_NAMESPACE + "\\lib\\adb\\adb.exe "
else:
    ADB_PATH = "adb " # for mac test