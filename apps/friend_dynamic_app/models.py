# -*-coding: utf-8 -*-
'''
Created on Nov 4, 2013

@author: jin
'''
from django.db import models
from django.contrib.auth.models import User
import datetime
from apps.user_app.models import UserProfile
class FriendDynamicManage(models.Manager):
    def get_coment_count(self,publishUserId,userId,dynamicId):
        if publishUserId==userId:
            return FriendDynamicComment.objects.filter(friendDynamic_id=dynamicId).count()
        else:
            from django.db.models.query_utils import Q
            return FriendDynamicComment.objects.filter(Q(friendDynamic_id=dynamicId,reviewer_id__in=[userId,publishUserId],receiver_id__in=[userId,publishUserId])|Q(receiver_id__isnull=True)).count()
class FriendDynamic(models.Model):
    publishUser=models.ForeignKey(User,verbose_name='发布用户',)
    type=models.SmallIntegerField(verbose_name=r"类型",)
    content=models.CharField(verbose_name=r"内容",max_length=255)
    data=models.TextField(verbose_name=r"图片或视频数据",)
    publishTime=models.DateTimeField(verbose_name="发表时间")
    argeeNum=models.IntegerField(verbose_name="点赞次数",default=0)
    commentNum=models.IntegerField(verbose_name="评论次数",default=0)
    objects=FriendDynamicManage()
    def save(self):
        today=datetime.datetime.today()
        self.publishTime=today
        super(FriendDynamic, self).save()
    def get_profile(self):
        return UserProfile.objects.get(user=self.publishUser).avatar_name
    class Meta:
        verbose_name = u'好友动态信息表' 
        verbose_name_plural = u'好友动态信息表'
        db_table = "friend_dynamic" 
        
class FriendDynamicArgeeManage(models.Manager):
    '''
    判断是否点赞
    '''
    def is_agree(self,friendDynamicId,userId):
        return FriendDynamicArgee.objects.filter(user_id=userId,friendDynamic_id=friendDynamicId).exists()
    
    '''
    点赞总数
    '''
    def get_agree_count(self,dynamicId):
            return FriendDynamicArgee.objects.filter(friendDynamic_id=dynamicId).count()
class FriendDynamicArgee(models.Model):
    friendDynamic=models.ForeignKey(FriendDynamic,verbose_name="好友动态",)
    user=models.ForeignKey(User,verbose_name="用户",)
    objects=FriendDynamicArgeeManage()
    class Meta:
        verbose_name = u'点赞表' 
        verbose_name_plural = u'点赞表'
        db_table = "friend_dynamic_argee" 

class FriendDynamicComment(models.Model):
    friendDynamic=models.ForeignKey(FriendDynamic,verbose_name="好友动态",)
    reviewer=models.ForeignKey(User,verbose_name="评论者",related_name="reviewer")
    receiver=models.ForeignKey(User,verbose_name="被评论者",related_name="receiver",null=True,blank=True,)
    content=models.CharField(verbose_name="评论内容",max_length=255)
    isDelete=models.NullBooleanField(verbose_name="是否删除",default=False)
    commentTime=models.DateTimeField(verbose_name="评论时间")
    def get_avatar_name(self,userId):
        userProfile=UserProfile.objects.get(user_id=userId)
        if userProfile.avatar_name_status=='3':
           return userProfile.avatar_name
        else:
           from apps.upload_avatar.app_settings import DEFAULT_IMAGE_NAME
           return DEFAULT_IMAGE_NAME
    def save(self):
        today=datetime.datetime.today()
        self.commentTime=today
        super(FriendDynamicComment, self).save()
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