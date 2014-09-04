# -*- coding: utf-8 -*-
'''
Created on Sep 8, 2013

@author: jin
'''
from django.shortcuts import render
from django.core.exceptions import ValidationError
from util.page import page
from apps.message_app.models import  Message, MessageLog
from django.http.response import  HttpResponse
from django.utils import simplejson
from apps.user_app.models import UserProfile
import logging
from django.db import transaction
from apps.message_app.method import add_message_121
from pinloveweb.settings import ADMIN_ID
logger=logging.getLogger(__name__)
###############################
##1.0
'''
初始化个人消息
'''
def message(request,template_name):
    args={}
    isRad=False
    user=request.user
    from apps.message_app.models import get_no_read_message_dynamic_list_count,get_message_dynamic_list
    if get_no_read_message_dynamic_list_count(user.id)>0:
        messageDynamicList=get_message_dynamic_list(user.id,False)
    else:
        messageDynamicList=get_message_dynamic_list(user.id,True)
        isRad=True
    pages=page(request,messageDynamicList)
    if not isRad: 
        #标记成已读
        from apps.message_app.method import clean_message_Dynamic
        clean_message_Dynamic(user.id,pages['pages'].object_list)
    from apps.pojo.message import messagedynamics_to_message_page
    messageDynamicsList=messagedynamics_to_message_page(pages['pages'].object_list)
    if pages['pages'].has_next():
        #如果为未读
        if not  pages['pages'].object_list[0]['isRead']:
            args['next_page_number']=1
        else:
            args['next_page_number']=pages['pages'].next_page_number()
    else:
        pages['next_page_number']=-1
    args['messageList']=simplejson.dumps(messageDynamicsList)
    #获取未读信息条数
    from pinloveweb.method import get_no_read_web_count
    args.update(get_no_read_web_count(user.id,fromPage=u'message'))
    if request.is_ajax():
        json=simplejson.dumps(args)
        return HttpResponse(json)
    return render(request,template_name,args)
    
'''
用户私信列表
'''
def message_list(request,template_name):
    args={}
    try:
            if MessageLog.objects.get_no_read_private_msessge_count(request.user.id)>0:
                messageLogList=MessageLog.objects.get_no_read_messagelog(request.user.id)
                data=page(request,messageLogList)
                MessageIds=[messageLog['id'] for messageLog in data['pages'].object_list]
                MessageLog.objects.filter(id__in=MessageIds).update(isRead=True)
            else:
                messageLogList=MessageLog.objects.messagelog_list(request.user.id)
                data=page(request,messageLogList)
            from apps.pojo.message import messagedynamics_to_message_page
            messageList=messagedynamics_to_message_page(data['pages'].object_list)
            args['messageList']=simplejson.dumps(messageList)
            if data['pages'].has_next():
                #如果为未读
                if data['pages'].object_list[0]['isRead']:
                    args['next_page_number']=1
                else:
                    args['next_page_number']=data['pages'].next_page_number()
            else:
                data['next_page_number']=-1
            #获取未读信息条数
            from pinloveweb.method import get_no_read_web_count
            args.update(get_no_read_web_count(request.user.id,fromPage=u'message'))
            if request.is_ajax():
                json=simplejson.dumps(args)
                return HttpResponse(json)  
            else:
                args['user']=request.user
                from apps.user_app.method import get_avatar_name
                args['avatar_name']=get_avatar_name(request.user.id,request.user.id)  
                return render(request,template_name,args)
            
    except Exception ,e:
        logger.exception('私信列表私信列表出错!')
        args={'result':'error','error_message':'私信列表出错'}
        json=simplejson.dumps(args)
        return HttpResponse(json)

'''
关注消息列表
'''
def get_follow_message(request,template_name):
    args={}
    try:
            if MessageLog.objects.get_no_read_follow_message_count(request.user.id)>0:
                followList=MessageLog.objects.get_follow_message_list(request.user.id,0)
                data=page(request,followList)
                MessageIds=[messageLog['id'] for messageLog in data['pages'].object_list]
                MessageLog.objects.filter(message_id__in=MessageIds).update(isRead=True)
            else:
                followList=MessageLog.objects.get_follow_message_list(request.user.id,1)
                data=page(request,followList)
            from apps.pojo.message import messagedynamics_to_message_page
            messageList=messagedynamics_to_message_page(data['pages'].object_list)
            args['messageList']=simplejson.dumps(messageList)
            if data['pages'].has_next():
                #如果为未读
                if data['pages'].object_list[0]['isRead']:
                    args['next_page_number']=1
                else:
                    args['next_page_number']=data['pages'].next_page_number()
            else:
                args['next_page_number']=-1
            from pinloveweb.method import get_no_read_web_count
            args.update(get_no_read_web_count(request.user.id,fromPage=u'message'))
            if request.is_ajax():
                json=simplejson.dumps(args)
                return HttpResponse(json)
            else:
                args['user']=request.user
                from apps.user_app.method import get_avatar_name
                args['avatar_name']=get_avatar_name(request.user.id,request.user.id)  
                return render(request,template_name,args)
    except Exception ,e:
        logger.exception('关注消息列表出错!')
        args={'result':'error','error_message':'私信列表私信列表出错'}
        json=simplejson.dumps(args)
        return HttpResponse(json)
       
'''
获取我和指定异性之间所有私信
'''    
def message_detail(request,template_name):
    args={}
    try:
        senderId=int(request.REQUEST.get('senderId',False))
        if senderId and senderId :
            messageList=MessageLog.objects.messagelog_list_by_userid(senderId,request.user.id)
            data=page(request,messageList)
            from apps.pojo.message import messagedynamics_to_message_page
            messageList=messagedynamics_to_message_page(data['pages'].object_list)
            args['messageList']=simplejson.dumps(messageList)
            args['userId']=request.user.id
            args['userusername']=request.user.username
            args['senderId']=senderId
            from apps.user_app.method import get_avatar_name
            args['avatarName']=get_avatar_name(request.user.id,request.user.id)
            if data['pages'].has_next():
                args['next_page_number']=data['pages'].next_page_number()
            else:
                args['next_page_number']=-1
            args['userId']=request.user.id
            #标记已读
            from apps.message_app.method import clean_message_by_user
            clean_message_by_user(senderId,request.user.id)
        else:
            args={'result':'error','error_message':'传递参数出错!'}
        if request.is_ajax():
            from apps.pojo.message import MessageBeanEncoder
            json=simplejson.dumps(args,cls=MessageBeanEncoder)
            return HttpResponse(json)
        else:
            return render(request,template_name,args)
    except Exception as e:
        print '%s%s' %('获取我和指定异性之间所有私信出错，出错原因',e)
        args={'result':'error','error_message':'获取我和指定异性之间所有私信出错!'}
        json=simplejson.dumps(args)
        return HttpResponse(json)
    
    
'''
回复私信
attribute：
     receiver_id(int)： 接收者id
     reply_content(text)： 回复内容
return ：
     
'''   
@transaction.commit_on_success
def message_reply(request):  
    args={}
    try:
        if request.method=="POST":
            receiver_id=request.POST.get('receiverId')
            content=request.POST.get('content')
            type=1
            if receiver_id==ADMIN_ID:
                type=0
            message=Message(sender_id=request.user.id,content=content,type=type)
            message.save()
            messageLog=MessageLog(receiver_id=receiver_id,message=message)
            messageLog.save()
            from apps.pojo.message import MessageLog_to_Message
            messageBean=MessageLog_to_Message([messageLog,],request.user.id,type=1)
            from apps.pojo.message import MessageBeanEncoder
                
            args={'result':'success','message':'发送成功!','messageBean':messageBean}
        else:
            args={'result':'success','error_message':'提交参数出错!'}  
        json=simplejson.dumps(args,cls=MessageBeanEncoder)
        return HttpResponse(json)
       
    except Exception as e:
        logger.exception('获取我和指定异性之间所有私信出错!')
        args={'result':'error','error_message':'获取我和指定异性之间所有私信出错!'}
        json=simplejson.dumps(args)
        return HttpResponse(json)
    
    

'''
获取信息数量
'''
def count(request):
    arg={}
    if request.is_ajax():
        from apps.message_app.method import get_no_read_message_count
        count=get_no_read_message_count(request.user.id)
        arg['count']=count
        json=simplejson.dumps(arg)
        return HttpResponse(json)
    else:
        return render(request,'error.html')
    
'''
全部标记成已读
'''    
def clean(request):
    args={}
    try:
        from apps.message_app.method import clean_message
        clean_message(request.user.id)
        args={'result':'success'}
    except Exception as e:
       logger.exception('全部标记成已读,出错!')
       args={'result':'error','error_message':e.message}
    json=simplejson.dumps(args)
    return HttpResponse(json)
    
'''
获取用户未读消息
'''   
def no_read_message(request,template_name):
    args={}
    try:
        messageList=MessageLog.objects.get_no_read_messagelog(request.user.id)
        args=page(request,messageList)
        messageList=args['pages']
        from apps.pojo.message import MessageLog_to_Message
        messageList.object_list=MessageLog_to_Message(messageList.object_list,request.user.id)
        #用户消息标记为已读
        MessageLog.objects.clean_message(request.user.id)
        if request.is_ajax():
            data={}
            data['messageList']=messageList.object_list
            data['has_next']=messageList.has_next()
            if messageList.has_next():
                data['next_page_number']=messageList.next_page_number()
            from apps.pojo.message import MessageBeanEncoder
            json=simplejson.dumps(data,cls=MessageBeanEncoder)
            return HttpResponse(json)
        args['pages']=messageList
        userProfile=UserProfile.objects.get(user_id=request.user.id)
        from pinloveweb.method import init_person_info_for_card_page
        args.update(init_person_info_for_card_page(userProfile))
        args['from']='no_read_message'
        return render(request,template_name,args)
    except Exception,e:
        error_mesage='获取用户未读消息,出错!'
        logger.exception(error_mesage)
    
'''
私信   发送
attribute：
     receiver_id(int)： 接收者id
     reply_content(text)： 回复内容
return ：
     
'''   
def message_send(request):  
    args={}
    try:
        user=request.user
        receiver_id=request.REQUEST.get('receiver_id')
        reply_content=request.REQUEST.get('reply_content')
        message=add_message_121(user.id,receiver_id,reply_content,1)
        args={'result':'success','messageTime':message.sendTime.strftime("%m-%d %H:%M")}  
    except Exception ,e:    
        logger.error('私信   发送,出粗')
        args={'result':'error','error_message':'发送私信出错!'}   
    json = simplejson.dumps(args)
    return HttpResponse(json)

'''
获得最近三条消息
'''
def get_noread_messges_by_userid(request):
    userId=request.GET.get('userId')
    user=request.user
    messageList=MessageLog.objects.get_nr_message_list_121(user.id,userId)
    if len(messageList)==0:
        #获取未读的message和最近发出的三条message
        messageList=MessageLog.objects.get_message_list_121(user.id,userId,first=0,end=3)
    from util.util import regex_expression
    result=[{'sender_id':message['sender_id'],'receiver_id':message['receiver_id'],'content':regex_expression(message['content'])} for message in messageList ]
    result=result[::-1]
    json = simplejson.dumps(result)
    return HttpResponse(json, mimetype="application/json")


'''
根据id获取未读信息
@param userIds: 用户id集合的字符串
@param num: 未读消息数量
@return: messageList：列表
  
'''
def get_no_read_messge_by_ids(request):
    args={}
    try:
        userIdString=request.REQUEST.get('userIds')
        num=int(request.REQUEST.get('num',False))
        userIdList=[int(x) for x in userIdString.split(',')]
        if num:
            messageLogList=MessageLog.objects.get_no_read_messagelog(request.user.id, 0, num)
            messageList=[messageLog for messageLog in messageLogList if  messageLog['sender_id'] in userIdList]
        else:
            messageList=MessageLog.objects.get_no_read_messagelog(request.user.id)
        MessageLog.objects.filter(message_id__in=[messageTmp['id'] for messageTmp in messageList]).update(isRead=True)
        from apps.pojo.message import MessageLog_to_MessageBean
        messageBeanList=MessageLog_to_MessageBean(messageList,request.user.id)
        args['messageList']=messageBeanList
#         #获取消息数
#         from pinloveweb.method import get_no_read_web_count
#         args.update(get_no_read_web_count(request.user,id))
        from apps.pojo.message import MessageBeanEncoder
        json=simplejson.dumps(args,cls=MessageBeanEncoder)
        return HttpResponse(json)
    except Exception,e:
        logger.exception('根据id获取未读信息,出错!')
        args={'result':'error','error_message':e.message}
        json=simplejson.dumps(args)
        return HttpResponse(json)

def message_test(request):
    return HttpResponse('abc')
##############################


'''
过去消息列表
attribute： 
     type  列表类型(systemNoRead,system,messageNoRead,message)
'''
def list(request):
    arg={}
    if request.user.is_authenticated():
        type=request.GET.get('type').strip()
        if type==u"systemNoRead":
            #获取未读系统消息
            arg['type']='systemNoRead'
            messageList=Notify.objects.filter(type='0',receiver=request.user,isRead=False).order_by('sendTime')
        elif type==u'system':
            #获取系统消息的总数
            arg['type']='system'
            messageList=Notify.objects.filter(type='0',receiver=request.user).order_by('sendTime')
        elif type==u'messageNoRead':
            #获取未读私信消息
            arg['type']=u'messageNoRead'
            messageList=Message.objects.filter(receiver=request.user,isRead=False,isDeletereceiver=False).order_by('sendTime')
            len(messageList)
            Message.objects.filter(receiver=request.user.id,isRead=False,isDeletereceiver=False).update(isRead=True)  
        elif type==u'message':
            #获取全部私信消息
            arg['type']='message'
            
            messageList=Message.objects.raw('SELECT DISTINCT sender_id,id,receiver_id,content,sendTime,count(id) as count from message where isDeleteSender=0  ORDER BY sendTime')
        else:    
            raise ValidationError(u"没有获得type")
        arg=dict(page(request,messageList),**arg)
        if type=='message' or type=='messageNoRead':
            return render(request,'message_list.html',arg)
        else:
            return render(request,'notify_list.html',arg)
    else:
        return render(request, 'login.html', arg,) 

    
'''
  删除系统消息
  attribute：notify_id （int）系统消息id
  return： result（boolean） 删除结果  True:删除成功；False：删除失败
'''
def delete_notify(request):
    try:
        notifyId=request.GET.get('notify_id')
    except:
        result = False 
        json = simplejson.dumps(result)
        return HttpResponse(json)
#     Notify.objects.filter(id=notifyId).delete()
    result = True
    json = simplejson.dumps(result)
    return HttpResponse(json)
    

    
    

    

'''
获得未读的消息个数
attribute：

return：
     systemNoReadCount  (int)：系统未读消息
     messageNoReadCount (int):私信未读消息
'''    
def has_new_message(request):
    arg={}
    if request.user.is_authenticated():
         #获取未读系统消息的数量
        systemNoReadCount=Notify.objects.filter(type='0',receiver=request.user,isRead=False).count()
        #获取未读私信消息的数量
        messageNoReadCount=Message.objects.filter(receiver=request.user,isRead=False,isDeletereceiver=False).count()
        arg['systemNoReadCount']=systemNoReadCount
        arg['messageNoReadCount']=messageNoReadCount
        arg['isLogin']=True
        json = simplejson.dumps(arg)
        return HttpResponse(json)
    else:
        arg['isLogin']=False  
        json = simplejson.dumps(arg)
        return HttpResponse(json)
    



