@echo ==================================
@echo �Զ���������
@echo ==================================
cd "C:\Users\Phil\Desktop\transunitservicedeploytool\
@echo �����...
@echo y | pyinstaller --distpath out pack\transUnit.spec
@echo �����...
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" "C:\Users\Phil\Desktop\transunitservicedeploytool\pack\���.iss"
@echo �ϴ���smb������...
copy "C:\Users\Phil\Desktop\transunitservicedeploytool\out\DHMS���䵥Ԫ�����𹤾�.exe" \\192.168.1.100\dhms_share\download\DHMS_TransUnit\