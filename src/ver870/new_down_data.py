import requests
from bs4 import BeautifulSoup
import schedule
import time
import sys


# Import customized libraries
import new_utils
import new_parse_mrt
import new_real_time
import new_topology
import new_gis

BASEUrl = "https://data.ris.ripe.net/rrc04"


def myTask():
    year, month, day = new_utils.getYearMonthDay()
    currPath = new_utils.getCurrPath(year, month)

    currUrl = BASEUrl + "/" + year + "." + month
    response = requests.get(currUrl)
    # Check whether the request is successful
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # print(response.text)
        fileNames = new_utils.getMonthFileNames(year, month)
        links = soup.find_all('a')
        # Traverse the text and URL of all links
        for link in links:
            link_url = link.get('href')
            if (len(link_url) == 24):
                findex = link_url.find(".")  #
                lindex = link_url.rfind(".")  #
                substr = link_url[findex + 1:lindex]
                if substr not in fileNames:
                    # print(f"URL: {link_url}")
                    download(year, month, currUrl + "/" + link_url)

    else:
        print("Unable to get page content, status code:", response.status_code)


def download(year, month, url):
    response = requests.get(url)
    if response.status_code == 200:
        new_utils.delTempFiles()
        fileName = url.split('/')[-1]
        filePath = new_utils.TEMPPath + "/" + fileName

        with open(filePath, 'wb') as file:
            file.write(response.content)
            file1, file2 = new_parse_mrt.handleFile(year, month, fileName)
            # print(file1,file2)
            new_real_time.real_defense(file1)
            new_topology.topo_calc(file2)
            new_gis.parseIP(file2)
            # exit()


def grap_main():
    new_utils.initEnv()
    myTask()
    # Set a scheduled task to be executed periodically
    schedule.every(5).minutes.do(myTask)  #
    #
    while True:
        schedule.run_pending()
        time.sleep(5)  # Adjust sleep time appropriately to reduce CPU load
