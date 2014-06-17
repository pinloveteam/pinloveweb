# -*- coding: utf-8 -*-
'''
Created on 2014年6月10日

@author: jin
'''
from django.utils import simplejson
class NotifyBean(object):
    def __init__(self,*args,**kwargs):
        self.id=kwargs.pop('id',None)
        self.senderId=kwargs.pop('sender_id',None)
        self.senderName=kwargs.pop('senderName',None)
        self.receiverId=kwargs.pop('receiver_id',None)
        self.receiverName=kwargs.pop('receiverName',None)
        self.content=kwargs.pop('content',None)
        self.sendTime=kwargs.pop('sendTime',None)
        if self.sendTime :
            self.sendTime=self.sendTime.strftime("%Y-%m-%d %H:%M:%S")
        self.isRead=kwargs.pop('isRead',None)
        self.avatarName=None
     
    '''
    将Notify初始化成notifybean
    attridute:
       userId[long]  用户id
       obj[Notify]  Notify对象
       userId  当前用户id
       option：
          type[int]  1  得到用户头像不是自己
    '''   
    def get_notifybean(self,obj,userId,**kwargs):
        self.id=getattr(obj,'id',None)
        self.senderId=getattr(obj,'sender_id',None)
        self.receiverId=getattr(obj,'receiver_id',None)
        self.content=getattr(obj,'content',None)
        self.sendTime=getattr(obj,'sendTime',None)
        if self.sendTime :
            self.sendTime=self.sendTime.strftime("%Y-%m-%d %H:%M:%S")
        self.isRead=getattr(obj,'isRead',None)
        self.senderName=obj.sender.username
        self.receiverName=obj.receiver.username
        from apps.upload_avatar.app_settings import SYSTEM_DEFAULT_IMAGE_NAME
        self.avatarName=SYSTEM_DEFAULT_IMAGE_NAME
        if kwargs.pop('type',None) is None:
            if userId==self.senderId:
                self.avatarName=obj.get_avatar_name(userId)
        elif userId==self.senderId:
            self.receiverName=u'拼爱小助手'
        else:
            self.senderName=u'拼爱小助手'
            
        
class NotifyBeanEncoder(simplejson.JSONEncoder):
    def default(self, obj):
        if not isinstance(obj, NotifyBean):
            return super(NotifyBeanEncoder, self).default(obj)
        dict=obj.__dict__
        return dict
    
def Notify_to_NotifyBean(notifyList,userId,**kwargs):
    notifyBeanList=[]
    for notify in notifyList:
        notifyBean=NotifyBean()
        notifyBean.get_notifybean(notify,userId,**kwargs)
        notifyBeanList.append(notifyBean)
    return notifyBeanList