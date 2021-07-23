@echo ==================================
@echo 自动打包并封包
@echo ==================================
cd "C:\Users\Phil\Desktop\transunitservicedeploytool\
@echo 打包中...
@echo y | pyinstaller --distpath out pack\transUnit.spec
@echo 封包中...
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" "C:\Users\Phil\Desktop\transunitservicedeploytool\pack\封包.iss"
@echo 上传至smb服务器...
copy "C:\Users\Phil\Desktop\transunitservicedeploytool\out\DHMS传输单元服务部署工具.exe" \\192.168.1.100\dhms_share\download\DHMS_TransUnit\