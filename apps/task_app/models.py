# -*- coding: utf-8 -*-
'''
Created on 2015年4月2日

@author: jin
'''
# -*- coding: utf-8 -*-
'''
Created on Aug 30, 2013

@author: jin
'''
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured
from django.db.models.signals import post_save
import datetime

    
class EmailRecommendHistory(models.Model):
    '''
    邮件推荐过的人
    '''
    user=models.ForeignKey(User,verbose_name=u'用户',related_name='email_recommend_user')
    recommender=models.ForeignKey(User,verbose_name=u'推荐用户',related_name='email_recommend_recommender')
    time = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = u'邮件推荐表' 
        verbose_name_plural = u'邮件推荐表'
        db_table=u'email_recommend_history'
        
class TaskRecode(models.Model):
    '''
    任务运行记录
    '''
    time = models.DateTimeField(auto_now_add=True)
    result=models.CharField(verbose_name=u'结果',choices=(('success','成功'),('error','错误')),max_length=10)
    content=models.CharField(verbose_name=u'任务内容',max_length=125)
    data=models.CharField(verbose_name=u'数据',max_length=255,null=True,blank=True,)
    class Meta:
        verbose_name = u'任务运行记录表' 
        verbose_name_plural = u'任务运行记录表'
        db_table=u'task_recode'
    
        