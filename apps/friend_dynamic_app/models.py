# -*-coding: utf-8 -*-
'''
Created on Nov 4, 2013

@author: jin
'''
from django.db import models
from django.contrib.auth.models import User
import datetime
class FriendDynamic(models.Model):
    publishUser=models.ForeignKey(User,verbose_name='发布用户',)
    type=models.SmallIntegerField(verbose_name=r"类型",)
    content=models.CharField(verbose_name=r"内容",max_length=255)
    data=models.TextField(verbose_name=r"图片或视频数据",)
    publishTime=models.DateTimeField(verbose_name="发表时间")
    argeeNum=models.IntegerField(verbose_name="点赞次数",default=0)
    commentNum=models.IntegerField(verbose_name="评论次数",default=0)
    def save(self):
        today=datetime.datetime.today()
        self.publishTime=today
        super(FriendDynamic, self).save()
    class Meta:
        verbose_name = u'好友动态信息表' 
        verbose_name_plural = u'好友动态信息表'
        db_table = "friend_dynamic" 
        
    
class FriendDynamicArgee(models.Model):
    friendDynamic=models.ForeignKey(FriendDynamic,verbose_name="好友动态",)
    user=models.ForeignKey(User,verbose_name="用户",)
    class Meta:
        verbose_name = u'点赞表' 
        verbose_name_plural = u'点赞表'
        db_table = "friend_dynamic_argee" 

class FriendDynamicComment(models.Model):
    friendDynamic=models.ForeignKey(FriendDynamic,verbose_name="好友动态",)
    user=models.ForeignKey(User,verbose_name="用户",)
    content=models.CharField(verbose_name="评论内容",max_length=255)
    isDelete=models.NullBooleanField(verbose_name="是否删除",default=False)
    commentTime=models.DateTimeField(verbose_name="评论时间")
    class Meta:
        verbose_name = u'评论表' 
        verbose_name_plural = u'评论表'
        db_table = "friend_dynamic_comment" 
        
class Picture(models.Model):
    user=models.ForeignKey(User,verbose_name="用户",)
    friendDynamic=models.ForeignKey(FriendDynamic,verbose_name="好友动态",)
    description=models.CharField(verbose_name="照片描述",max_length=255)
    picPath=models.CharField(verbose_name="图片路径",max_length=255)
    createTime=models.DateTimeField(verbose_name="创建时间")
    class Meta:
        verbose_name = u'图片表' 
        verbose_name_plural = u'图片表'
        db_table = "picture" 
    def save(self):
        today=datetime.datetime.today()
        self.createTime=today
        super(Picture, self).save()