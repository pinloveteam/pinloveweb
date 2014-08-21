# -*-coding: utf-8 -*-
'''
Created on Nov 4, 2013

@author: jin
'''
from django.db import models
from django.contrib.auth.models import User
import datetime
from apps.user_app.models import UserProfile, Follow
from util.connection_db import connection_to_db
class FriendDynamicManage(models.Manager):
    '''
    获得评论条数
    '''
    def get_coment_count(self,publishUserId,userId,dynamicId):
        if publishUserId==userId:
            return FriendDynamicComment.objects.filter(friendDynamic_id=dynamicId).count()
        else:
            from django.db.models.query_utils import Q
            return FriendDynamicComment.objects.filter(Q(friendDynamic_id=dynamicId,reviewer_id__in=[userId,publishUserId],receiver_id__in=[userId,publishUserId])|Q(friendDynamic_id=dynamicId,receiver_id__isnull=True)).count()
    
    '''
    获得关注的动态人列表
    '''
    def get_follow_list(self,user_id):
        followList=Follow.objects.filter(my_id=user_id)
        #我关注的人id列表
        followIdList=[]
        for follow in followList:
            followIdList.append(follow.follow_id)
        followIdList.append(user_id)
        return FriendDynamic.objects.select_related('publishUser').filter(publishUser_id__in=followIdList).order_by('-publishTime')
    
class FriendDynamic(models.Model):
    publishUser=models.ForeignKey(User,verbose_name='发布用户',)
    TYPE_CHOICE=((1,u'纯文字动态'),(2,u'图片动态'))
    type=models.SmallIntegerField(verbose_name=r"类型",choices=TYPE_CHOICE)
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
        userProfile=UserProfile.objects.get(user=self.publishUser)
        if userProfile.avatar_name_status!='3':
            return 'user_img/image'
        else:
            return userProfile.avatar_name
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
        
    '''
    未被查看点赞数
    '''
    def get_no_read_agree_count(self,userId):
        sql='''
       SELECT count(*)
from friend_dynamic_argee u1  LEFT JOIN friend_dynamic u2 on u2.id=u1.friendDynamic_id
LEFT JOIN auth_user u3 on u3.id=u1.user_id LEFT JOIN user_profile u4 on u4.user_id=u1.user_id
WHERE u2.publishUser_id=%s  and u1.isRead=0
'''
        return connection_to_db(sql,param=[userId])[0]
    
    '''
     未被查看点赞信息
    '''
    def get_no_read_agree_List(self,userId):
        sql='''
       SELECT u1.id,u1.user_id as sender_id ,u3.username as sender_name,u4.avatar_name,u4.avatar_name_status,
u2.publishUser_id as receiver_id,null as content,u1.time as sendTime ,3 as type,u1.isRead,
u1.friendDynamic_id,u2.content as friendDynamic_content ,u2.data
from friend_dynamic_argee u1  LEFT JOIN friend_dynamic u2 on u2.id=u1.friendDynamic_id
LEFT JOIN auth_user u3 on u3.id=u1.user_id LEFT JOIN user_profile u4 on u4.user_id=u1.user_id
WHERE u2.publishUser_id=%s  and u1.isRead=0
ORDER BY sendTime desc
'''
        return connection_to_db(sql,param=[userId],type=True)
    '''
     查看一条动态所有点赞列表
    '''
    def get_agree_List(self,userId,dynamicId):
        sql='''
       SELECT u1.id,u1.user_id as sender_id ,u3.username as sender_name,u4.avatar_name,u4.avatar_name_status,
u2.publishUser_id as receiver_id,null as content,u1.time as sendTime ,3 as type,u1.isRead,
u1.friendDynamic_id,u2.content as friendDynamic_content ,u2.data
from friend_dynamic_argee u1  LEFT JOIN friend_dynamic u2 on u2.id=u1.friendDynamic_id
LEFT JOIN auth_user u3 on u3.id=u1.user_id LEFT JOIN user_profile u4 on u4.user_id=u1.user_id
WHERE u2.publishUser_id=%s and u1.friendDynamic_id=%s
ORDER BY time desc
'''
        return connection_to_db(sql,param=[userId,dynamicId],type=True)
    
    '''
    查看对应用户的动态评论
    @param  dynamicId:动态id
    @param idList: id列表
    '''
    def get_agree_List_by_ids(self,idList,dynamicId):
        sql='''
       SELECT u1.id,u1.user_id as sender_id ,u3.username as sender_name,u4.avatar_name,u4.avatar_name_status,
u2.publishUser_id as receiver_id,null as content,u1.time as sendTime ,3 as type,u1.isRead,
u1.friendDynamic_id,u2.content as friendDynamic_content ,u2.data
from friend_dynamic_argee u1  LEFT JOIN friend_dynamic u2 on u2.id=u1.friendDynamic_id
LEFT JOIN auth_user u3 on u3.id=u1.user_id LEFT JOIN user_profile u4 on u4.user_id=u1.user_id
WHERE u2.publishUser_id in ('''+('%s,'*len(idList))[:-1]+''') and u1.user_id in ('''+('%s,'*len(idList))[:-1]+''')  and u1.friendDynamic_id=%s
ORDER BY sendTime desc
'''
        paramList=idList
        paramList.extend(idList)
        paramList.append(dynamicId)
        return connection_to_db(sql,param=paramList,type=True)

class FriendDynamicArgee(models.Model):
    friendDynamic=models.ForeignKey(FriendDynamic,verbose_name="好友动态",)
    user=models.ForeignKey(User,verbose_name="用户",)
    objects=FriendDynamicArgeeManage()
    time=models.DateTimeField(verbose_name="时间")
    isRead=models.NullBooleanField(verbose_name="是否阅读",default=False)
    class Meta:
        verbose_name = u'点赞表' 
        verbose_name_plural = u'点赞表'
        db_table = "friend_dynamic_argee" 
        
class FriendDynamicCommentManage(models.Manager):
    '''
    根据用户id获取未读评论
    '''
    def get_no_read_comment_by_user_id(self,userId):
        return FriendDynamicComment.objects.select_related('friendDynamic','reviewer').filter(receiver_id=userId,isRead=False)
    
    '''
    获取未读评论，用于消息中心数据
    '''
    def get_no_read_comment_list(self,userId):
        sql='''
        SELECT u1.id,u1.reviewer_id as sender_id ,u3.username as sender_name,u4.avatar_name,u4.avatar_name_status,
u1.receiver_id,u1.content,u1.commentTime as sendTime ,5 as type,u1.isRead,
u1.friendDynamic_id,u2.content as friendDynamic_content ,u2.data
from friend_dynamic_comment u1  LEFT JOIN friend_dynamic u2 on u2.id=u1.friendDynamic_id
LEFT JOIN auth_user u3 on u3.id=u1.reviewer_id LEFT JOIN user_profile u4 on u4.user_id=u1.reviewer_id
WHERE u1.receiver_id=%s and u1.isRead=0
ORDER BY sendTime desc
        '''
        return connection_to_db(sql,param=[userId],type=True)
    '''
    获取评论，用于消息中心数据
    '''
    def get_comment_list(self,userId):
        sql='''
        SELECT u1.id,u1.reviewer_id as sender_id ,u3.username as sender_name,u4.avatar_name,u4.avatar_name_status,
u1.receiver_id,u1.content,u1.commentTime as sendTime ,5 as type,u1.isRead,
u1.friendDynamic_id,u2.content as friendDynamic_content ,u2.data
from friend_dynamic_comment u1  LEFT JOIN friend_dynamic u2 on u2.id=u1.friendDynamic_id
LEFT JOIN auth_user u3 on u3.id=u1.reviewer_id LEFT JOIN user_profile u4 on u4.user_id=u1.reviewer_id
WHERE u1.receiver_id=%s 
ORDER BY sendTime desc
        '''
        return connection_to_db(sql,param=[userId],type=True)
    
    '''
    根据用户id获取未读评论数量
    '''
    def get_no_read_comment_count(self,userId):
        return FriendDynamicComment.objects.filter(receiver_id=userId,isRead=False).count()

class FriendDynamicComment(models.Model):
    friendDynamic=models.ForeignKey(FriendDynamic,verbose_name="好友动态",)
    reviewer=models.ForeignKey(User,verbose_name="评论者",related_name="reviewer")
    receiver=models.ForeignKey(User,verbose_name="被评论者",related_name="receiver",null=True,blank=True,)
    content=models.CharField(verbose_name="评论内容",max_length=255)
    isDelete=models.NullBooleanField(verbose_name="是否删除",default=False)
    commentTime=models.DateTimeField(verbose_name="评论时间")
    isRead=models.NullBooleanField(verbose_name="是否阅读",default=False)
    objects=FriendDynamicCommentManage()
    
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