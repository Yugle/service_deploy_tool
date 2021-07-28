# 传输单元服务部署工具

## 运行
```
pip install -r requirements.txt
```
```
python transUnit_login.py
```
## 打包
```
pyi-makespec --uac-admin -w -i .\resource\icon.ico --clean .\transUnit_login.py
pyinstaller  --distpath .\out .\pack\transUnit.spec
```
## 封包

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

## 备注
- 服务文件要求打包为tar包，且tar包与服务文件在文件名上包含所要部署的服务名。
- .log文件支持直接打开；.log.gz无法直接打开，需要下载后解压。
- 无线连接推荐SSH协议，ADB推荐有线连接。由于Telnet协议传输文件稳定性较低，因此暂时只支持读取信息，并不支持读取log或执行部署动作；传输单元ADB服务打开无线端口会导致ADB服务直接崩溃，ADB无线连接暂时无法使用。

## Release
[DHMS传输单元部署工具.exe](http://192.168.1.100/download/DHMS_TransUnit/)