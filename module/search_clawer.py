from bs4 import BeautifulSoup as bs
from selenium import webdriver
from urllib.parse import quote
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

def get_chrome():
    try:
        # CHROMEDRIVER_PATH ="/Users/jarvis/Desktop/chromedriver"
        CHROMEDRIVER_PATH = "./chromedriver"
        op = webdriver.ChromeOptions()
        op.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        op.add_argument("--headless") #背景執行
        op.add_argument("--disable-dev-shm-usage")
        op.add_argument("--no-sandbox")
        browser = webdriver.Chrome(CHROMEDRIVER_PATH,options=op)
        # return webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=op)
        return browser
    except:
        print("chromedriver設定錯誤")

def heroku_chrome():
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--headless") #無頭模式
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    except:
        print("chromedriver設定錯誤")
    return driver

def heroku_chrome():
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--headless") #無頭模式
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    except Exception as e:
        print(e)
        print("chromedriver設定錯誤")
    return driver

def youtube_page(keyword):
    print("爬蟲開始")
    target_url = 'https://www.youtube.com/results?search_query={}'.format(quote(keyword))
    browser = heroku_chrome()
    browser.get(target_url)
    # time.sleep(3)
    WebDriverWait(browser,10).until(EC.visibility_of_any_elements_located((By.ID,"video-title")))
    soup = bs(browser.page_source, "html.parser")
    browser.close()

    channelId = []
    channelName = []
    titles = []
    urls = []
    pics = []
    shortVideoIds = []
    result = []

    counter = 0
    soupfilter = soup.find_all("a", "yt-simple-endpoint style-scope yt-formatted-string" )
    for channel in soupfilter:
        if counter > 4:
            break
        channelId.append(channel['href'].split("/")[2])
        channelName.append(channel.text)
        counter+=1

    counter = 0
    soupfilter = soup.find_all("a",id="video-title")
    for data in soupfilter:
        if counter > 4:
            break
        urls.append('https://www.youtube.com{}'.format(data['href']))
        shortVideoIds.append(data['href'].lstrip("/watch?v="))
        titles.append(data['title'])
        pics.append(('https://i.ytimg.com/vi/{}/0.jpg'.format(data['href'][9:])))
        counter+=1

    for i in range(len(urls)):
        result.append({"url": urls[i] , "shortVideoId": shortVideoIds[i] , "title": titles[i] , "pic": pics[i] , "channelName": channelName[i], "channelId": channelId[i] })
    return result
if __name__=="__main__":
    res = (youtube_page("panpiano"))
    for i in range(len(res)):
        print(res[i]['shortVideoId'])
        print(res[i]['url'])
        print(res[i]['title'])
        print(res[i]['pic'])
        print(res[i]['channelName'])
        print(res[i]['channelId'])
    pass
 
