from django.conf import settings
from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebotapp.models import user_info, user_videos, video_info
import time

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
        
def sendBack_storeVideo(event, backdata):  #處理Postback
        decodeName = backdata.get('name').replace("%2g2022","&") 

        check = user_videos.objects.filter(user = event.source.user_id)
        if len(check) < 10:
            singleV = video_info.objects.filter(url = backdata.get('videourl'))
            user = user_info.objects.get(user_id = event.source.user_id)
            if singleV:
                if user_videos.objects.filter(videos = singleV[0], user = user):
                    print("影片已在收藏清單")
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text='影片已在收藏清單!'))
                else:
                    user_videos.objects.create(user=user, videos=singleV[0]) 
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text='添加成功!'))
            else:
                video_info.objects.create(url = backdata.get('videourl'),name = decodeName,timestamp = time.time(),icon = backdata.get('videoicon'))   
                singleV = video_info.objects.get(url = backdata.get('videourl'))
                user_videos.objects.create(user=user, videos=singleV)                    
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text='添加成功!'))                
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='清單最多只能存放10個影片喔'))

           

    