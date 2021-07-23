# 传输单元服务部署工具

## run
```
python transUnit_login.py
```
## 打包
```
pyinstaller --uac-admin -w -i .\resource\icon.ico --clean .\transUnit_login.py
pyinstaller  --distpath .\out .\pack\transUnit.spec
```
## 封包

使用[Inno Setup Compiler](https://jrsoftware.org/isdl.php)进行封包，[封包脚本](/pack/封包.iss)