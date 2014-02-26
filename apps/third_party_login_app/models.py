# -*- coding: utf-8 -*-
'''
Created on Aug 30, 2013

@author: jin
model ThirdPsartyLogin 第三方登录表
'''
from django.db import models
from django.contrib.auth.models import User
from django.utils import simplejson

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
'''
facebook 用户表
'''        
class FacebookUser(models.Model):
    uid=models.CharField(verbose_name=u'用户ID',primary_key=True,max_length=125)
    username=models.CharField(verbose_name=u'用户名',max_length=125)
    GENDER_CHOISE=(
                   (u'male',u'F'),
                   (u'female',u'M')
                   )
    gender=models.CharField(verbose_name=u'性别',max_length='1',choices=GENDER_CHOISE)
    avatar=models.CharField(verbose_name=u'头像',max_length=255,null=True,blank=True,)
    location=models.CharField(verbose_name=u'地址',max_length=125,null=True,blank=True,)
    birthday=models.DateTimeField(verbose_name=u'生日',null=True,blank=True,)
    age=models.SmallIntegerField(verbose_name=u'年龄',null=True,blank=True,)
    list=simplejson.dumps([])
    recommendList=models.TextField(verbose_name=u'已经推荐列表',null=True,blank=True,default=list)
    link=models.CharField(verbose_name=u'主题链接',max_length=255,)
    #不推荐列表，包括好友和推荐过的
    noRecommendList=models.TextField(verbose_name=u'不推荐列表',null=True,blank=True,default=list)
    updateTime=models.DateTimeField(verbose_name='最后更新时间')
    
    class Meta:
        verbose_name = u'facebook用户表' 
        verbose_name_plural = u'facebook用户表'
        db_table = "facebook_user" 
        
        
class FacebookPhoto(models.Model):
    id=models.CharField(verbose_name=u'图片ID',primary_key=True,max_length=125)
    user=models.ForeignKey(FacebookUser,related_name="user",verbose_name=u'facebook用户')
    description=models.TextField(verbose_name='说明')
    smailPhoto=models.CharField(verbose_name=u'缩略图',max_length=255)
    bigPhoto=models.CharField(verbose_name=u'原图',max_length=255)
    class Meta:
        verbose_name = u'facebook照片' 
        verbose_name_plural = u'facebook照片'
        db_table = "facebook_photo" 
