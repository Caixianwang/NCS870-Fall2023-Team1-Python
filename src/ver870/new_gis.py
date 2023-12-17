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


def getIpLngLat():
    ipLngLats = []
    filename = "src/ver870/ip2pos.csv"
    with open(filename, 'r') as file:
        for line in file:
            dar = line.strip().split(',')
            ipLngLats.append(dar)
    return ipLngLats
def getLngLat(ip,ipLngLats):
    for ipLngLat in ipLngLats:
        if ipLngLat[0]==ip:
            return ipLngLat[1],ipLngLat[2]
    return -1
def parseIP(file_path):

    ipLngLats = getIpLngLat()
    fromLine = ''
    toLine = ''
    both = False
    LngAndLats = []
    count = 0
    repeatSet = set()
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('FROM:'):
                fromLine = line[6:].strip()
            if line.startswith('TO:'):
                toLine = line[4:].strip()
                both = True
            if both:
                both = False
                joinLine = fromLine+toLine

                if joinLine not in repeatSet:
                    repeatSet.add(joinLine)
                    fromLngLat = getLngLat(fromLine,ipLngLats)
                    toLngLat = getLngLat(toLine,ipLngLats)
                    if fromLngLat!=-1 and toLngLat!=-1:
                        fromPos = {'lng': fromLngLat[0], 'lat': fromLngLat[1]}
                        toPos = {'lng': toLngLat[0], 'lat': toLngLat[1]}
                        LngAndLats.append([fromPos,toPos])

                        count +=1
                        if count == 5000:
                            break;



    # print(len(LngAndLats))
    jsonReq = {'gis':LngAndLats}
    new_utils.pushOutput(jsonReq)

# parseIP('E:/project870/20230901.0000M.txt')





