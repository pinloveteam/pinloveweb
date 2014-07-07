# -*-coding: utf-8 -*-
'''
Created on 2014年7月7日

@author: jin
'''
from apps.friend_dynamic_app.models import FriendDynamicComment
'''
根据用户id获取未读消息数量
'''
def get_no_read_comment_count(userId):
    return FriendDynamicComment.objects.get_no_read_comment_count(userId)