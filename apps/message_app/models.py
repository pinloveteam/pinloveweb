# -*- coding: utf-8 -*-
'''
Created on Aug 30, 2013

@author: jin
model Notify 消息表
'''
from django.db import models
from django.contrib.auth.models import User

class Notify(models.Model):
    sender=models.ForeignKey(User,related_name="from",verbose_name=u'发信人')
    receiver=models.ForeignKey(User,related_name="receive",verbose_name=u'收信人',null=True,blank=True,)
    TYPE_CHOICE=(('0','系统消息'),('1','系统邮件'),)
    type=models.CharField(verbose_name="发送方式",max_length=2,choices=TYPE_CHOICE,null=True,default='1')
    title=models.CharField(verbose_name="标题",max_length=128,null=True)
    content=models.TextField(verbose_name="内容")
    sendTime=models.DateTimeField(verbose_name="发出时间")
    isRead=models.NullBooleanField(verbose_name="是否阅读")
    
    class Meta:
        verbose_name = u'系统通知表' 
        verbose_name_plural = u'系统通知表'
        db_table = "notify" 
        
class Message(models.Model):
    sender=models.ForeignKey(User,verbose_name=u'发信人',related_name="message_from")
    receiver=models.ForeignKey(User,verbose_name=u'收信人',related_name="message_to")
    content=models.TextField(verbose_name="内容")
    sendTime=models.DateTimeField(verbose_name="发出时间")
    """
    isDeleteSender,idDeleteSender:
                 接收者，发送者删除
      false-----默认,未删
        true---删除
    """
    isDeleteSender=models.NullBooleanField(verbose_name="发信人删除",default=False)
    isDeletereceiver=models.NullBooleanField(verbose_name="收信删除状态",default=False)
    #接收者是否读件
    isRead=models.NullBooleanField(verbose_name="是否阅读",default=False)
    
  
    class Meta:
        verbose_name = u'私信消息表' 
        verbose_name_plural = u'私信消息表'
        db_table = "Message" 
