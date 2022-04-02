# -*- coding: utf-8 -*-
"""
Created on Fri Feb  4 14:13:22 2022

@author: Rechal
"""
from bs4 import BeautifulSoup
from selenium import webdriver 
import time,re
import  pandas as PD

list_all = [
# 'https://www.youtube.com/channel/UCHm9SiOLG8UoBT8STWY5mVA/videos',\
# 'https://www.youtube.com/channel/UCTQ-gSOpuLtgQarXw3XVmyQ/videos',\
# 'https://www.youtube.com/channel/UCXpxKdZAiyUEaTkoCPpEZzg/videos',\
# 'https://www.youtube.com/channel/UCA2qvunXtkK3SUVxfOGiobA/videos',\
# 'https://www.youtube.com/channel/UC6FcYHEm7SO1jpu5TKjNXEA/videos',\
# 'https://www.youtube.com/channel/UCTMt7iMWa7jy0fNXIktwyLA/videos',\
# 'https://www.youtube.com/channel/UCPcF3KTqhD67ADkukx_OeDg/videos',\
# 'https://www.youtube.com/channel/UCI7ktPB6toqucpkkCiolwLg/videos',\
# 'https://www.youtube.com/channel/UCX9VHpN62jkqCCntHxymPOA/videos',\
# 'https://www.youtube.com/channel/UCrLO-yoAu4ZTzRSdmWqS53A/videos',\
# 'https://www.youtube.com/user/babybus1000/featured/videos',\
# 'https://www.youtube.com/c/charlie615119/videos',\
# 'https://www.youtube.com/channel/UC5l1Yto5oOIgRXlI4p4VKbw/videos',\
# 'https://www.youtube.com/c/RayDuEnglish/videos',\
# 'https://www.youtube.com/channel/UC77tdTDovSm70lFOkn9398Q/videos',\
# 'https://www.youtube.com/user/binmusictaipei/videos',\
# 'https://www.youtube.com/c/MashaBearCH/videos',\
# 'https://www.youtube.com/c/ettvCTime/videos',\
# 'https://www.youtube.com/c/%E8%94%A1%E9%98%BF%E5%98%8ELife/videos',\
'https://www.youtube.com/c/jaychou/videos/videos',\
'https://www.youtube.com/c/JoemanStarCraft/videos',\
'https://www.youtube.com/c/%E6%9C%A8%E6%9B%9C4%E8%B6%85%E7%8E%A9/videos',\
'https://www.youtube.com/channel/UC3LBFXbWtEBdOOUb8-qJm9Q/videos',\
'https://www.youtube.com/c/RusPiano/videos',\
'https://www.youtube.com/c/HuashiRomance/videos',\
'https://www.youtube.com/c/amogood/videos',\
'https://www.youtube.com/channel/UCIU8ha-NHmLjtUwU7dFiXUA/videos',\
'https://www.youtube.com/c/TVBSNEWS01/videos',\
'https://www.youtube.com/c/%E9%BB%83%E6%B0%8F%E5%85%84%E5%BC%9F/videos',\
'https://www.youtube.com/c/DEJunMix/videos',\
'https://www.youtube.com/c/LinfairRecords/videos',\
'https://www.youtube.com/c/Chienseating/videos',\
'https://www.youtube.com/c/newsebc/videos',\
'https://www.youtube.com/c/%E4%B8%AD%E5%A4%A9%E6%96%B0%E8%81%9ECH52/videos',\
'https://www.youtube.com/c/LucasandKibo/videos',\
'https://www.youtube.com/user/KEVIN0204660/videos',\
'https://www.youtube.com/c/warnertaiwan/videos',\
'https://www.youtube.com/c/%E8%94%A1%E9%98%BF%E5%98%8ELife/videos',\
'https://www.youtube.com/c/%E7%99%BD%E7%99%A1%E5%85%AC%E4%B8%BB/videos',\
'https://www.youtube.com/c/%E7%B6%9C%E8%97%9D%E7%8E%A9%E5%BE%88%E5%A4%A7MrPlayer/featured/videos',\
'https://www.youtube.com/user/HIMservice/videos',\
'https://www.youtube.com/c/masaabc1/videos',\
'https://www.youtube.com/c/chuchushoeTW/videos',\
'https://www.youtube.com/c/TaiwanTalentShow/videos',\
'https://www.youtube.com/channel/UCgdwtyqBunlRb-i-7PnCssQ/videos',\
'https://www.youtube.com/c/STRNetworkasia/videos',\
'https://www.youtube.com/c/%E4%BA%AE%E7%94%9F%E6%B4%BBBrightSide/videos',\
'https://www.youtube.com/c/TerryFilms2019/videos',\
'https://www.youtube.com/c/SanyuanJAPAN2015/videos',\
'https://www.youtube.com/c/anjouclever103/videos',\
'https://www.youtube.com/channel/UCnfPDcASesYjcO5u-ELnb-Q/videos',\
'https://www.youtube.com/channel/UCGpNjY0Xq2GJLXh4OOX1LOA/videos',\
'https://www.youtube.com/user/jasonjason1124/videos',\
'https://www.youtube.com/c/yoyotvebc/videos',\
'https://www.youtube.com/channel/UC24h-JBUHXT5HXIK_9cWOmQ/videos',\
'https://www.youtube.com/c/%E4%BA%BA%E7%94%9F%E8%82%A5%E5%AE%85x%E5%B0%8A/videos',\
'https://www.youtube.com/user/13foreverandever/videos',\
'https://www.youtube.com/c/FTVDRAMA/videos',\
'https://www.youtube.com/channel/UCIdhd_1spj49unBWx1fjS2A/videos',\
'https://www.youtube.com/c/%E5%A2%A8%E9%8F%A1%E5%93%A5%E5%AF%A6%E6%B3%81TV/videos',\
'https://www.youtube.com/channel/UCcb9uxCoIgw7RQjQnlgd0Xw/videos',\
'https://www.youtube.com/user/d59025/videos',\
'https://www.youtube.com/c/%E6%90%9E%E7%A5%9E%E9%A6%AC/videos',\
'https://www.youtube.com/user/louislee0602/videos',\
'https://www.youtube.com/c/andchinablue500walkerdad/videos',\
'https://www.youtube.com/c/RSPannie72127/videos',\
'https://www.youtube.com/channel/UCzxN4G3s9uR9ao5_O5DoXmA/videos',\
'https://www.youtube.com/c/ZyNXyZ/videos',\
'https://www.youtube.com/user/SETShowBiz/videos',\
'https://www.youtube.com/user/TheLiuPei/videos',\
'https://www.youtube.com/c/LukeMartin/videos',\
'https://www.youtube.com/c/%E4%B8%AD%E6%99%82%E6%96%B0%E8%81%9E%E7%B6%B2/videos',\
'https://www.youtube.com/c/%E6%88%91%E6%84%9B%E5%A4%A7%E7%86%B1%E9%96%80/videos',\
'https://www.youtube.com/c/Kusdream%E9%85%B7%E7%9A%84%E5%A4%A2/videos',\
'https://www.youtube.com/c/liketaitai/videos',\
'https://www.youtube.com/channel/UCTqPBBnP2T57kmiPQ87986g/videos',\
'https://www.youtube.com/c/oeurxhichocolate/videos',\
'https://www.youtube.com/channel/UC8zkK0-g8S8Z_t8ZjUmpAlA/videos',\
'https://www.youtube.com/c/%E9%A4%A8%E9%95%B7%E6%88%90%E5%90%89%E6%80%9D%E6%B1%97/videos',\
'https://www.youtube.com/channel/UCZVCbj9weVNAWqXS9gnfm5A/videos',\
'https://www.youtube.com/channel/UCAfcy122TZHqDQMMAwfbvBQ/videos',\
'https://www.youtube.com/c/ggukim/videos',\
'https://www.youtube.com/c/EBCbuzz/videos',\
'https://www.youtube.com/c/%E5%B0%91%E5%BA%B7%E6%88%B0%E6%83%85%E5%AE%A4/videos',\
'https://www.youtube.com/user/NGCTaiwan/videos',\
'https://www.youtube.com/c/%E6%88%91%E6%84%9B%E5%BA%B7%E7%86%99/videos',\
'https://www.youtube.com/channel/UCOf3OYchR7r7FjkIhD949rA/videos',\
'https://www.youtube.com/c/NyoNyoTV/videos',\
'https://www.youtube.com/c/papayaclass/videos',\
'https://www.youtube.com/channel/UC_dXxZgHNpNVElF6y4P10Rw/videos',\
'https://www.youtube.com/c/HelloCatie/videos',\
'https://www.youtube.com/user/TWnineoneone911/videos',\
'https://www.youtube.com/user/MrChesterccj/videos',\
'https://www.youtube.com/c/dan201/videos',\
'https://www.youtube.com/c/VSMediatw/videos',\
'https://www.youtube.com/c/counter656/videos',\
'https://www.youtube.com/c/TaiwanBar/videos',\
'https://www.youtube.com/user/Stopkiddinstudio/videos',\
'https://www.youtube.com/c/%E5%81%A5%E5%BA%B720health20/featured/videos',\
'https://www.youtube.com/c/%E5%90%AB%E7%BE%9E%E8%8D%89MIMOSAGO/videos',\
'https://www.youtube.com/channel/UCw2W7GIqJNB-UMUxncnMuiw/videos']

linebotapp_video_info=[]
    
for url in list_all :
    print(str(url)) 
       
    driver = webdriver.Chrome()
    driver.get(url)
    
    time.sleep(2)
    # driver.execute_script(f'window.scrollTo(0, 400)')
    
    
    soup = BeautifulSoup(driver.page_source,'lxml')
    videoId = soup.find_all('a',id='video-title')
    counter = 0
    
    findimg  = soup.find('link',{'href':re.compile('https://yt3.ggpht.com')})
    print(findimg['href'])
    
    

    for i in videoId:
        videoliist=[]
        counter +=1
        print(counter)
        
        #影片網址 
        YT = 'https://www.youtube.com/watch?v='
        short =i["href"][9:]
        print(YT + str(short))
        videoliist.append(i["href"][9:])
          
        #標題(需取出來整理特殊符號)
        print(i["title"])
        videoliist.append(i['title'])
        
        # 更新時間(需修改成時間挫劑)
        
        Published =soup.find_all('span',class_="style-scope ytd-grid-video-renderer")[counter*2-1].text
        print(Published)
        videoliist.append(Published)
        videoliist.append(url)
        print("*****************************")
        
        linebotapp_video_info.append(videoliist)
        
        if counter == 10 :      
            break 
       
    
    driver.close()
print("linebotapp_video_info")
print(linebotapp_video_info)
print("----"*10)

df = PD.DataFrame(linebotapp_video_info)
# print(type(df[2][i]))
# print(df[2][i])
#%%
import psycopg2
from sqlalchemy import create_engine

##求大神幫看方法一
'''
def using_alchemy(df):
    try:
        engine = create_engine("postgresql+psycopg2://cvyycoqolturzq:3d2686d07472f4f90309cfd61672c663195b7eb176cc848da37c6dab2c7d1731@ec2-44-194-113-156.compute-1.amazonaws.com/d7rqrbot9jdphg")
        df.to_sql('test', con=engine, index=False, if_exists='append',chunksize = 1000)
        print("Data inserted using to_sql()(sqlalchemy) done successfully...")
        
    except (Exception, psycopg2.DatabaseError) as err:
        print('err')
        
using_alchemy(df_video_info)
'''
# df.to_sql('table_name', engine)#


##方法二也有問題  說表已經存在但我刷新沒有 剛剛還沒問題 ??

conn=psycopg2.connect(host='ec2-44-194-113-156.compute-1.amazonaws.com',
                      user='cvyycoqolturzq',
                      dbname='d7rqrbot9jdphg',
                      password='3d2686d07472f4f90309cfd61672c663195b7eb176cc848da37c6dab2c7d1731',
                      sslmode='allow'    )

conn.autocommit = True  #就不用寫 commit 囉con.set_session(autocommit=True)
cursor = conn.cursor()
cursor.execute("DROP TABLE IF EXISTS xxx")
cursor.execute("CREATE TABLE xxx (id VARCHAR(50) PRIMARY KEY, name VARCHAR(100), ids VARCHAR(10), url VARCHAR(250))")
# print("Finished creating table")

def single_insert(conn, insert_req):
    """ Execute a single INSERT request """
    cursor = conn.cursor()
    try:
        cursor.execute( insert_req )
        conn.commit()
        print("insert complete")
        
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cursor.close()
        return 1
    cursor.close()
    
num=1    
for i in range(820):
    query = """
    INSERT into zzz(id, name, ids, url) values('%s','%s','%s','%s')
    """ % (df[0][i],df[1][i], df[2][i], df[3][i])
    
    print(num)
    print("")
    print(df[0][i],df[1][i], df[2][i], df[3][i])
    single_insert(conn, query)

    num+=1    
    

conn.close()


print("totally complepte")