# -*- coding: utf-8 -*-
'''
Created on 2014年11月15日

@author: jin
'''
from django.db import models
from django.contrib.auth.models import User
import datetime
class ScoreRank(models.Model):
    my=models.ForeignKey(User,related_name='rank_my',verbose_name=u'自己')
    other=models.ForeignKey(User,related_name='rank_other',verbose_name=u'别人')
    score=models.FloatField(verbose_name=u"分数")
    nickname=models.CharField(verbose_name=u"昵称",max_length=128)
    time=models.DateTimeField(verbose_name='时间')
    data=models.CharField(verbose_name='详细数据',max_length=255)
    def save(self, *args, **kwargs):
        self.time=datetime.datetime.now()
        super(ScoreRank, self).save(*args, **kwargs)
    class Meta:
        verbose_name = u'微信游戏表' 
        verbose_name_plural = u'微信游戏表'
        db_table=u'weixin_score_rank'