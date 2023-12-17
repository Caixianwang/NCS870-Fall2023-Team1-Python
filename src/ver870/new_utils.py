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


import time
import os
import shutil
import requests
import json

# DATARoot = '/home/caixian/870/datas'
DATARoot = '/mnt/mydisk/870/datas'
TEMPPath = DATARoot + "/temp"

PUSHurl = 'http://66.135.21.56:8080/pushDefense'

def isDevelopment():
    return False
def pushOutput(jsonReq,type='normal'):
    if isDevelopment():
        if type =='topo':
            print('Topology processing complete ! ')
        else:
            print(jsonReq)
    else:
        headers = {'Content-Type': 'application/json'}
        payloadText = json.dumps(jsonReq)
        response = requests.post(PUSHurl, data=payloadText, headers=headers)
        print(response.json())

# Initializing creating folders and copying language toolkits such as C#
def initEnv():
    if not os.path.exists(DATARoot):
        os.makedirs(DATARoot,exist_ok=True)
    if not os.path.exists(TEMPPath):
        os.makedirs(TEMPPath, exist_ok=True)
        shutil.copy2('src/data_ripe/zebra-script.sh', TEMPPath + "/zebra-script.sh")
        shutil.copy2('src/data_ripe/zebra-dump-parser-modified.pl', TEMPPath + "/zebra-dump-parser-modified.pl")
        shutil.copy2('src/CSharp_Tool_BGP/ConsoleApplication1/bin/Release/ConsoleApplication1.exe', TEMPPath + "/ConsoleApplication1.exe")
def getYearMonthDay():
    gmtime_now = time.gmtime()
    year = gmtime_now.tm_year
    year = str(year)

    month = gmtime_now.tm_mon
    month = str(month)
    if len(month) == 2:
        pass
    else:
        month = '0' + month

    day = gmtime_now.tm_mday
    day = str(day)
    if len(day) == 2:
        pass
    else:
        day = '0' + day
    return year, month, day


def getCurrPath(year, month):
    currDir = os.path.join(DATARoot, "".join([year, month]))
    if not os.path.exists(currDir):
        os.makedirs(currDir)
    return currDir


def getMonthFileNames(year, month):
    currDir = os.path.join(DATARoot, "".join([year, month]))
    allFileNames = os.listdir(currDir)
    resNames = set()
    for fileName in allFileNames:
        if "M" not in fileName:
            resNames.add(fileName[:fileName.rfind(".")])
    return resNames


def delTempFiles():
    ext = [".pl", ".sh", ".exe"]
    try:
        for root, dirs, files in os.walk(TEMPPath):
            for file in files:
                file_path = os.path.join(root, file)
                if not any(file.endswith(ending) for ending in ext):
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

