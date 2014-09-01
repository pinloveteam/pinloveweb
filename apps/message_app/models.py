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
获取未读消息，动态评论的列表数量
'''
def get_no_read_message_dynamic_list_count(receiverId):  
    sql='''
    SELECT count(*) from(
SELECT u2.id,u2.sender_id,u3.username as sender_name,u4.avatar_name,u4.avatar_name_status,u1.receiver_id,u2.content,u2.sendTime,u2.type,u1.isRead,
null as friendDynamic_id,null as friendDynamic_content  ,null as data
from message_log u1 LEFT JOIN message u2 on u1.message_id=u2.id 
LEFT JOIN auth_user u3 on u3.id=u2.sender_id LEFT JOIN user_profile u4 on u4.user_id=u2.sender_id
where  isDeletereceiver = False  and u1.isRead=False  AND receiver_id =%s
UNION
SELECT u3.id,u3.sender_id,u1.username as sender_name,u4.avatar_name,u4.avatar_name_status,%s as receiver_id,u3.content,u3.sendTime,u3.type,0 as isRead,
null as friendDynamic_id,null as friendDynamic_content ,null as data
from message u3 LEFT JOIN auth_user u1 on u1.id=u3.sender_id LEFT JOIN user_profile u4 on u4.user_id=u3.sender_id
where u3.type=0 and u3.id not in (SELECT u4.message_id from message_log u4 where u4.receiver_id=%s) and now()<=u3.expireTime
UNION
SELECT u1.id,u1.reviewer_id as sender_id ,u3.username as sender_name,u4.avatar_name,u4.avatar_name_status,
u1.receiver_id,u1.content,u1.commentTime as sendTime ,5 as type,u1.isRead,
u1.friendDynamic_id,u2.content as friendDynamic_content ,u2.data
from friend_dynamic_comment u1  LEFT JOIN friend_dynamic u2 on u2.id=u1.friendDynamic_id
LEFT JOIN auth_user u3 on u3.id=u1.reviewer_id LEFT JOIN user_profile u4 on u4.user_id=u1.reviewer_id
WHERE u1.receiver_id=%s and u1.isRead=0
UNION
SELECT u1.id,u1.user_id as sender_id ,u3.username as sender_name,u4.avatar_name,u4.avatar_name_status,
u2.publishUser_id as receiver_id,null as content,u1.time as sendTime ,3 as type,u1.isRead,
u1.friendDynamic_id,u2.content as friendDynamic_content ,u2.data
from friend_dynamic_argee u1  LEFT JOIN friend_dynamic u2 on u2.id=u1.friendDynamic_id
LEFT JOIN auth_user u3 on u3.id=u1.user_id LEFT JOIN user_profile u4 on u4.user_id=u1.user_id
WHERE u2.publishUser_id=%s and u1.isRead=0
)s 
    '''
    result=connection_to_db(sql,param=[receiverId,receiverId,receiverId,receiverId,receiverId])
    return result[0][0]
     
'''
获取消息，动态评论的列表
@param receiverId:接收用户id 
@param isRead:是否已读 
'''
def get_message_dynamic_list(receiverId,isRead):
    if isRead ==False:
        sql='''
    SELECT * from(
SELECT u2.id,u2.sender_id,u3.username as sender_name,u4.avatar_name,u4.avatar_name_status,u1.receiver_id,u2.content,u2.sendTime,u2.type,u1.isRead,
null as friendDynamic_id,null as friendDynamic_content  ,null as data
from message_log u1 LEFT JOIN message u2 on u1.message_id=u2.id 
LEFT JOIN auth_user u3 on u3.id=u2.sender_id LEFT JOIN user_profile u4 on u4.user_id=u2.sender_id
where  isDeletereceiver = False  and u1.isRead=False  AND receiver_id =%s
UNION
SELECT u3.id,u3.sender_id,u1.username as sender_name,u4.avatar_name,u4.avatar_name_status,%s as receiver_id,u3.content,u3.sendTime,u3.type,0 as isRead,
null as friendDynamic_id,null as friendDynamic_content ,null as data
from message u3 LEFT JOIN auth_user u1 on u1.id=u3.sender_id LEFT JOIN user_profile u4 on u4.user_id=u3.sender_id
where u3.type=0 and u3.id not in (SELECT u4.message_id from message_log u4 where u4.receiver_id=%s) and now()<=u3.expireTime
UNION
SELECT u1.id,u1.reviewer_id as sender_id ,u3.username as sender_name,u4.avatar_name,u4.avatar_name_status,
u1.receiver_id,u1.content,u1.commentTime as sendTime ,5 as type,u1.isRead,
u1.friendDynamic_id,u2.content as friendDynamic_content ,u2.data
from friend_dynamic_comment u1  LEFT JOIN friend_dynamic u2 on u2.id=u1.friendDynamic_id
LEFT JOIN auth_user u3 on u3.id=u1.reviewer_id LEFT JOIN user_profile u4 on u4.user_id=u1.reviewer_id
WHERE u1.receiver_id=%s and u1.isRead=0
UNION
SELECT u1.id,u1.user_id as sender_id ,u3.username as sender_name,u4.avatar_name,u4.avatar_name_status,
u2.publishUser_id as receiver_id,null as content,u1.time as sendTime ,3 as type,u1.isRead,
u1.friendDynamic_id,u2.content as friendDynamic_content ,u2.data
from friend_dynamic_argee u1  LEFT JOIN friend_dynamic u2 on u2.id=u1.friendDynamic_id
LEFT JOIN auth_user u3 on u3.id=u1.user_id LEFT JOIN user_profile u4 on u4.user_id=u1.user_id
WHERE u2.publishUser_id=%s and u1.isRead=0
)s 
ORDER BY sendTime desc
    '''
    else:
        sql='''
   SELECT * from(
SELECT u2.id,u2.sender_id,u3.username as sender_name,u4.avatar_name,u4.avatar_name_status,u1.receiver_id,u2.content,u2.sendTime,u2.type,u1.isRead,
null as friendDynamic_id,null as friendDynamic_content  ,null as data
from message_log u1 LEFT JOIN message u2 on u1.message_id=u2.id 
LEFT JOIN auth_user u3 on u3.id=u2.sender_id LEFT JOIN user_profile u4 on u4.user_id=u2.sender_id
where  isDeletereceiver = False  AND receiver_id =%s
UNION
SELECT u3.id,u3.sender_id,u1.username as sender_name,u4.avatar_name,u4.avatar_name_status,%s as receiver_id,u3.content,u3.sendTime,u3.type,0 as isRead,
null as friendDynamic_id,null as friendDynamic_content ,null as data
from message u3 LEFT JOIN auth_user u1 on u1.id=u3.sender_id LEFT JOIN user_profile u4 on u4.user_id=u3.sender_id
where u3.type=0 and u3.id not in (SELECT u4.message_id from message_log u4 where u4.receiver_id=%s) and now()<=u3.expireTime
UNION
SELECT u1.id,u1.reviewer_id as sender_id ,u3.username as sender_name,u4.avatar_name,u4.avatar_name_status,
u1.receiver_id,u1.content,u1.commentTime as sendTime ,5 as type,u1.isRead,
u1.friendDynamic_id,u2.content as friendDynamic_content ,u2.data
from friend_dynamic_comment u1  LEFT JOIN friend_dynamic u2 on u2.id=u1.friendDynamic_id
LEFT JOIN auth_user u3 on u3.id=u1.reviewer_id LEFT JOIN user_profile u4 on u4.user_id=u1.reviewer_id
WHERE u1.receiver_id=%s 
UNION
SELECT u1.id,u1.user_id as sender_id ,u3.username as sender_name,u4.avatar_name,u4.avatar_name_status,
u2.publishUser_id as receiver_id,null as content,u1.time as sendTime ,3 as type,u1.isRead,
u1.friendDynamic_id,u2.content as friendDynamic_content ,u2.data
from friend_dynamic_argee u1  LEFT JOIN friend_dynamic u2 on u2.id=u1.friendDynamic_id
LEFT JOIN auth_user u3 on u3.id=u1.user_id LEFT JOIN user_profile u4 on u4.user_id=u1.user_id
WHERE u2.publishUser_id=%s 
)s 
ORDER BY sendTime desc
    '''
    return connection_to_db(sql,param=[receiverId,receiverId,receiverId,receiverId,receiverId],type=True)
        
'''
系统消息
'''
class Message(models.Model):
    sender=models.ForeignKey(User,verbose_name=u'发信人',related_name="message_from")
    content=models.TextField(verbose_name="内容")
    sendTime=models.DateTimeField(verbose_name="发出时间")
    TYPE_CHOICES=((0,u'单发系统消息'),(1,u'私信'),(2,u'加好友'),(4,u'群发系统消息'))
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
    def get_message_list(self,userId,first=None,end=None): 
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
GROUP BY sender_id  '''
        if first is not None:
            sql=sql+'limit %s , %s'%(first,end)
        return  connection_to_db(sql,param=[userId,userId,userId],type=True)
    
    '''
    获得两个用户之间的私信
    '''
    def get_message_list_121(self,userId,otherId,first=None,end=None): 
        sql='''
   
SELECT u1.*,u2.*,u3.username as receiverName,u4.username as senderName from message_log u1 LEFT JOIN message u2 on u1.message_id=u2.id
INNER JOIN auth_user u3 on u1.receiver_id=u3.id INNER JOIN auth_user u4 on u2.sender_id=u4.id
where  isDeletereceiver = False  AND receiver_id in (%s,%s) and sender_id in (%s,%s)
ORDER BY sendTime DESC
 '''
        if first is not None:
            sql=sql+'limit %s , %s'%(first,end)
        return  connection_to_db(sql,param=[userId,otherId,userId,otherId],type=True)
    
    '''
获得两个用户的未读私信
    '''
    def get_nr_message_list_121(self,receiverId,senderId,first=None,end=None): 
        sql='''
   
SELECT u1.*,u2.*,u3.username as receiverName,u4.username as senderName from message_log u1 LEFT JOIN message u2 on u1.message_id=u2.id
INNER JOIN auth_user u3 on u1.receiver_id=u3.id INNER JOIN auth_user u4 on u2.sender_id=u4.id
where  isDeletereceiver = False  AND receiver_id in (%s,%s) and sender_id in (%s,%s)
and u2.sendTime >=(
SELECT sendTime 
from message_log m1  LEFT JOIN message m2 on m1.message_id=m2.id
where isDeletereceiver = False  and isRead=False and m1.receiver_id=%s and m2.sender_id=%s
ORDER BY sendTime
limit 0,1
)
ORDER BY sendTime DESC
 '''
        if first is not None:
            sql=sql+'limit %s , %s'%(first,end)
        return  connection_to_db(sql,param=[receiverId,senderId,receiverId,senderId,receiverId,senderId,],type=True)
   
       
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
    def get_no_read_messagelog(self,userId,first=None,end=None):
        sql='''
        SELECT * from (
SELECT u2.id,u2.sender_id,u3.username as sender_name,u4.avatar_name,u4.avatar_name_status,u1.receiver_id,u2.content,u2.sendTime,u2.type,u1.isRead
from message_log u1 LEFT JOIN message u2 on u1.message_id=u2.id 
LEFT JOIN auth_user u3 on u3.id=u2.sender_id LEFT JOIN user_profile u4 on u4.user_id=u2.sender_id
where  isDeletereceiver = False  AND receiver_id =%s
UNION
SELECT u3.id,u3.sender_id,u1.username as sender_name,u4.avatar_name,u4.avatar_name_status,%s as receiver_id,u3.content,u3.sendTime,u3.type,0 as isRead
from message u3 LEFT JOIN auth_user u1 on u1.id=u3.sender_id LEFT JOIN user_profile u4 on u4.user_id=u3.sender_id
where u3.type=0 and u3.id not in (SELECT u4.message_id from message_log u4) and now()<=u3.expireTime
) s
ORDER BY sendTime desc
        '''
        if first is not None :
            sql=sql+'  limit %s , %s'%(first,end)
        return connection_to_db(sql,param=[userId,userId],type=True)
       
       
    '''
    获取消息列表
    '''
    def messagelog_list(self,userId,first=None,end=None):
        sql='''
        SELECT * from (
SELECT u2.id,u2.sender_id,u3.username as sender_name,u4.avatar_name,u4.avatar_name_status,u1.receiver_id,u2.content,u2.sendTime,u2.type,u1.isRead
from message_log u1 LEFT JOIN message u2 on u1.message_id=u2.id 
LEFT JOIN auth_user u3 on u3.id=u2.sender_id LEFT JOIN user_profile u4 on u4.user_id=u2.sender_id
where  receiver_id =%s
) s
ORDER BY sendTime desc
        '''
        if first is not None :
            sql=sql+'  limit %s , %s'%(first,end)
        return connection_to_db(sql,param=[userId],type=True)
    
    '''
    根据发送者id和接受者id获取消息详情
    @param senderId:发送者id
    @param receiver_id:接受者id 
    '''
    def messagelog_list_by_userid(self,senderId,receiver_id,first=None,end=None):
        sql='''
        SELECT * from (
SELECT u2.id,u2.sender_id,u3.username as sender_name,u4.avatar_name,u4.avatar_name_status,u1.receiver_id,u2.content,u2.sendTime,u2.type,u1.isRead
from message_log u1 LEFT JOIN message u2 on u1.message_id=u2.id 
LEFT JOIN auth_user u3 on u3.id=u2.sender_id LEFT JOIN user_profile u4 on u4.user_id=u2.sender_id
where  receiver_id in(%s,%s) and sender_id in(%s,%s)
) s
ORDER BY sendTime desc
        '''
        if first is not None :
            sql=sql+'  limit %s , %s'%(first,end)
        return connection_to_db(sql,param=[senderId,receiver_id,senderId,receiver_id],type=True)
    
    '''
    未读关注消息数量
    '''
    def get_no_read_follow_message_count(self,userId):
        sql='''
        SELECT count(*)
from message_log u1 LEFT JOIN message u2 on u1.message_id=u2.id 
LEFT JOIN auth_user u3 on u3.id=u2.sender_id LEFT JOIN user_profile u4 on u4.user_id=u2.sender_id
where  isDeletereceiver = False  AND receiver_id =%s and type=2 and isRead=0
        '''
        return connection_to_db(sql,param=[userId,])[0][0]
        
    '''
    关注消息列表
    '''
    def get_follow_message_list(self,userId,isRead,first=None,end=None):
        sql='''
        SELECT u2.id,u2.sender_id,u3.username as sender_name,u4.avatar_name,u4.avatar_name_status,u1.receiver_id,u2.content,u2.sendTime,u2.type,u1.isRead
from message_log u1 LEFT JOIN message u2 on u1.message_id=u2.id 
LEFT JOIN auth_user u3 on u3.id=u2.sender_id LEFT JOIN user_profile u4 on u4.user_id=u2.sender_id
where  isDeletereceiver = False  AND receiver_id =%s and type=2 and isRead=%s
ORDER BY sendTime desc
        '''
        if first is not None :
            sql=sql+'  limit %s , %s'%(first,end)
        return connection_to_db(sql,param=[userId,isRead],type=True)
    
    '''
    将消息标记成已读
    '''
    def clean_message_by_ids(self,userId,Ids):
        sql='''
        SELECT id
from message u3 
where u3.type=0 and u3.id not in (SELECT u4.message_id from message_log u4 where u4.receiver_id=%s ) and now()<=u3.expireTime  '''
        sql=sql+'and id in ('+('%s,'*len(Ids))[:-1]+')'
        paramList=[userId]
        paramList.extend(Ids)
        ressult=connection_to_db(sql,paramList)
        if len(ressult)>0:
            messageLogList=[]
            for i in ressult:
              messageLog=MessageLog(receiver_id=userId,message_id=i[0],isRead=True)
              messageLogList.append(messageLog)
            MessageLog.objects.bulk_create(messageLogList)
        MessageLog.objects.filter(receiver_id=userId,message_id__in=Ids).update(isRead=True)
        
        
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
where u3.type=0 and u3.id not in (SELECT u4.message_id from message_log u4 where u4.receiver_id=%s ) and now()<=u3.expireTime
        '''
        messageList=Message.objects.raw(sql,[userId])
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
