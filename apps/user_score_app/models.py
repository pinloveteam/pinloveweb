# -*- coding: utf-8 -*-
'''
Created on 2014年4月5日

@author: jin
'''
from django.db import models
from django.contrib.auth.models import User
import datetime
'''
用户积分表
'''
class UserScore(models.Model):
    user=models.ForeignKey(User,related_name="user_score",verbose_name=u'用户')
    validScore=models.IntegerField(verbose_name=u'有效积分',default=0)
    freezeScore=models.IntegerField(verbose_name=u'冻结积分积分',default=0)
    class Meta:
        verbose_name = u'用户积分表' 
        verbose_name_plural = u'用户积分表'
        db_table = "user_score"
        
'''
用户积分兑换关系表
用于记录用户的兑换关系
'''      
class UserScoreExchangeRelate(models.Model):
    type=models.CharField(verbose_name=u'操作类型',max_length=10)
    amount=models.IntegerField(verbose_name=u'获得积分数量')
    instruction=models.CharField(verbose_name=u'说明',max_length=255,)
    class Meta:
        verbose_name = u'户积分兑换关系表' 
        verbose_name_plural = u'户积分兑换关系表'
        db_table = "user_score_exchange_relate"
 
'''
用户积分明细表
  用于记录用户每一次积分修改
'''   
class UserScoreDtail(models.Model):
    userScore=models.ForeignKey(UserScore,related_name="user_score_detail",verbose_name=u'用户积分')
    exchangeRelate=models.ForeignKey(UserScoreExchangeRelate,related_name="UserScoreExchangeRelate",verbose_name=u'兑换关系')
    amount=models.IntegerField(verbose_name=u'积分数量',)
    time=models.DateTimeField(verbose_name=u'记录时间',)
    def save(self, *args, **kwargs):
        today=datetime.datetime.today()
        self.time=today
        super(UserScoreDtail, self).save(*args, **kwargs)
    class Meta:
        verbose_name = u'用户积分明细表' 
        verbose_name_plural = u'用户积分明细表'
        db_table = "user_score_detail"
 

