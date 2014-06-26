# # -*- coding: utf-8 -*-
'''
Created on 2014年6月26日

@author: jin
'''
from apps.message_app.models import Notify, Message
'''
获取未读信息
'''
def get_no_read_message_count(userId):
    #获取未读系统消息的数量
    systemNoReadCount=Notify.objects.filter(type='0',receiver=userId,isRead=False).count()
    #获取未读私信消息的数量
    messageNoReadCount=Message.objects.filter(receiver=userId,isRead=False,isDeletereceiver=False).count()
    return systemNoReadCount+messageNoReadCount

'''
将未读信息标记成已读
'''
def clean_message(userId):
    Notify.objects.filter(type='0',receiver_id=userId,isRead=False).update(isRead=True)
    Message.objects.filter(receiver_id=userId,isRead=False,isDeletereceiver=False).update(isRead=True)

'''
将两个用户之间的未读消息标记成已读
attridute:
   notify  系统消息
   message 私信
'''
def clean_message_by_user(senderId,type,receiverId=None):
    if type=='notify':
        Notify.objects.filter(type='0',receiver_id=senderId,isRead=False).update(isRead=True)
    elif type=='message':
        Message.objects.filter(sender_id=senderId,receiver_id=receiverId,isRead=False,isDeletereceiver=False).update(isRead=True)
    
    