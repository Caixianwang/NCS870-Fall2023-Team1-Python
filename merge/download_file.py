import requests
from bs4 import BeautifulSoup

BASEUrl = "https://data.ris.ripe.net/rrc04"

def myTask():
    # year, month, day = utils.getYearMonthDay()
    year, month= '2023','09'
    currUrl = BASEUrl + "/" + year + "." + month
    response = requests.get(currUrl)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # print(response.text)
        links = soup.find_all('a')

        for link in links:
            link_url = link.get('href')
            if(len(link_url)==24):
                if '20230901' in link_url:
                    print(f"URL: {link_url}")
                    download(currUrl+"/"+link_url)

    else:
        print("无法获取网页内容，状态码:", response.status_code)



def download(url):
    response = requests.get(url)
    if response.status_code == 200:
        fileName = url.split('/')[-1]
        filePath = '/home/caixian/870/testMerge/20230901/' + fileName
        with open(filePath, 'wb') as file:
            file.write(response.content)
            # parseMrt.handleFile(year, month, fileName)
            # exit()


myTask()

