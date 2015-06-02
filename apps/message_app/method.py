# # -*- coding: utf-8 -*-
'''
Created on 2014年6月26日

@author: jin
'''
from apps.message_app.models import MessageLog, Message
'''
获取未读私信
'''
def get_no_read_private_message_count(userId):
    #获取未读消息的数量
    count=MessageLog.objects.get_no_read_private_msessge_count(userId)
    return count

def get_no_read_follow_message_count(userId):
    count=MessageLog.objects.get_no_read_follow_message_count(userId)
    return count
    
'''
将未读信息标记成已读
'''
def clean_message(userId):
    MessageLog.objects.clean_message(userId)

'''
将两个用户之间的未读消息标记成已读
attridute:
   notify  系统消息
   message 私信
'''
def clean_message_by_user(senderId,receiverId):
       MessageLog.objects.clean_message_121(senderId, receiverId)
    
'''
添加一条消息
一对一
@param type: 0 系统单发消息
            1   私信
            2   加好友
'''
def add_message_121(senderId,receiverId,content,type):
    message=Message(sender_id=senderId,content=content,type=type)
    message.save()
    messageLog=MessageLog(receiver_id=receiverId,message=message)
    messageLog.save()
    return messageLog

    
'''
将消息中心的消息标记成已读
'''
def clean_message_Dynamic(userId,messageDynamicList):
    args={'messageLog':[],'dynamicComent':[],'dynamicArgee':[]}
    for messageDynamic in messageDynamicList:
        if messageDynamic['type']<3:
            args['messageLog'].append(messageDynamic['id'])
        elif  messageDynamic['type']==3:
            args['dynamicArgee'].append(messageDynamic['id'])
        elif messageDynamic['type']==5:
            args['dynamicComent'].append(messageDynamic['id'])
    for key in args.keys():
        if key=='messageLog':
            if len(args[key])>0:
                MessageLog.objects.clean_message_by_ids(userId,args[key])
        if key=='dynamicComent':
            from apps.friend_dynamic_app.method import clean_dynamic_comment_by_ids
            clean_dynamic_comment_by_ids(args[key])
        if key=='dynamicArgee':
            from apps.friend_dynamic_app.method import clean_dynamic_argee_by_ids
            clean_dynamic_argee_by_ids(args[key])