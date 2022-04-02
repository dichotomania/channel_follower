from django.conf import settings
from linebot import LineBotApi
from linebot.models import TextSendMessage, TemplateSendMessage, PostbackTemplateAction, CarouselTemplate, CarouselColumn
from linebotapp.models import user_videos, user_channel, youtuber, user_info, video_info
from module.search_clawer import youtube_page


line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
#baseurl = 'https://7e77-61-220-44-217.ngrok.io//static/'


def makeTSM(user, CCLtype):
    if CCLtype:
        message = TemplateSendMessage(
            alt_text='轉盤樣板',
            template=CarouselTemplate(
            columns= VideoCarouselColumnList(user)
            )
        )  
    else:
        message = TemplateSendMessage(
            alt_text='轉盤樣板',
            template=CarouselTemplate(
            columns= ChannelCarouselColumnList(user)
            )
        )         
    return message


def checkLenth(name):               
    if len(name) >= 60:
        text = name[:57]+"..."
    else:
        text = name
    encodeName = name.replace("&","%2g2022")   
    return (text, encodeName)


def sendVideoCarousel(event):  #轉盤樣板
    try:
        user = user_videos.objects.filter(user = event.source.user_id)     
        if user:
            message = makeTSM(user, 1)
            line_bot_api.reply_message(event.reply_token,message)
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='您並無收藏任何影片喔!'))
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))


def sendChannelCarousel(event):  #轉盤樣板
    #try:
        user = user_channel.objects.filter(user = event.source.user_id)
        if user:
            message = makeTSM(user, 0)
            line_bot_api.reply_message(event.reply_token,message)
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='您並無追蹤任何頻道喔!'))
    #except:
    #    line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))


def sendBack_new(event, backdata):  #處理Postback
    try:
        channel = youtuber.objects.get(name = backdata.get('name'))
        videos = channel.video_info_set.all().order_by('-timestamp')[:10]# bug1: 沒限制影片數量
        if videos:
            CCL = []
            for item in videos:
                text, encodeName = checkLenth(item.name)   
                columns = CarouselColumn(
                    thumbnail_image_url = item.icon,
                    title = backdata.get('name'),
                    text = text,
                    actions=[
                        PostbackTemplateAction(
                            label='播放',
                            data='action=play&video='+item.url
                        ),
                        PostbackTemplateAction(
                            label='加入我的清單',
                            data="action=addVideo&name="+encodeName
                        )
                    ]
                )     
                CCL.append(columns)
            message = TemplateSendMessage(
                alt_text='轉盤樣板',
                template= CarouselTemplate(CCL)
            )  
            line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
        
        
def sendBack_play(event, backdata):  #處理Postback
    try:
        message = TextSendMessage(  #傳送文字
            text = backdata.get('video')
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
        
        
def sendBack_addChannel(event, backdata):  #處理Postback
    try:
        check = user_channel.objects.filter(user = event.source.user_id)
        if len(check) < 3 :
            channel = youtuber.objects.get(name = backdata.get('item'))
            if user_channel.objects.filter(user__exact = event.source.user_id, channel__exact = channel) :
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text='已經追蹤過該頻道喔~'))
            else:
                user = user_info.objects.get(user_id = event.source.user_id)#             
                user_channel.objects.create(user=user, channel=channel)
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text='追蹤成功!你可以用下方「我的追蹤」刪除已追蹤頻道~'))
        else:
             line_bot_api.reply_message(event.reply_token, TextSendMessage(text='最多只能追蹤3個頻道喔~'))           
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))      
        

def sendBack_delChannel(event, backdata):  #處理Postback
    try:
        url = youtuber.objects.get(name = backdata.get("name"))
        target = user_channel.objects.filter(user = event.source.user_id, channel_id = url.url)
        target[0].delete()  
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='移除成功!'))
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))


def sendBack_addVideo(event, backdata):  #處理Postback
    try:
        check = user_videos.objects.filter(user = event.source.user_id)
        decodeName = backdata.get('name').replace("%2g2022","&")  
        if len(check) < 10:   
            video = video_info.objects.get(name = decodeName)
            if user_videos.objects.filter(user__exact = event.source.user_id , videos__exact = video) :
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text='已經追蹤過此影片喔~'))
            else:
                user = user_info.objects.get(user_id = event.source.user_id)
                user_videos.objects.create(user=user, videos = video)
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text='影片已加入收藏清單~'))           
        else:
             line_bot_api.reply_message(event.reply_token, TextSendMessage(text='清單最多只能存放10個影片喔'))
           
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))        
        

def sendBack_delVideo(event, backdata):  #處理Postback
    try:
        decodeName = backdata.get('name').replace("%2g2022","&")  
        url = video_info.objects.get(name = decodeName)
        target = user_videos.objects.filter(user = event.source.user_id, videos_id = url.url)
        target[0].delete()  
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='移除成功!'))
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))


def VideoCarouselColumnList(user):
    CCL = []
    
    for item in user:
        videos = video_info.objects.get(url = item.videos_id)
        text, encodeName = checkLenth(videos.name)    
        CC = CarouselColumn(
            thumbnail_image_url=videos.icon,
            text=text,
            actions=[
                PostbackTemplateAction(
                    label='播放',
                    data='action=play&video='+videos.url
                ),
                PostbackTemplateAction(
                    label='移除',
                    data='action=delVideo&name='+encodeName
                    ),
                ]
            )
        CCL.append(CC)
    return CCL
    
    
def ChannelCarouselColumnList(user):
    CCL = []
    for item in user:
        channel = youtuber.objects.get(url = item.channel_id)
        CC = CarouselColumn(
                  thumbnail_image_url=channel.icon,
                  title=channel.name,
                  text="類別: "+ channel.youtuber_type,
                  actions=[
                      PostbackTemplateAction(
                            label='最新影片',
                            data='action=new&name='+channel.name
                        ),
                      PostbackTemplateAction(
                          label='移除',
                          data='action=delChannel&name='+channel.name
                          ),
                      ]
                  )
        CCL.append(CC)            
    return CCL


def searchChannel(event, keyWord):
    target = youtuber.objects.filter(name__icontains = keyWord)
    if target:
        CCL = []
        for item in target:
            columns = CarouselColumn(
                    thumbnail_image_url=item.icon,
                    title=item.name,
                    text= "類別: "+ item.youtuber_type,
                    actions=[
                        PostbackTemplateAction(
                            label='最新影片',
                            data='action=new&name='+item.name
                        ),
                        PostbackTemplateAction(
                            label='加入追蹤',
                            data='action=addChannel&item='+item.name
                        ),
                    ]
                )     
            CCL.append(columns)
        message = TemplateSendMessage(
            alt_text='轉盤樣板',
            template= CarouselTemplate(CCL)
            )
        line_bot_api.reply_message(event.reply_token,message)
    else:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='查無此頻道'))


def searchVideo(event, keyWord):
    searchresult = youtube_page(keyWord)
    print("爬蟲完成,已取回資料")
    CCL = []
    for item in searchresult:
        text, encodeName = checkLenth(item['title']) 
        videourl=item['url']
        videoicon=item["pic"]

        columns = CarouselColumn(
                thumbnail_image_url=videoicon,
                text=text,
                actions=[
                    PostbackTemplateAction(
                        label='播放',
                        data= 'action=play&video='+videourl
                        ),
                    PostbackTemplateAction(
                        label='加入我的清單',
                        data= f'action=storeVideo&name={encodeName}&videourl={videourl}&videoicon={videoicon}'
                        )
                ]
            )
        CCL.append(columns)
    
    message = TemplateSendMessage(
        alt_text='轉盤樣板',
        template= CarouselTemplate(CCL)
    )

    line_bot_api.reply_message(event.reply_token,message)
  
    


    
    
    
  
