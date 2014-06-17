# -*- coding: utf-8 -*-
'''
Created on Aug 30, 2013

@author: jin
model Notify 消息表
'''
from django.db import models
from django.contrib.auth.models import User
from apps.upload_avatar.app_settings import SYSTEM_DEFAULT_IMAGE_NAME

class Notify(models.Model):
    sender=models.ForeignKey(User,related_name="from",verbose_name=u'发信人')
    receiver=models.ForeignKey(User,related_name="receive",verbose_name=u'收信人',null=True,blank=True,)
    TYPE_CHOICE=(('0','系统消息'),('1','系统邮件'),)
    type=models.CharField(verbose_name="发送方式",max_length=2,choices=TYPE_CHOICE,null=True,default='1')
    title=models.CharField(verbose_name="标题",max_length=128,null=True,)
    content=models.TextField(verbose_name="内容")
    sendTime=models.DateTimeField(verbose_name="发出时间")
    isRead=models.NullBooleanField(verbose_name="是否阅读")
    
    '''
    '''
    def get_avatar_name(self,userId):
        from apps.user_app.models import UserProfile
        userProfile=UserProfile.objects.get(user_id=userId)
        if userProfile.avatar_name_status=='3':
            return userProfile.avatar_name
        else:
            from apps.upload_avatar.app_settings import DEFAULT_IMAGE_NAME
            return DEFAULT_IMAGE_NAME
    class Meta:
        verbose_name = u'系统通知表' 
        verbose_name_plural = u'系统通知表'
        db_table = "notify" 
   
class MessageManger(models.Manager):  
    '''
    获得所有我和所有用户之间的最近私信一条不是我发送的私信
    
    '''
    def get_message_list(self,userId): 
        sql='''
    SELECT id,sender_id,senderName,receiver_id,receiveName,content,sendTime,isDeleteSender,isDeletereceiver,isRead  from (
SELECT u.id,u.sender_id,u.receiver_id,u.content,u.sendTime,u.isDeleteSender,u.isDeletereceiver,u.isRead,u2.sendTime as sendTime2
 ,u3.username as senderName,u4.username as  receiveName
 FROM  (
SELECT * FROM (SELECT * from message ORDER BY sendTime desc ) u
WHERE (isDeleteSender= False  AND sender_id= %s ) 
OR (isDeletereceiver = False  AND receiver_id = %s and sender_id!=%s) 
GROUP BY sender_id,receiver_id
 ORDER BY sendTime desc
) u LEFT JOIN  (
SELECT * FROM (SELECT * from message ORDER BY sendTime desc ) u
WHERE (isDeleteSender= False  AND sender_id= %s ) 
OR (isDeletereceiver = False  AND receiver_id = %s and sender_id!=%s) 
GROUP BY sender_id,receiver_id
 ORDER BY sendTime desc)u2 on u.sender_id=u2.receiver_id and  u2.sender_id=u.receiver_id 
 LEFT JOIN auth_user u3 on u.sender_id=u3.id 
LEFT JOIN  auth_user u4 on u.receiver_id=u4.id
 )s
WHERE sendTime>sendTime2 or sendTime2 is NULL
    '''
        return Message.objects.raw(sql,[userId,userId,userId,userId,userId,userId])
 
class Message(models.Model):
    sender=models.ForeignKey(User,verbose_name=u'发信人',related_name="message_from")
    receiver=models.ForeignKey(User,verbose_name=u'收信人',related_name="message_to")
    content=models.TextField(verbose_name="内容")
    sendTime=models.DateTimeField(verbose_name="发出时间")
    '''
    isDeleteSender,idDeleteSender:
                 接收者，发送者删除
      false-----默认,未删
        true---删除
    '''
    isDeleteSender=models.NullBooleanField(verbose_name="发信人删除",default=False)
    isDeletereceiver=models.NullBooleanField(verbose_name="收信删除状态",default=False)
    #接收者是否读件
    isRead=models.NullBooleanField(verbose_name="是否阅读",default=False)
    objects=MessageManger()
    def get_avatar_name(self,*args,**kwargs):
        from apps.user_app.models import UserProfile
        from apps.upload_avatar.app_settings import DEFAULT_IMAGE_NAME
        if kwargs.get('userId',None) is None:
            userProfile=UserProfile.objects.get(user_id=self.sender_id)
        else:
            userProfile=UserProfile.objects.get(user_id=kwargs.get('userId',None))
        if userProfile.avatar_name_status=='3':
            return userProfile.avatar_name
        else:
            return DEFAULT_IMAGE_NAME
        
    
    '''
    序列化
    '''
    def as_json_for_id_conent(self):
        return dict(
            sender_id=self.sender.id,
            content=self.content, 
            receiver_id=self.receiver.id,
           )
    class Meta:
        verbose_name = u'私信消息表' 
        verbose_name_plural = u'私信消息表'
        db_table = "message" 
