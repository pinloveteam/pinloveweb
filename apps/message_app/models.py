# -*- coding: utf-8 -*-
'''
Created on Aug 30, 2013

@author: jin
model Notify 消息表
'''
from django.db import models
from django.contrib.auth.models import User
from util.connection_db import connection_to_db, connection_to_db_commit
import datetime
from pinloveweb.settings import ADMIN_ID

# class Notify(models.Model):
#     sender=models.ForeignKey(User,related_name="from",verbose_name=u'发信人')
#     receiver=models.ForeignKey(User,related_name="receive",verbose_name=u'收信人',null=True,blank=True,)
#     TYPE_CHOICE=(('0','系统消息'),('1','系统邮件'),)
#     type=models.CharField(verbose_name="发送方式",max_length=2,choices=TYPE_CHOICE,null=True,default='1')
#     title=models.CharField(verbose_name="标题",max_length=128,null=True,)
#     content=models.TextField(verbose_name="内容")
#     sendTime=models.DateTimeField(verbose_name="发出时间")
#     isRead=models.NullBooleanField(verbose_name="是否阅读")
#     
#     '''
#     '''
#     def get_avatar_name(self,userId):
#         from apps.user_app.models import UserProfile
#         userProfile=UserProfile.objects.get(user_id=userId)
#         if userProfile.avatar_name_status=='3':
#             return userProfile.avatar_name
#         else:
#             from apps.upload_avatar.app_settings import DEFAULT_IMAGE_NAME
#             return DEFAULT_IMAGE_NAME
#     class Meta:
#         verbose_name = u'系统通知表' 
#         verbose_name_plural = u'系统通知表'
#         db_table = "notify" 
#    
# class MessageManger(models.Manager):  
#     '''
#     获得所有我和所有用户之间的最近私信一条不是我发送的私信
#     
#     '''
#     def get_message_list(self,userId): 
#         sql='''
#     SELECT id,sender_id,senderName,receiver_id,receiveName,content,sendTime,isDeleteSender,isDeletereceiver,isRead  from (
# SELECT u.id,u.sender_id,u.receiver_id,u.content,u.sendTime,u.isDeleteSender,u.isDeletereceiver,u.isRead,u2.sendTime as sendTime2
#  ,u3.username as senderName,u4.username as  receiveName
#  FROM  (
# SELECT * FROM (SELECT * from message ORDER BY sendTime desc ) u
# WHERE (isDeleteSender= False  AND sender_id= %s ) 
# OR (isDeletereceiver = False  AND receiver_id = %s and sender_id!=%s) 
# GROUP BY sender_id,receiver_id
#  ORDER BY sendTime desc
# ) u LEFT JOIN  (
# SELECT * FROM (SELECT * from message ORDER BY sendTime desc ) u
# WHERE (isDeleteSender= False  AND sender_id= %s ) 
# OR (isDeletereceiver = False  AND receiver_id = %s and sender_id!=%s) 
# GROUP BY sender_id,receiver_id
#  ORDER BY sendTime desc)u2 on u.sender_id=u2.receiver_id and  u2.sender_id=u.receiver_id 
#  LEFT JOIN auth_user u3 on u.sender_id=u3.id 
# LEFT JOIN  auth_user u4 on u.receiver_id=u4.id
#  )s
# WHERE sendTime>sendTime2 or sendTime2 is NULL
#     '''
#         return Message.objects.raw(sql,[userId,userId,userId,userId,userId,userId])
#     
#     '''
#     根据userid获得未读信息
#     '''
#     def get_no_read_message_by_user_id(self,userId):
#         return Message.objects.filter(receiver_id=userId,isRead=False,isDeletereceiver=False)
#  
# class Message(models.Model):
#     sender=models.ForeignKey(User,verbose_name=u'发信人',related_name="message_from")
#     receiver=models.ForeignKey(User,verbose_name=u'收信人',related_name="message_to")
#     content=models.TextField(verbose_name="内容")
#     sendTime=models.DateTimeField(verbose_name="发出时间")
#     '''
#     isDeleteSender,idDeleteSender:
#                  接收者，发送者删除
#       false-----默认,未删
#         true---删除
#     '''
#     isDeleteSender=models.NullBooleanField(verbose_name="发信人删除",default=False)
#     isDeletereceiver=models.NullBooleanField(verbose_name="收信删除状态",default=False)
#     #接收者是否读件
#     isRead=models.NullBooleanField(verbose_name="是否阅读",default=False)
#     objects=MessageManger()
#     def get_avatar_name(self,*args,**kwargs):
#         from apps.user_app.models import UserProfile
#         from apps.upload_avatar.app_settings import DEFAULT_IMAGE_NAME
#         if kwargs.get('userId',None) is None:
#             userProfile=UserProfile.objects.get(user_id=self.sender_id)
#         else:
#             userProfile=UserProfile.objects.get(user_id=kwargs.get('userId',None))
#         if userProfile.avatar_name_status=='3':
#             return userProfile.avatar_name
#         else:
#             return DEFAULT_IMAGE_NAME
#         
#     
#     '''
#     序列化
#     '''
#     def as_json_for_id_conent(self):
#         from util.util import regex_expression
#         content=regex_expression(self.content)
#         return dict(
#             sender_id=self.sender.id,
#             content=content, 
#             receiver_id=self.receiver.id,
#            )
#     class Meta:
#         verbose_name = u'私信消息表' 
#         verbose_name_plural = u'私信消息表'
#         db_table = "message" 

    
'''
系统消息
'''
class Message(models.Model):
    sender=models.ForeignKey(User,verbose_name=u'发信人',related_name="message_from")
    content=models.TextField(verbose_name="内容")
    sendTime=models.DateTimeField(verbose_name="发出时间")
    TYPE_CHOICES=((0,'群发'),(1,'单发'))
    type=models.SmallIntegerField(verbose_name="信息类型",choices=TYPE_CHOICES)
    expireTime=models.DateTimeField(verbose_name="失效时间",null=True)
    def save(self,*args,**kwargs):
        self.sendTime=datetime.datetime.now()
        super(Message,self).save(*args,**kwargs)
    class Meta:
        verbose_name = u'消息表' 
        verbose_name_plural = u'消息表'
        db_table = "message" 
        
class MessageLogManger(models.Manager):  
    '''
    获得所有我和所有用户之间的私信
     
    '''
    def get_message_list(self,userId): 
        sql='''
         SELECT * from (  
   SELECT * from (
SELECT null as id1,%s as receiver_id,null as message_id,null as isDeleteSender,
null as isDeletereceiver ,null as isRead, u3.* ,null as receiverName,u4.username as senderName 
from message u3 INNER JOIN  auth_user u4 on u4.id=u3.sender_id
where u3.type=0 and u3.id not in (SELECT u4.message_id from message_log u4) and now()<=u3.expireTime
UNION
SELECT u1.*,u2.*,u3.username as receiverName,u4.username as senderName from message_log u1 LEFT JOIN message u2 on u1.message_id=u2.id
INNER JOIN auth_user u3 on u1.receiver_id=u3.id INNER JOIN auth_user u4 on u2.sender_id=u4.id
where  (isDeletereceiver = False  AND receiver_id = %s and sender_id!=%s)
) s
ORDER BY type,sendTime desc
)s1
GROUP BY sender_id


    '''
        return  connection_to_db(sql,param=[userId,userId,userId],type=True)
    
    '''
    获取用户未读消息数量
    '''
    def get_no_read_msessge_count(self,userId):
        sql='''
        SELECT count(*) from (
SELECT  u3.id
from message u3 
where u3.type=0 and u3.id not in (SELECT u4.message_id from message_log u4) and now()<=u3.expireTime
UNION
SELECT u2.id from message_log u1 LEFT JOIN message u2 on u1.message_id=u2.id
where  isDeletereceiver = False  and isRead=0 AND receiver_id = %s
) s
        '''
        return  connection_to_db(sql,param=[userId])[0]
    
    '''
    获取所有未读消息
    '''
    def get_no_read_messagelog(self,userId):
        sql='''
        SELECT * from (
SELECT null as id,%s as receiver_id,u3.id as message_id,0 as isDeleteSender,
0 as isDeletereceiver ,0 as isRead,u3.sendTime
from message u3 
where u3.type=0 and u3.id not in (SELECT u4.message_id from message_log u4) and now()<=u3.expireTime
UNION
SELECT u1.*,u2.sendTime from message_log u1 LEFT JOIN message u2 on u1.message_id=u2.id
where  isDeletereceiver = False  and u1.isRead=False  AND receiver_id = %s 
) s
ORDER BY sendTime desc
        '''
        messageLogList=MessageLog.objects.raw(sql, [userId,userId])
        return  messageLogList
       
    '''
    将所有消息标记成已读
    '''    
    def clean_message(self,userId):
        MessageLog.objects.filter(receiver_id=userId,isRead=False).update(isRead=True)
        #系统未读消息
        self.clean_message_12m(userId)
        
    '''
    将群发消息标记成已读消息
    '''   
    def clean_message_12m(self,userId):
        sql='''
        SELECT *
from message u3 
where u3.type=0 and u3.id not in (SELECT u4.message_id from message_log u4) and now()<=u3.expireTime
        '''
        messageList=Message.objects.raw(sql)
        messageLogList=[MessageLog(receiver_id=userId,message_id=message.id,isRead=True) for message in messageList]
        MessageLog.objects.bulk_create(messageLogList)
        
    '''
    
    '''
    def clean_message_121(self,senderId,receiverId):
        userId=None
        if senderId ==ADMIN_ID or receiverId==ADMIN_ID:
            if senderId ==ADMIN_ID:
                userId=receiverId
            else:
                userId=senderId
            self.clean_message_12m(userId)
        sql='''
        update message_log u set isRead=True 
where u.id in (
 select a.id from 
(
select u1.id from message_log u1 LEFT JOIN message u2 on u1.message_id= u2.id 
where u1.isRead=False and u1.receiver_id=%s and u2.sender_id=%s
)a
)
        '''
        connection_to_db_commit(sql,[receiverId,senderId])
    '''
    获取信息列表除了第一行
    '''
    def get_message_list_with_first_row(self,senderId,receiverId):
        sql=''
        if senderId ==ADMIN_ID or receiverId==ADMIN_ID:
            sql='''
            SELECT * from (
SELECT * from (
SELECT null as id1,3 as receiver_id,null as message_id,null as isDeleteSender,
null as isDeletereceiver ,null as isRead, u3.* ,null as receiverName,u4.username as senderName 
from message u3 INNER JOIN  auth_user u4 on u4.id=u3.sender_id
where u3.type=0 and u3.id not in (SELECT u4.message_id from message_log u4) and now()<=u3.expireTime 
UNION
SELECT u1.*,u2.*,u3.username as receiverName,u4.username as senderName from message_log u1 LEFT JOIN message u2 on u1.message_id=u2.id
INNER JOIN auth_user u3 on u1.receiver_id=u3.id INNER JOIN auth_user u4 on u2.sender_id=u4.id
where  (isDeletereceiver = False  AND receiver_id in(%s,%s) and sender_id in(%s,%s))
) s
ORDER BY sendTime desc
LIMIT 1,100
)s1

            '''
            return connection_to_db(sql,param=[senderId,receiverId,senderId,receiverId],type=True)
        else:
            sql='''
            SELECT * from (
            SELECT u1.id as id1,receiver_id, message_id,isDeleteSender,null as isDeletereceiver , isRead,u2.*,u3.username as receiverName,u4.username as senderName 
from message_log u1 LEFT JOIN message u2 on u1.message_id=u2.id
INNER JOIN auth_user u3 on u1.receiver_id=u3.id INNER JOIN auth_user u4 on u2.sender_id=u4.id
where  (isDeletereceiver = False  AND receiver_id in(%s,%s) and sender_id in(%s,%s))
ORDER BY sendTime desc
limit 1,100
)s
            '''
            return connection_to_db(sql,param=[senderId,receiverId,senderId,receiverId],type=True)
class MessageLog(models.Model):
    receiver=models.ForeignKey(User,verbose_name=u'收信人',related_name="message_to")
    message=models.ForeignKey(Message,verbose_name=u'消息表')
    '''
    isDeleteSender,idDeleteSender:
                 接收者，发送者删除
      false-----默认,未删
        true---删除
    '''
    isDeleteSender=models.NullBooleanField(verbose_name="发信人删除",default=False)
    isDeletereceiver=models.NullBooleanField(verbose_name="收信删除状态",default=False)
    #接收者是否读件
    isRead=models.NullBooleanField(verbose_name="是否阅读",default=False)
    objects=MessageLogManger()
    
    class Meta:
        verbose_name = u'消息记录表' 
        verbose_name_plural = u'消息记录表'
        db_table = "message_log" 
