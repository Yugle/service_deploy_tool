import time
import requests
 
# 请求下载地址，以流式的。打开要下载的文件位置。
with requests.get('http://lan100.dhms.net/download/DHMS_TransUnit/DHMS%E4%BC%A0%E8%BE%93%E5%8D%95%E5%85%83%E6%9C%8D%E5%8A%A1%E9%83%A8%E7%BD%B2%E5%B7%A5%E5%85%B7.dmg', stream=True) as r, open('1.dmg', 'wb') as file:
    # 请求文件的大小单位字节B
    total_size = int(r.headers['content-length'])
    # 以下载的字节大小
    content_size = 0
    # 进度下载完成的百分比
    plan = 0
    # 请求开始的时间
    start_time = time.time()
    # 上秒的下载大小
    temp_size = 0
    # 开始下载每次请求1024字节
    for content in r.iter_content(chunk_size=1024):
        file.write(content)
        # 统计以下载大小
        content_size += len(content)
        # 计算下载进度
        plan = (content_size / total_size) * 100
        print(plan)