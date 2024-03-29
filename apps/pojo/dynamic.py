# -*- coding: utf-8 -*-
'''
Created on Sep 17, 2014

@author: jin
'''
from django.utils import simplejson
from simplejson.encoder import JSONEncoder
from util.util import regex_expression, regex_url
from apps.friend_dynamic_app.models import FriendDynamicComment
'''
评论类
'''
class DynamicComment(object):
    def __init__(self,id,reviewer,receiver,content,commentTime,reviewerAvatarName):
        self.id=id
        self.reviewerName=reviewer.username
        self.reviewerId=reviewer.id
        if receiver is None:
            self.receiverName=None
            self.receiverId=None
        else:
            self.receiverId=receiver.id
            self.receiverName=receiver.username
        content=regex_url(content)
        self.content=regex_expression(content)
        self.commentTime=commentTime.strftime("%Y-%m-%d %H:%M:%S")
        self.reviewerAvatarName=reviewerAvatarName
        
class DynamicCommentEncoder(simplejson.JSONEncoder):
    def default(self, obj):
        if not isinstance(obj, DynamicComment):
            return super(DynamicCommentEncoder, self).default(obj)
        dict=obj.__dict__
        return dict

def FriendDynamicCommentList_to_DynamicCommentList(userId,friendDynamicCommentList):
    dynamicCommentList=[]
    for friendDynamicComment in friendDynamicCommentList:
        id=friendDynamicComment.id
        reviewer=friendDynamicComment.reviewer
        try:
            receiver=friendDynamicComment.receiver
        except FriendDynamicComment.DoesNotExist: 
            receiver=None
        content=friendDynamicComment.content
        commentTime=friendDynamicComment.commentTime
        from apps.user_app.method import get_avatar_name
        reviewerAvatarName=get_avatar_name(userId, friendDynamicComment.reviewer.id)
        dynamicComment=DynamicComment(id,reviewer,receiver,content,commentTime,reviewerAvatarName)
        dynamicCommentList.append(dynamicComment)
    return dynamicCommentList
        
  
'''
动态类
'''  
class Dynamic(object):
   def __init__(self):
    self.id=None
    self.publishUserName=None
    self.publishUserId=None
    self.avatarName=None
    self.type=None
    self.content=None
    self.data=None
    self.publishTime=None
    self.argeeNum=None
    self.commentNum=None
    self.isAgree=False
    self.commentList=None
    '''
     key:username,time
    '''
    self.agreeList=[]
    
class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__  
def friendDynamicList_to_Dynamic(friendDynamicList,userId):
    dynamicList=[]
    from apps.friend_dynamic_app.models import FriendDynamicArgee
    from apps.friend_dynamic_app.models import FriendDynamic
    for friendDynamic in friendDynamicList:
        dynamic=Dynamic()
        for field in ['id','type','content']:
            setattr(dynamic,field,getattr(friendDynamic,field))
        dynamic.content=regex_url(dynamic.content)
        dynamic.content=regex_expression(dynamic.content)
        dynamic.publishUserId=friendDynamic.publishUser.id
        dynamic.publishUserName=friendDynamic.publishUser.username
        from apps.user_app.method import get_avatar_name
        dynamic.avatarName=get_avatar_name(userId, friendDynamic.publishUser.id)
        from util.util import time_for_now
        dynamic.publishTime=time_for_now( friendDynamic.publishTime)
        if friendDynamic.type==2:
            dynamic.data=simplejson.loads(friendDynamic.data)
        dynamic.isAgree=FriendDynamicArgee.objects.is_agree(friendDynamic.id, userId)
        dynamic.commentNum=FriendDynamic.objects.get_coment_count(friendDynamic.publishUser.id,userId,friendDynamic.id)
        #获得评论
        if dynamic.publishUserId==userId:
            friendDynamicCommentList=FriendDynamicComment.objects.select_related('reviewer','receiver').filter(friendDynamic_id=friendDynamic.id,isDelete=False).order_by('-commentTime')
            friendDynamicArgeeList=FriendDynamicArgee.objects.get_agree_List_by_dynamic(userId,friendDynamic.id)
            dynamic.argeeNum=FriendDynamicArgee.objects.filter(friendDynamic_id=friendDynamic.id).count()
        else:
            from django.db.models.query_utils import Q
            friendDynamicCommentList=FriendDynamicComment.objects.select_related('reviewer','receiver').filter(friendDynamic_id=friendDynamic.id,reviewer_id__in=[userId,dynamic.publishUserId],isDelete=False).filter(Q(receiver_id__in=[userId,dynamic.publishUserId])|Q(receiver_id=None)).order_by('-commentTime')
            friendDynamicArgeeList=FriendDynamicArgee.objects.get_agree_List_by_ids([userId,dynamic.publishUserId],friendDynamic.id)
            dynamic.argeeNum=FriendDynamicArgee.objects.filter(friendDynamic_id=friendDynamic.id,user_id__in=[dynamic.publishUserId,userId]).count()
        friendDynamicCommentList=friendDynamicCommentList.reverse()
        dynamic.commentList=simplejson.dumps(FriendDynamicCommentList_to_DynamicCommentList(userId,friendDynamicCommentList),cls=DynamicCommentEncoder)
        for friendDynamicArgee in friendDynamicArgeeList:
            from apps.user_app.method import get_avatar_name
            dynamic.agreeList.append({'userId':friendDynamicArgee['sender_id'],'username':friendDynamicArgee['sender_name'],'avatarName':get_avatar_name(userId,friendDynamicArgee['sender_id']),'time':friendDynamicArgee['sendTime'].strftime("%m-%d %H:%M")})
        dynamicList.append(dynamic)
    return dynamicList


'''
评论和动态类
'''        
class  CommentDynamic(DynamicComment):
    def __init__(self,id,reviewer,receiver,content,commentTime,reviewerAvatarName,dynamic):
        super(CommentDynamic,self).__init__(id,reviewer,receiver,content,commentTime,reviewerAvatarName)
        self.dynamicId=dynamic.id
        self.content=regex_url(dynamic.content)
        self.dynamicConent=regex_expression(self.content)
        if dynamic.type==2:
            pics=(u'[图片]'*len(simplejson.loads(dynamic.data)))
            self.dynamicConent='%s%s'%(self.dynamicConent,pics)
        self.dynamicPublishTime=dynamic.publishTime
        self.dynamicCommentNum=dynamic.commentNum

'''
动态评论类转化成评论和动态类
'''     
def FriendDynamicCommentList_to_CommentDynamicList(friendDynamicCommentList):
    dynamicCommentList=[]
    for friendDynamicComment in friendDynamicCommentList:
        id=friendDynamicComment.id
        reviewer=friendDynamicComment.reviewer
        from apps.friend_dynamic_app.models import FriendDynamicComment
        try:
            receiver=friendDynamicComment.receiver
        except FriendDynamicComment.DoesNotExist: 
            receiver=None
        content=friendDynamicComment.content
        commentTime=friendDynamicComment.commentTime
        reviewerAvatarName=friendDynamicComment.get_avatar_name(friendDynamicComment.reviewer.id)
        dynamicComment=CommentDynamic(id,reviewer,receiver,content,commentTime,reviewerAvatarName,friendDynamicComment.friendDynamic)
        dynamicCommentList.append(dynamicComment)
    return dynamicCommentList
