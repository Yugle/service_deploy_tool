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

若需要管理员权限

- 在[封包脚本](/pack/封包.iss)[Setup]项中加入
```
PrivilegesRequired=admin
```
- 更改Inno Setup Compiler安装目录下的SetupLdr.e32文件。反编译SetupLdr.e32后，将  
```xml
<requestedExecutionLevel level="asInvoker" uiAccess="false"/></requestedPrivileges>
```
修改为  

```xml
<requestedExecutionLevel level="requireAdministrator" uiAccess="false"/></requestedPrivileges>
```  

后进行编译