# -*- coding: utf-8 -*-
'''
Created on Sep 17, 2014

@author: jin
'''
from django.utils import simplejson
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
        self.content=content
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
    self.publishUser=None
    self.type=None
    self.content=None
    self.data=None
    self.publishTime=None
    self.argeeNum=None
    self.commentNumNone
    
# def friendDynamicList_to_Dynamic(friendDynamicList,friendDynamicArgeeList):
#     arg={}
#     DynamicList=[]
#     argeeList=[]
#     for friendDynamic in friendDynamicList:
#         for field in []
#         if friendDynamic.type==2:
#             friendDynamic.data=simplejson.loads(friendDynamic.data)
#         is_agreee=False  
#         for friendDynamicArgee in friendDynamicArgeeList:
#             if friendDynamic.id==friendDynamicArgee.friendDynamic_id:
#                 is_agreee=True 
#         argeeList.append(is_agreee)  
#     arg['friendDynamicList']=friendDynamicList
#     arg['argeeList']=argeeList
    return arg