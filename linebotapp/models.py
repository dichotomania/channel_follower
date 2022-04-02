from django.db import models

# Create your models here.


class youtuber(models.Model):
	url = models.CharField(max_length=200, primary_key=True,default='') 
	name = models.CharField(max_length=100,null=False,default='')
	youtuber_type = models.CharField(max_length=20) 
	icon = models.CharField(max_length=200,null=False,default='')


class video_info(models.Model):
	url = models.CharField(max_length=200, primary_key=True,default='') 
	name = models.CharField(max_length=100,null=False) 
	timestamp = models.FloatField(null=False, default=0.0) 
	channel = models.ForeignKey(youtuber ,to_field ='url', on_delete=models.CASCADE, blank=True, null=True)
	icon = models.CharField(max_length=200, null=False, default='') 
    #CASCADE當主表被刪除時，子表也跟著刪除
    #PROTECT 返回錯誤提示阻止刪除
    #SET_NULL 用null代替
    #SET_DEFAULT 用default代替
    #SET()  自定義
    #to_field 設置關聯到主表的欄位，不打就是對應到ＰＫ
    #related_name 用於反向查詢（主表查詢子表）
    
    
class hot_video(models.Model):
	url = models.CharField(max_length=200, primary_key=True,default='') 
	name = models.CharField(max_length=100,null=False) 
	timestamp = models.FloatField(null=False, default=0.0) 
	icon = models.CharField(max_length=200, null=False, default='') 

    
class user_info(models.Model):
    user_id = models.CharField(max_length=100,null=False,default='', primary_key=True)         #user_id
    name = models.CharField(max_length=100,blank=True,null=False)    #儲存頻道             #儲存影片
    channel = models.ManyToManyField(youtuber, through='user_channel')
    videos = models.ManyToManyField(video_info, through='user_videos')
    class Meta:
    	db_table = "user"
    	

class user_videos(models.Model):
    user = models.ForeignKey(user_info, on_delete=models.CASCADE)
    videos = models.ForeignKey(video_info, on_delete=models.CASCADE) 


class user_channel(models.Model):
    user = models.ForeignKey(user_info, on_delete=models.CASCADE)
    channel = models.ForeignKey(youtuber, on_delete=models.CASCADE) 
