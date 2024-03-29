# -*- coding: utf-8 -*-
'''
Created on Sep 17, 2013

@author: jin
'''
from django.utils import simplejson
from util.util import regex_expression, regex_url
from apps.user_app.method import get_avatar_name
'''
消息类类
'''
class MessageBean(object):
    def __init__(self,*args,**kwargs):
        self.id=kwargs.pop('id',None)
        self.senderId=kwargs.pop('sender_id',None)
        self.receiverId=kwargs.pop('receiver_id',None)
        self.senderName=kwargs.pop('sender_name',None)
        self.receiverName=kwargs.pop('receiver_name',None)
        self.content=kwargs.pop('content',None)
        if self.content:
            self.content=regex_expression(self.content)
        self.sendTime=kwargs.pop('sendTime',None)
        if self.sendTime :
            self.sendTime=self.sendTime.strftime("%Y-%m-%d %H:%M:%S")
        self.isDeleteSender=kwargs.pop('isDeletereceiver',None)
        self.isDeletereceiver=kwargs.pop('isDeletereceiver',None)
        self.isRead=kwargs.pop('isRead',None)
        if self.senderId:
            self.avatarName=get_avatar_name(kwargs.get('userId'),self.senderId)
        
        
    
        
    def get_messagebean(self,obj,userId,**kwargs):
        message=obj.message
        self.id=getattr(obj,'id1',None)
        self.senderId=getattr(message,'sender_id',None)
        self.receiverId=getattr(obj,'receiver_id',None)
        self.content=getattr(message,'content',None)
        if self.content:
            self.content=regex_expression( self.content)
        self.sendTime=getattr(message,'sendTime',None)
        if self.sendTime :
            self.sendTime=self.sendTime.strftime("%Y-%m-%d %H:%M:%S")
        self.isDeleteSender=getattr(obj,'isDeleteSender',None)
        self.isDeletereceiver=getattr(obj,'isDeletereceiver',None)
        self.isRead=getattr(obj,'isRead',None)
        self.senderName=message.sender.username
        self.receiverName=obj.receiver.username
        self.avatarName=get_avatar_name(userId,self.senderId)
        
    
        
class MessageBeanEncoder(simplejson.JSONEncoder):
    def default(self, obj):
        if not isinstance(obj, MessageBean):
            return super(MessageBeanEncoder, self).default(obj)
        dict=obj.__dict__
        return dict
    
def MessageLog_to_MessageBean(messageList,userId,**kwargs):
    messageBeanList=[]
    for message in messageList:
        kwargs.update(message)
        kwargs['userId']=userId
        messageBean=MessageBean(**kwargs)
        messageBeanList.append(messageBean)
    return messageBeanList
    
def MessageLog_to_Message(messageLogList,userId,**kwargs):
    messageBeanList=[]
    for message in messageLogList:
        messageBean=MessageBean()
        messageBean.get_messagebean(message,userId,**kwargs)
        messageBeanList.append(messageBean)
    return messageBeanList


'''
转换为页面的消息信息
'''
def messagedynamics_to_message_page(messageDynamicList):
    messageList=[]
    for messageDynamic in messageDynamicList:
        message=messageDynamic
        message['sendTime']=message['sendTime'].strftime("%m-%d %H:%M")
        message['content']=regex_url(message['content'])
        message['content']=regex_expression(message['content'])
        if 'friendDynamic_content' in message and message['friendDynamic_content'] !=None:
            message['friendDynamic_content']=regex_url(message['friendDynamic_content'])
            message['friendDynamic_content']=regex_expression(message['friendDynamic_content'])
        if message['type']==2:
            #判断是否关注
            from apps.user_app.method import is_follow,is_follow_each
            if is_follow(message['receiver_id'],message['sender_id']):
                message['fllow_type']=1
            elif is_follow_each(message['receiver_id'],message['sender_id']):
                message['fllow_type']=2
            else:
                message['fllow_type']=0
        #判断黑名单
        from util.cache import is_black_list
        message['isBlackList']=is_black_list(message['receiver_id'],message['sender_id'])
        messageList.append(message)
    return messageList