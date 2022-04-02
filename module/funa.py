#!/usr/bin/env python
from django.conf import settings

from linebot import LineBotApi
from linebot.models import TextSendMessage, TemplateSendMessage, PostbackTemplateAction, CarouselTemplate, CarouselColumn
from linebot.models import QuickReply, QuickReplyButton, MessageAction, URIAction
from linebotapp.models import video_info, hot_video
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
import time
import random


def daily_play(event):  #處理Postback
    try: 
        videos = video_info.objects.filter(timestamp__gte = (time.time()-86400))
        if videos:
            one = random.randint(0,len(videos)-1)
            if len(videos[one].name) >= 60:
                text = videos[one].name[:57]+"..."
            else:
                text = videos[one].name
            encodeName = videos[one].name.replace("&","%2g2022")   
            CC = [CarouselColumn(thumbnail_image_url=videos[one].icon,
                                         text=text,
                                         actions=[ PostbackTemplateAction(label='播放',
                                                                          data='action=play&video='+videos[one].url),
                                                  PostbackTemplateAction(label='加入我的清單',
                                                                         data='action=addVideo&name='+encodeName)
                                                  ]
                                         )
                          ]
            message = TemplateSendMessage(alt_text='每日推薦', template= CarouselTemplate(CC))  
            line_bot_api.reply_message(event.reply_token,message)
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='目前資料庫無24小時內的影片 此為隨機推播！'))
           
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生推播錯誤！'))
        
       
        
def sendQuickreply(event):  #快速選單
    try:
        message = TextSendMessage(
            text='使用指南',
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(image_url = 'https://cdn.icon-icons.com/icons2/1814/PNG/128/22map_115452.png',action=MessageAction(label='使用指南' ,  text='使用指南')),
                    QuickReplyButton(image_url = 'https://cdn.icon-icons.com/icons2/1814/PNG/128/23direction_115454.png',action=URIAction(label="可追蹤頻道列表", uri="https://dichotomania.wixsite.com/channelfollower")), 
                    QuickReplyButton(image_url = 'https://cdn.icon-icons.com/icons2/1814/PNG/128/24cocktail_115460.png',action=MessageAction(label="打賞杯咖啡", text="@我的支持是你們堅持的動力!")),                    
                    QuickReplyButton(image_url = 'https://cdn.icon-icons.com/icons2/1465/PNG/128/723email2_101014.png',action=MessageAction(label="聯絡我們", text="聯繫方式"))
                   ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))


def sendQuickreplySponsor(event):  #快速選單
    try:
        message = TextSendMessage(
            text='匯款偏好',
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=MessageAction(label="台北富邦", text="台北富邦(012)673168137413")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="中國信託", text="中國信託(822)853540307795")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="LinePay", text="LineID: rechal1991")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="PayPal", text="Paypal申請中")
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

      
def hotVideo(event):
    try: 
        #videos = hot_video.objects.filter(timestamp__gte = (time.time()-86400))
        sortVideos = hot_video.objects.order_by('-timestamp')[:5]
        videos = reversed(sortVideos) 
        if videos:
            CCL = []
            for video in videos: 
            
                if len(video.name) >= 60:
                    text = video.name[:57]+"..."
                else:
                    text = video.name
                encodeName = video.name.replace("&","%2g2022") 
                CC = CarouselColumn(thumbnail_image_url=video.icon,
                                         text=text,
                                         actions=[ PostbackTemplateAction(label='播放',
                                                                          data='action=play&video='+video.url),
                                                  PostbackTemplateAction(label='加入我的清單',
                                                                         data='action=addVideo&name='+encodeName)
                                                  ]
                                         )
                CCL.append(CC)          
            message = TemplateSendMessage(alt_text='每日推薦', template= CarouselTemplate(CCL))  
            line_bot_api.reply_message(event.reply_token,message)
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='目前資料庫無24小時內的影片 請稍後再試'))
           
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生推播錯誤！'))
    