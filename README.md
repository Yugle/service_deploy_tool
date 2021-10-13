# xxxx服务部署工具

## 运行
```
pip install -r requirements.txt
```
```
python main.py
```
## 打包
生成打包脚本
```
pyi-makespec --uac-admin -w -i .\resource\icon.ico --clean .\main.py
```
打包为Windows .exe可执行文件
```
pyinstaller  --distpath .\out .\pack\transUnit.spec
```
打包成Mac .app文件(由于程序基于Windows编写调试，在Mac平台未经过测试，所以在UI和功能上可能存在问题)
```
pyinstaller  --distpath out pack/transUnitForMac.spec
```
其他打包细节参照[MQTT_Client](https://github.com/Yugle/MQTT_Client)
## 封包

### Windows

使用[Inno Setup Compiler](https://jrsoftware.org/isdl.php)进行封包，[封包脚本](/pack/封包.iss)

- 若需要管理员权限
 
    1. 在[封包脚本](/pack/封包.iss)[Setup]项中加入
    ```
    PrivilegesRequired=admin
    ```  

    2. 更改Inno Setup Compiler安装目录下的SetupLdr.e32文件。反编译SetupLdr.e32后，将  
    ```xml
    <requestedExecutionLevel level="asInvoker" uiAccess="false"/></requestedPrivileges>
    ```  

	修改为  

    ```xml
   	<requestedExecutionLevel level="requireAdministrator" uiAccess="false"/></requestedPrivileges>
    ```  

    后进行编译

- 可以使用Inno Setup Compiler安装目录下ISCC.exe进行自动封包
```
ISCC.exe xxx.iss
```

### Mac

可直接运行.app文件，发布请使用DMG创建映像

## 备注
- 可以部署单个服务文件或者及其依赖文件，服务文件在文件名上包含所要部署的服务名。
- 单个服务二进制文件直接上传；服务有依赖文件需要打包为tar包，且放在tar根目录下的文件夹下，如依赖文件etc/visualdiagnosis.yaml与服务文件visualdiagnosis打包为visualdiagnosis.tar.
- .log文件支持直接打开；.gz或.tar等压缩文件无法直接打开，需要下载后解压。
- 无线连接推荐SSH协议，ADB推荐有线连接。由于Telnet协议传输文件稳定性较低，因此暂时只支持读取信息，并不支持读取log或执行部署动作；传输单元ADB服务打开无线端口会导致ADB服务直接崩溃，ADB无线连接暂时无法使用。
- 传输单元若使用dhms_daemon, 新服务需修改配置文件dhms_conf.json;若使用tum_daemon, 使用crontab方式启动，不需要修改配置文件。如下是快速诊断服务需在dhms_conf.json中加入的内容:
```
{
  "path": "/system/bin/redis-server",
  "arg": [
    "redis-server"
  ],
  "env": [],
  "version_cmd": "redis-server -v | awk '{print $3}' | tr '\n' '.'"
},
{
  "path": "/system/bin/visualdiagnosis",
  "arg": [
    "visualdiagnosis"
  ],
  "env": [],
  "version_cmd": "visualdiagnosis -v | awk '{print $3}' | tr '\n' '.'"
}
```

## Release
[xxxx部署工具](http://192.168.1.100/download/DHMS_TransUnit/)
