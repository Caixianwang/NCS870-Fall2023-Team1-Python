import requests
from bs4 import BeautifulSoup
import schedule
import time


def hrefTest():
    # 定义要抓取的网页URL
    url = 'https://data.ris.ripe.net/rrc04/2023.09/'

    # 使用Requests库发送HTTP GET请求
    response = requests.get(url)

    # 检查请求是否成功
    if response.status_code == 200:
        # 使用Beautiful Soup解析HTML内容
        soup = BeautifulSoup(response.text, 'html.parser')
        print(response.text)
        # 查找所有<a>标签
        links = soup.find_all('a')
        count = 0
        # 打印所有链接的文本和URL
        for link in links:
            link_text = link.text
            link_url = link.get('href')
            print(f"链接文本: {link_text}")
            print(f"链接URL: {link_url}")
            count +=1
        print(count)
    else:
        print("无法获取网页内容，状态码:", response.status_code)

# hrefTest()

def download():
    file_url = 'https://data.ris.ripe.net/rrc04/2023.09/updates.20230901.0000.gz'

    # 发送HTTP GET请求并获取文件内容
    response = requests.get(file_url)

    # 检查请求是否成功
    if response.status_code == 200:
        # 提取文件名
        file_name = file_url.split('/')[-1]

        # 保存文件内容到本地
        with open(file_name, 'wb') as file:
            file.write(response.content)

        print(f"文件'{file_name}'已成功下载.")
    else:
        print("无法下载文件，状态码:", response.status_code)

# 定义要定时执行的任务

def my_task():
    time.sleep(5)
    print("执行任务...")

# 设置定时任务，每隔一段时间执行一次
schedule.every(1).seconds.do(my_task)  # 例如，每隔5分钟执行一次任务

# 进入无限循环，持续执行定时任务
while True:
    schedule.run_pending()
    time.sleep(5)  # 可以适当调整 sleep 时间以减轻 CPU 负载