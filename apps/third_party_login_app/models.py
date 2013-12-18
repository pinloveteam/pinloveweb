# -*- coding: utf-8 -*-
'''
Created on Aug 30, 2013

@author: jin
model ThirdPsartyLogin 第三方登录表
'''
from django.db import models
from django.contrib.auth.models import User

PROVIDER_CHOICE=(('0','QQ'),('1','新浪'),('2','facebook'),)
class ThirdPsartyLogin(models.Model):
    user=models.ForeignKey(User,related_name="user",verbose_name=u'用户')
    provider=models.CharField(verbose_name=u'供应方',max_length=2,choices=PROVIDER_CHOICE,null=True,blank=True,)
    uid=models.CharField(verbose_name="用户id",max_length=125,null=True)
    access_token=models.CharField(verbose_name='密令',max_length=255,null=True)
    class Meta:
        verbose_name = u'第三方登录表' 
        verbose_name_plural = u'第三方登录表'
        db_table = "third_party_login" 
        