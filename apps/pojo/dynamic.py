# -*- coding: utf-8 -*-
'''
Created on Sep 17, 2014

@author: jin
'''
from django.utils import simplejson
from simplejson.encoder import JSONEncoder
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
        self.content=regex_expression(content)
        self.commentTime=commentTime.strftime("%Y-%m-%d %H:%M:%S")
        self.reviewerAvatarName=reviewerAvatarName
        
        
class DynamicCommentEncoder(simplejson.JSONEncoder):
    def default(self, obj):
        if not isinstance(obj, DynamicComment):
            return super(DynamicCommentEncoder, self).default(obj)
        dict=obj.__dict__
        return dict

def FriendDynamicCommentList_to_DynamicCommentList(friendDynamicCommentList):
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
    
class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__  
def friendDynamicList_to_Dynamic(friendDynamicList,userId):
    DynamicList=[]
    from apps.friend_dynamic_app.models import FriendDynamicArgee
    from apps.friend_dynamic_app.models import FriendDynamic
    for friendDynamic in friendDynamicList:
        dynamic=Dynamic()
        for field in ['id','type','content']:
            setattr(dynamic,field,getattr(friendDynamic,field))
        from util.util import regex_expression
        dynamic.content=regex_expression(dynamic.content)
        dynamic.publishUserId=friendDynamic.publishUser.id
        dynamic.publishUserName=friendDynamic.publishUser.username
        dynamic.avatarName=friendDynamic.get_profile()
        dynamic.publishTime=friendDynamic.publishTime.strftime("%Y-%m-%d %H:%M:%S")
        if friendDynamic.type==2:
            dynamic.data=simplejson.loads(friendDynamic.data)
        dynamic.isAgree=FriendDynamicArgee.objects.is_agree(friendDynamic.id, userId)
        dynamic.argeeNum=FriendDynamicArgee.objects.get_agree_count(friendDynamic.id)
        dynamic.commentNum=FriendDynamic.objects.get_coment_count(friendDynamic.publishUser.id,userId,friendDynamic.id)
        DynamicList.append(dynamic)
    return DynamicList


