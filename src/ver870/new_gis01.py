"""
    @author Caixian Wang
    @email 289892559@qq.com
    @date Sep. 15, 2023
    @version: 1.0.0
    @description:
                Modules include runtime environment initialization and general tools.

    @copyright Copyright (c) Sep. 15, 2023
        All Rights Reserved

    This Python code (versions 3.6 and newer)
"""

import new_utils
import requests
import json
import time


def parseIP(file_path):

    reader = new_utils.getIPReader()
    fromLine = ''
    toLine = ''
    both = False
    LngAndLats = []
    posSet = set()
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('FROM:'):
                fromLine = line[6:].strip()
            if line.startswith('TO:'):
                toLine = line[4:].strip()
                both = True
            if both:
                location1 = reader.city(fromLine).location
                fromPos = {'lng': location1.longitude, 'lat': location1.latitude}

                location2 = reader.city(toLine).location
                toPos = {'lng': location2.longitude, 'lat': location2.latitude}
                LngAndLats.append([fromPos,toPos])
                poss = location1.longitude+location1.latitude+location2.longitude+location2.latitude
                both = False
                if poss not in posSet :
                    print(fromLine,toLine)
                    print(fromPos, toPos)
                    posSet.add(poss)


    # print(LngAndLats)
    print(len(LngAndLats))
    # jsonReq = {'gis':LngAndLats}
    # headers = {'Content-Type': 'application/json'}
    # payloadText = json.dumps(jsonReq)
    # response = requests.post('http://127.0.0.1:8080/pushDefense', data=payloadText, headers=headers)
    # print(response.json())
# file_path = 'E:/project870/20230901.0000M.txt'
parseIP('E:/project870/20230901.0000M.txt')
# 1. 获取 GeoIP 数据库文件并创建 reader
# reader = new_utils.getIPReader()
#
# # 2. 进行 IP 地理位置查询
# ip_address = '192.65.185.233'
# response = reader.city(ip_address)
# # 192.65.185.3 192.65.185.40
# # {'lng': 8.1551, 'lat': 47.1449} {'lng': 8.1551, 'lat': 47.1449}
# # 192.65.185.140 192.65.185.40
# # {'lng': 8.1551, 'lat': 47.1449} {'lng': 8.1551, 'lat': 47.1449}
# # 192.65.185.233 192.65.185.40
# # {'lng': 8.1551, 'lat': 47.1449} {'lng': 8.1551, 'lat': 47.1449}
#
# # 3. 获取查询结果
# print(f"Country: {response.country.name}")
# print(f"City: {response.city.name}")
# print(f"Latitude: {response.location.latitude}")
# print(f"Longitude: {response.location.longitude}")
#
# # 4. 关闭数据库连接
# reader.close()

import requests
import csv

def get_location(ip):
    # 5d8e809ac83711
    import requests
    # 替换为你的 API 访问令牌
    api_token = '5d8e809ac83711'
    # 要查询的 IP 地址（例如，8.8.8.8）
    ip_address = ip
    # 设置 API 请求的标头，包括 API 访问令牌
    headers = {
        'Authorization': f'Bearer {api_token}'
    }
    # 发起 GET 请求以获取地理位置信息
    response = requests.get(f'https://ipinfo.io/{ip_address}/json', headers=headers)

    if response.status_code == 200:
        data = response.json()
        print(f'经度: {data["loc"].split(",")[0]}')
        print(f'纬度: {data["loc"].split(",")[1]}')
        return data["loc"].split(",")[0],data["loc"].split(",")[1]
    else:
        print(f'请求失败，状态码: {response.status_code}')
        return -1


# ip_address = "2001:07f8:001c:024a:0000:0000:0201:0001"
# loc =get_location(ip_address)
# print(loc[0],loc[1])


def parseIP1():
    file_path = 'E:/project870/20230901.0000M.txt'
    fromLine = ''
    toLine = ''
    both = False
    LngAndLats = []
    posSet = set()
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('FROM:'):
                fromLine = line[6:].strip()
            if line.startswith('TO:'):
                toLine = line[4:].strip()
                both = True
            if both:
                both = False
                try:
                    loc1 = get_location(fromLine)['loc'].split(',')
                    fromPos = {'lng': loc1[0], 'lat': loc1[1]}

                    loc2 = get_location(toLine)['loc'].split(',')
                    toPos = {'lng': loc2[0], 'lat': loc2[1]}
                    LngAndLats.append([fromPos, toPos])

                    poss = loc1[0] + loc1[1] + loc2[0] + loc2[1]
                    if poss not in posSet :
                        print(fromLine,toLine)
                        print(fromPos, toPos)
                        posSet.add(poss)
                except Exception as e:
                    print(f"An error occurred: {str(e)}")

# parseIP1()

# text = "apple,banana,cherry"
# result = text.split(",")
# print(result)

def IPS():
    file_path = 'E:/project870/20230901.0000M.txt'
    reader = new_utils.getIPReader()
    fromLine = ''
    toLine = ''
    both = False
    LngAndLats = []
    posSet = set()
    filename = "example.csv"
    ipSet = set()
    with open(file_path, 'r') as file:
        with open(filename, mode="w", newline="") as wfile:
            writer = csv.writer(wfile)
            for line in file:
                if line.startswith('FROM:'):
                    fromLine = line[6:].strip()
                    if fromLine not in ipSet:
                        print(fromLine)
                        writer.writerow([fromLine])
                        ipSet.add(fromLine)
                if line.startswith('TO:'):
                    toLine = line[4:].strip()
                    if toLine not in ipSet:
                        writer.writerow([toLine])
                        ipSet.add(toLine)

import os

def ip2pos():
    ipSet = set()
    folder_path = 'E:/project870/8701'
    filename = "ip2pos.csv"
    with open(filename, 'r') as file:
        for line in file:
            dar = line.split(',')
            ipSet.add(dar[0])

    # 遍历文件夹中的所有文件
    with open(filename, mode="a", newline="") as wfile:
        writer = csv.writer(wfile)
        for filename in os.listdir(folder_path):
            # 检查文件是否以 ".csv" 扩展名结尾
            if filename.endswith(".txt"):
                # 构建完整的文件路径
                file_path = os.path.join(folder_path, filename)
                print(filename)
                # 打开 CSV 文件并处理数据
                with open(file_path, 'r') as file:
                    for line in file:
                        if line.startswith('FROM:'):
                            fromLine = line[6:].strip()
                            if fromLine not in ipSet:
                                print(fromLine)
                                loc =get_location(fromLine)
                                writer.writerow([fromLine,loc[0],loc[1]])
                                ipSet.add(fromLine)
                        if line.startswith('TO:'):
                            toLine = line[4:].strip()
                            if toLine not in ipSet:
                                print(toLine)
                                loc = get_location(toLine)
                                writer.writerow([toLine, loc[0], loc[1]])
                                ipSet.add(toLine)
# ip2pos()