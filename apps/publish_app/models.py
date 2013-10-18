# -*- coding: utf-8 -*-
'''
Created on Aug 30, 2013

@author: jin
'''
from django.db import models
from django.contrib.auth.models import User

class Publish(models.Model):
    #发布人
    user=models.ForeignKey(User)
    title=models.CharField(verbose_name=u"标题" ,max_length='50',null=True,blank=True,)
    picture=models.ImageField(verbose_name=u"发布图片" ,upload_to='publish_img',max_length='128',null=True,blank=True,)
    content=models.TextField(verbose_name=u"内容",null=True,blank=True,)
    publishDate=models.DateField(verbose_name=u"发布时间",null=True,blank=True,)
    applyChannel=models.URLField(verbose_name=u"报名通道",null=True,blank=True,)
    class Meta:
        verbose_name = u'消息发布表' 
        verbose_name_plural = u'消息发布表'
