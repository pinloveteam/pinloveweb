# # -*- coding: utf-8 -*-
'''
Created on 2014年6月26日

@author: jin
'''
from apps.message_app.models import MessageLog, Message
'''
获取未读信息
'''
def get_no_read_message_count(userId):
    #获取未读消息的数量
    count=MessageLog.objects.get_no_read_msessge_count(userId)[0]
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
添加一条系统消息
一对一
'''
def add_system_message_121(senderId,receiverId,content):
    message=Message(sender_id=senderId,content=content,type=0)
    message.save()
    MessageLog(receiver_id=receiverId,message=message)
    return message
    
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
            MessageLog.objects.clean_message_by_ids(userId,args[key])
        if key=='dynamicComent':
            from apps.friend_dynamic_app.method import clean_dynamic_comment_by_ids
            clean_dynamic_comment_by_ids(args[key])
        if key=='dynamicArgee':
            from apps.friend_dynamic_app.method import clean_dynamic_argee_by_ids
            clean_dynamic_argee_by_ids(args[key])