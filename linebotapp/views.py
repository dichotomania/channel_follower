from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, PostbackEvent, FollowEvent, TextSendMessage
from module import func, funa
from urllib.parse import parse_qsl
import re
from linebotapp.models import user_info
from module.storeVideo import sendBack_storeVideo


line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                if isinstance(event.message, TextMessage):
                    mtext = event.message.text
                    if mtext == '@我的追蹤': #我的追蹤頻道
                        func.sendChannelCarousel(event)
    
                    elif mtext == '@每日推薦': #ramdon 
                        funa.daily_play(event)
    
                    elif mtext == '@收藏清單': #我的影片清單
                        func.sendVideoCarousel(event)
    
                    elif mtext == '@使用指南' or mtext == '@help': #help
                        funa.sendQuickreply(event)
    
                    elif mtext == '@我的支持是你們堅持的動力!':
                        funa.sendQuickreplySponsor(event)

                    elif mtext == '@今日熱門':
                        funa.hotVideo(event)

                    elif re.search(r"^:",mtext) or re.search(r"^：",mtext):
                        try:
                            func.searchChannel(event, mtext[1:])#未完成
                        
                        except:    
                            line_bot_api.reply_message(event.reply_token,TextSendMessage(text= "此頻道並無提供追蹤功能"))
                    elif re.search(r"^!",mtext) or re.search(r"^！",mtext):
                        try:
                            func.searchVideo(event, mtext[1:])#未完成
                        except:    
                            line_bot_api.reply_message(event.reply_token,TextSendMessage(text= "哎呀 出錯了！"))
                            
                                                
            if isinstance(event, PostbackEvent):  #PostbackTemplateAction觸發此事件
                backdata = dict(parse_qsl(event.postback.data))  #取得Postback資料
                if backdata.get('action') == 'play':
                    func.sendBack_play(event, backdata)
                elif backdata.get('action') == 'new':
                    func.sendBack_new(event, backdata)
                elif backdata.get('action') == 'addChannel':
                    func.sendBack_addChannel(event, backdata)
                elif backdata.get('action') == 'delChannel':
                    func.sendBack_delChannel(event, backdata)
                elif backdata.get('action') == 'addVideo':
                    func.sendBack_addVideo(event, backdata)
                elif backdata.get('action') == 'delVideo':
                    func.sendBack_delVideo(event, backdata)
                elif backdata.get('action') == 'storeVideo':
                    sendBack_storeVideo(event, backdata)


            if isinstance(event, FollowEvent):  #加入時收集ID寫進資料庫
                user_id = event.source.user_id
                user_name = line_bot_api.get_profile(user_id).display_name                 
                try:
                    line_bot_api.reply_message(event.reply_token,TextSendMessage(text= user_name+" 歡迎使用!"))
                    user_info.objects.create(user_id=user_id, name=user_name) 
                    
                except Exception as e:
                    print(e)
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
