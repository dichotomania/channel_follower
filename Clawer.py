# -*- coding: utf-8 -*-
"""
Created on Fri Feb  4 14:13:22 2022

@author: Rechal
"""
from selenium import webdriver 
import time,re
import  pandas as pd
import psycopg2
from bs4 import BeautifulSoup as bs
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def get_chrome(type_):
    try:
        op = webdriver.ChromeOptions()
        op.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        op.add_argument("--headless") #背景執行
        op.add_argument("--disable-dev-shm-usage")
        op.add_argument("--no-sandbox")
        op.add_argument("--lang=zh-TW")
        if type_ == "local":
            CHROMEDRIVER_PATH ="./chromedriver"
            browser = webdriver.Chrome(CHROMEDRIVER_PATH,options=op)
        elif type_ == "heroku":
            browser = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=op)
        return browser
    except:
        print("chromedriver設定錯誤")


def creatConn():
    conn=psycopg2.connect(host='ec2-3-209-61-239.compute-1.amazonaws.com',
                      user='vzkhdlccezxnep',
                      dbname='d4crf41rmge8ds',
                      password='637dfcb124c91f2e45e56035d6147d01f7e7c710bcebd84e26491873642c4c4d',
                      sslmode='allow'    )
    conn.autocommit = True 
    return conn


def single_insert(conn, insert_req):
    """ Execute a single INSERT request """
    cursor = conn.cursor()
    try:
        cursor.execute(insert_req)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cursor.close()
        return 1
    cursor.close()


def single_select(conn, select_req):
    """ Execute a single INSERT request """
    cursor = conn.cursor()
    try:
        cursor.execute(select_req)
        data = cursor.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cursor.close()
        return 1
    cursor.close()
    return data 


def getCIcon():
    df =  pd.read_csv("./yt百萬頻道.csv", encoding = "utf8")
    df["網址"] = df["網址"] + "/videos" 
    list_all = df["網址"]
    imgList = []
    driver = webdriver.Chrome()
    for url in list_all :
        driver.get(url)
        time.sleep(2)
        soup = bs(driver.page_source,'lxml')
        findimg  = soup.find('link',{'href':re.compile('https://yt3.ggpht.com')})
        print(findimg['href'])
        imgList.append(findimg['href'])
    driver.close()    
    df["icon"] = imgList
    df.to_csv("channelData.csv")


def creatYoutubeTable():
    df =  pd.read_csv("./channelData.csv", encoding = "utf8")    
    df['頻道名'] = df['頻道名'].str.replace("'","\\'")
    dfLen = len(df)
    conn = creatConn()
    for i in range(dfLen):
        query = """
            INSERT into linebotapp_youtuber(url, name, youtuber_type, icon) values('%s', E'%s', '%s', '%s')
            """ % (df["網址"][i], df["頻道名"][i], df["類別"][i], df["icon"][i])
        single_insert(conn, query)
    conn.close()


def getVideoInf():    
    df =  pd.read_csv("./channelData.csv", encoding = "utf8")
    list_all = df["網址"]      
    linebotapp_video_info=[]
    driver = get_chrome("heroku")  
    for cUrl in list_all :
        print(str(cUrl)) 
        driver.get(cUrl)
        WebDriverWait(driver,10).until(EC.visibility_of_any_elements_located((By.ID,"video-title")))
        soup = bs(driver.page_source,'html.parser')
        videoId = soup.find_all('a',id='video-title')[:10]
        videoId.reverse()
        print(videoId)

        for i in videoId:
            videoliist=[]
            
            #影片網址 
            vUrl = 'https://www.youtube.com/watch?v='+i["href"][9:]
            print(vUrl)
            videoliist.append(vUrl)
              
            #標題(需取出來整理特殊符號)
            print(i["title"])
            videoliist.append(i['title'])
            
            # 更新時間(需修改成時間挫劑)
            
            currentTime = time.time()
            print(currentTime)
            videoliist.append(currentTime)
            videoliist.append(cUrl)
            
            #影片圖片網址
            pic = f"https://img.youtube.com/vi/{i['href'][9:]}/0.jpg"
            videoliist.append(pic)
            print("*****************************")
            linebotapp_video_info.append(videoliist)
            
    driver.close()
    df = pd.DataFrame(linebotapp_video_info)
    df[1]  = df[1].str.replace("'","\\'")
    df = df.iloc[::-1]
    return df


def creatVideoTable(df):
    conn = creatConn()
    for i in range(len(df)):
        
        queryExist = f"""
            SELECT * FROM linebotapp_video_info WHERE url = '{df[0][i]}' AND channel_id IS NULL
        """
        data = single_select(conn, queryExist)

        if data:
            print(data)

            queryExist2 = f"""
                SELECT * FROM linebotapp_user_videos WHERE videos_id = '{df[0][i]}' 
            """
            data2 = single_select(conn, queryExist2)                        
        
            queryDelete = f"""
                DELETE FROM linebotapp_user_videos WHERE videos_id = '{df[0][i]}'
                """
            single_insert(conn, queryDelete)

            queryDelete2 = f"""
                DELETE FROM linebotapp_video_info WHERE url = '{df[0][i]}' AND channel_id IS NULL
                """
            single_insert(conn, queryDelete2)                
                
            query = f"""
                INSERT into linebotapp_video_info(url, name, timestamp, icon, channel_id) values('{df[0][i]}', \
                E'{df[1][i]}', {df[2][i]}, '{df[4][i]}', '{df[3][i]}')""" 
            single_insert(conn, query)           
            
            for d2 in data2:
                query2 = f"""
                    INSERT into linebotapp_user_videos(user_id, videos_id) values('{d2[1]}', '{d2[2]}')""" 
                single_insert(conn, query2)                
            
            
        else:
            query = f"""
                INSERT into linebotapp_video_info(url, name, timestamp, icon, channel_id) values('{df[0][i]}', \
                E'{df[1][i]}', {df[2][i]}, '{df[4][i]}', '{df[3][i]}')""" 
            single_insert(conn, query)
    conn.close()    
    
    
def createHotData():
    target_url = 'https://www.youtube.com/feed/trending?gl=TW&hl=zh-TW'
    browser = get_chrome("heroku")
    browser.get(target_url)
    WebDriverWait(browser,10).until(EC.visibility_of_any_elements_located((By.ID,"video-title")))
    soup = bs(browser.page_source, "html.parser")
    browser.close()

    counter2 = 0
    pics = []
    titles = []
    urls = []
    shortVideoIds = []
    #result = []
    vtitle = soup.find_all("a",id="video-title")
    for data in vtitle:
        if counter2 > 4:
            break
        urls.append(f"https://www.youtube.com{(data['href'])}")
        shortVideoIds.append(data['href'].lstrip("/watch?v="))
        titles.append(data['title'].replace("'","\\'"))
        pics.append(f"https://i.ytimg.com/vi/{(data['href'][9:])}/0.jpg")
        counter2+=1
    lens = len(urls) 
    conn = creatConn()
    
    for i in range(lens):
        currentTime = time.time()
        query = f"""
        INSERT into linebotapp_hot_video(url, name, timestamp, icon) values('{urls[i]}', \
             E'{titles[i]}', {currentTime}, '{pics[i]}') """ 
        single_insert(conn, query)
    
    conn.close()     
    
    

if __name__ == '__main__':
    #creatYoutubeTable()
    #df = getVideoInf()
    #creatVideoTable(df)
    createHotData()
