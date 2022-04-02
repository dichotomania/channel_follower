# -*- coding: utf-8 -*-
"""
Created on Fri Feb  4 14:13:22 2022

@author: Rechal
"""
from bs4 import BeautifulSoup
import random
from selenium import webdriver 
import time



#url = 'https://www.youtube.com/channel/UCI7ktPB6toqucpkkCiolwLg/videos'
url = "https://www.youtube.com/c/JoemanStarCraft/videos"
driver = webdriver.Chrome()
driver.get(url)
#for i in range(10):
#    time.sleep(5)
#driver.execute_script(f'window.scrollTo(0, 800)')
soup = BeautifulSoup(driver.page_source,'lxml')
videoId = soup.find_all('a',id='video-title')
counter = 0
for i in videoId:
    counter +=1
    print(counter)
    print(i["title"])
    
    # ariaList = i["aria-label"].split(" ")
    # if "小時前" in ariaList:
    #     index = ariaList.index("小時前")
    #     print(ariaList[index-1], ariaList[index])
    # elif "天前" in ariaList:
    #     index = ariaList.index("天前")
    #     print(ariaList[index-1], ariaList[index])
    # elif "週前" in ariaList:
    #     index = ariaList.index("週前")
    #     print(ariaList[index-1], ariaList[index])     
    # elif "個月前" in ariaList:
    #     index = ariaList.index("個月前")
    #     print(ariaList[index-1], ariaList[index])    
    # elif "年前" in ariaList:
    #     index = ariaList.index("年前")
    #     print(ariaList[index-1], ariaList[index])    
    #index = str(i["aria-label"]).find("前")
    #print(i["aria-label"][index-5:index+1])    
    
    print(i["href"][9:])
    print("*****************************")    

# videoImg = soup.find_all('div',id='dismissible')
# for j in videoImg:
#     counter +=1
#     k = j.find('img',id='img')
#     print(k['src'])
#     if counter > 4:
#         break



driver.close()
    