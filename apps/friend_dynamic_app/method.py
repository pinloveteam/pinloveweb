# -*-coding: utf-8 -*-
'''
Created on 2014年7月7日

@author: jin
'''
from apps.friend_dynamic_app.models import FriendDynamicComment,\
    FriendDynamicArgee
'''
根据用户id获取未读消息数量
'''
def get_no_read_comment_count(userId):
    return FriendDynamicComment.objects.get_no_read_comment_count(userId)

'''
根据id列表将评论标记成已读
@param ids:id列表 
'''
def clean_dynamic_comment_by_ids(ids):
    FriendDynamicComment.objects.filter(id__in=ids).update(isRead=True)
  
'''
根据id列表将点赞标记成已读
@param ids:id列表 
'''  
def clean_dynamic_argee_by_ids(ids):
    FriendDynamicArgee.objects.filter(id__in=ids).update(isRead=True)