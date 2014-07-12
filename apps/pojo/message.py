# -*- coding: utf-8 -*-
'''
Created on Sep 17, 2013

@author: jin
'''
from django.utils import simplejson
from util.util import regex_expression
from apps.user_app.method import get_avatar_name
'''
消息类类
'''
class MessageBean(object):
    def __init__(self,*args,**kwargs):
        self.id=kwargs.pop('id',None)
        self.senderId=kwargs.pop('sender_id',None)
        self.receiverId=kwargs.pop('receiver_id',None)
        self.senderName=kwargs.pop('senderName',None)
        self.receiverName=kwargs.pop('receiverName',None)
        self.content=kwargs.pop('content',None)
        if self.content:
            self.content=regex_expression(self.content)
        self.sendTime=kwargs.pop('sendTime',None)
        if self.sendTime :
            self.sendTime=self.sendTime.strftime("%Y-%m-%d %H:%M:%S")
        self.isDeleteSender=kwargs.pop('isDeletereceiver',None)
        self.isDeletereceiver=kwargs.pop('isDeletereceiver',None)
        self.isRead=kwargs.pop('isRead',None)
        self.avatarName=None if self.senderId is None else self.get_avatar_name(kwargs.get('userId'),type=kwargs.get('type'))
        
    '''
    获取头像
    myId当前用户的id
    '''
    def get_avatar_name(self,myId,type=None):
        userId=self.senderId
        if not type is None:
            if myId==self.senderId:
                userId=self.receiverId
        return get_avatar_name(myId,userId)
        
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
        self.avatarName=self.get_avatar_name(self,userId)
        
    
        
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