from django.conf import settings
from linebot import LineBotApi
from linebot.models import TextSendMessage, TemplateSendMessage , MessageTemplateAction, PostbackTemplateAction, CarouselTemplate, CarouselColumn
from linebotapp.models import youtuber
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
baseurl = 'https://7815-220-133-116-168.ngrok.io/static/'


def sendVideoCarousel(event):  #轉盤樣板
    try:
        message = TemplateSendMessage(
            alt_text='轉盤樣板',
            template=CarouselTemplate(
                columns= VideoCarouselColumnList(["8MG--WuNW1Y","3HsIaWuNeX0","0rp3pP2Xwhs"])
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def sendChannelCarousel(event):  #轉盤樣板
    try:
        message = TemplateSendMessage(
            alt_text='轉盤樣板',
            template=CarouselTemplate(
                columns= ChannelCarouselColumnList()
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))




def sendBack_sell(event, backdata):  #處理Postback
    try:
        message = TextSendMessage(  #傳送文字
            text = '點選的是賣 ' + backdata.get('item')
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
    


def sendBack_new(event, backdata):  #處理Postback
    try:
        channel = youtuber.objects.get(name = backdata.get('name'))
        videos = channel.video_info_set.all()
        if videos:
            CCL = []
            for item in videos:
                if len(item.name) >= 60:
                    text = item.name[:57]+"..."
                else:
                    text = item.name
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
                            data='action=sell&item=炸雞'
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


def VideoCarouselColumnList(videoList):
    CCL = []
    for video in videoList:
         CC = CarouselColumn(
             thumbnail_image_url='https://img.youtube.com/vi/'+video+'/0.jpg',
             #title='月老',
             text='韋禮安 WeiBird《如果可以 Red Scarf》MV - 電影「月老」主題曲導演親剪音樂視角版',
             actions=[
                 PostbackTemplateAction(
                     label='播放',
                     data='action=play&video=https://www.youtube.com/watch?v='+video
                 ),
                 PostbackTemplateAction(
                     label='移除',
                     data='action=sell&item=炸雞'
                     ),
                 ]
             )
         CCL.append(CC)
    return CCL
    
    
def ChannelCarouselColumnList():
    img1 = 'https://yt3.ggpht.com/tRnK3e0gymfRwbUtbdcF9Ca7YVvAvoJyD_WAwTTzkMdm8KZ1tPqqjwg0w-Ozok-kC6H3UlZp=s88-c-k-c0x00ffffff-no-rj'
    img2 = 'https://yt3.ggpht.com/ytc/AKedOLR5KDrFL0d_sUPoJgDZYcDQ6e8TO-xESARtHvTxfg=s88-c-k-c0x00ffffff-no-rj'
    CCL = [CarouselColumn(
             thumbnail_image_url=img1,
             title='韋禮安 WeiBird',
             text='123',
             actions=[
                MessageTemplateAction(
                                label='顯示清單',
                                text='@收藏清單'
                            ),
                 PostbackTemplateAction(
                     label='移除',
                     data='action=sell&item=炸雞'
                     ),
                 ]
             ),
           CarouselColumn(
             thumbnail_image_url=img2,
             title='Pan Piano',
             text='Pan Piano',
             actions=[
                MessageTemplateAction(
                                label='顯示清單',
                                text='@收藏清單'
                            ),
                 PostbackTemplateAction(
                     label='移除',
                     data='action=sell&item=炸雞'
                     ),
                 ]
             ),        
        ]
    return CCL


def searchChannel(event, keyWord):
    target = youtuber.objects.filter(name__contains = keyWord)
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
                            data='action=sell&item=炸雞'
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


  
