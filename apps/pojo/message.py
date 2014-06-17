# -*- coding: utf-8 -*-
'''
Created on Sep 17, 2013

@author: jin
'''
from django.utils import simplejson
from util.util import regex_expression
'''
  推荐结果类
'''
class MessageBean(object):
    def __init__(self,*args,**kwargs):
        self.id=kwargs.pop('id',None)
        self.senderId=kwargs.pop('sender_id',None)
        self.receiverId=kwargs.pop('receiver_id',None)
        self.content=kwargs.pop('content',None)
        if self.content:
            self.content=regex_expression(self.content)
        self.sendTime=kwargs.pop('sendTime',None)
        if self.sendTime :
            self.sendTime=self.sendTime.strftime("%Y-%m-%d %H:%M:%S")
        self.isDeleteSender=kwargs.pop('isDeletereceiver',None)
        self.isDeletereceiver=kwargs.pop('isDeletereceiver',None)
        self.isRead=kwargs.pop('isRead',None)
        self.avatarName=None
        
    def get_messagebean(self,obj,userId,**kwargs):
        self.id=getattr(obj,'id',None)
        self.senderId=getattr(obj,'sender_id',None)
        self.receiverId=getattr(obj,'receiver_id',None)
        self.content=getattr(obj,'content',None)
        if self.content:
            self.content=regex_expression( self.content)
        self.sendTime=getattr(obj,'sendTime',None)
        if self.sendTime :
            self.sendTime=self.sendTime.strftime("%Y-%m-%d %H:%M:%S")
        self.isDeleteSender=getattr(obj,'isDeleteSender',None)
        self.isDeletereceiver=getattr(obj,'isDeletereceiver',None)
        self.isRead=getattr(obj,'isRead',None)
        if not kwargs.pop('type',None) is None:
            self.senderName=getattr(obj,'senderName',False)
            if not self.senderName:
                self.senderName=obj.sender.username
            self.receiverName=getattr(obj,'receiverName',False)
            if not self.receiverName:
                self.receiverName=obj.receiver.username
            if userId==self.senderId:
                kwargs['userId']=self.receiverId
            else:
                kwargs['userId']=self.senderId
        self.avatarName=obj.get_avatar_name(**kwargs)
        
    
        
class MessageBeanEncoder(simplejson.JSONEncoder):
    def default(self, obj):
        if not isinstance(obj, MessageBean):
            return super(MessageBeanEncoder, self).default(obj)
        dict=obj.__dict__
        return dict
    
def Message_to_MessageBean(messageList,userId,**kwargs):
    messageBeanList=[]
    for message in messageList:
        messageBean=MessageBean()
        messageBean.get_messagebean(message,userId,**kwargs)
        messageBeanList.append(messageBean)
    return messageBeanList
    