# -*- coding: utf-8 -*-
'''
Created on Sep 8, 2013

@author: jin
'''
from django.shortcuts import render
from django.core.exceptions import ValidationError
from util.page import page
from apps.message_app.models import  Message, MessageLog
from django.http.response import Http404, HttpResponse
from django.utils import simplejson
import datetime
from apps.user_app.models import UserProfile
import logging
from django.db import transaction
from django.db.models.query_utils import Q
from pinloveweb.settings import ADMIN_ID
from apps.message_app.method import add_system_message_121
logger=logging.getLogger(__name__)
###############################
##1.0
'''
初始化个人消息
'''
def message(request,template_name):
    args={}
    user=request.user
    userProfile=UserProfile.objects.get(user=user)
    #获得所有我和所有用户之间的最近私信一条不是我发送的私信
    messageList=MessageLog.objects.get_message_list(user.id)
    args=page(request,messageList)
    messageList=args['pages']
    from apps.pojo.message import MessageLog_to_MessageBean
    messageList.object_list=MessageLog_to_MessageBean(messageList.object_list,request.user.id,type=1)
    #最近一条系统消息
#     notify=Notify.objects.select_related('sender','receiver').filter(Q(receiver_id=user.id,type='0')|Q(sender_id=user.id,type='0')).order_by('-sendTime')[:1]
#     if len(notify)>0:
#         from apps.pojo.notify import Notify_to_NotifyBean
#         notify=Notify_to_NotifyBean(notify,user.id,type=1)[0]
#     args['notify']=notify
    if request.REQUEST.get('ajax',False):
        data={}
        data['messageList']=messageList.object_list
        data['has_next']=messageList.has_next()
        if messageList.has_next():
            data['next_page_number']=messageList.next_page_number()
        from apps.pojo.message import MessageBeanEncoder
        json=simplejson.dumps(data,cls=MessageBeanEncoder)
        return HttpResponse(json)
    args['pages']=messageList
    from pinloveweb.method import init_person_info_for_card_page
    args.update(init_person_info_for_card_page(userProfile))
    return render(request,template_name,args)


'''
获取我和指定异性之间所有私信
'''    
def message_detail(request):
    args={}
    try:
        senderId=int(request.REQUEST.get('senderId',False))
        receiverId=int(request.REQUEST.get('receiverId',False))
#         id=int(request.REQUEST.get('id',False))
        if senderId and senderId :
            messageList=MessageLog.objects.get_message_list_with_first_row(senderId,receiverId)
            messageList=page(request,messageList)['pages']
            from apps.pojo.message import MessageLog_to_MessageBean
            messageList.object_list=MessageLog_to_MessageBean(messageList.object_list,request.user.id,type=1)
            args['messageList']=messageList.object_list
            args['has_next']=messageList.has_next()
            if messageList.has_next():
                args['next_page_number']=messageList.next_page_number()
            args['result']='success'
            args['userId']=request.user.id
            #标记已读
            from apps.message_app.method import clean_message_by_user,get_no_read_message_count
            clean_message_by_user(senderId,receiverId)
            args['messageCount']=get_no_read_message_count(receiverId)
        else:
            args={'result':'error','error_message':'传递参数出错!'}
        from apps.pojo.message import MessageBeanEncoder
        json=simplejson.dumps(args,cls=MessageBeanEncoder)
        return HttpResponse(json)
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
    
    
# def notify_detail(request):
#     args={}
#     try:
#         senderId=int(request.REQUEST.get('senderId',False))
#         receiverId=int(request.REQUEST.get('receiverId',False))
#         id=int(request.REQUEST.get('id',False))
#         if senderId and senderId and id:
#             notifyList=Notify.objects.filter(sender_id__in=[senderId,receiverId],receiver_id__in=[senderId,receiverId]).exclude(id=id).order_by('-sendTime')
#             notifyList=page(request,notifyList)['pages']
#             from apps.pojo.notify import Notify_to_NotifyBean
#             notifyList.object_list=Notify_to_NotifyBean(notifyList.object_list,request.user.id)
#             args['messageList']=notifyList.object_list
#             args['has_next']=notifyList.has_next()
#             if notifyList.has_next():
#                 args['next_page_number']=notifyList.next_page_number()
#             args['result']='success'
#             args['userId']=request.user.id
#             #标记已读
#             from apps.message_app.method import clean_message_by_user,get_no_read_message_count
#             clean_message_by_user(receiverId,'notify')
#             args['messageCount']=get_no_read_message_count(receiverId)
#         else:
#             args={'result':'error','error_message':'传递参数出错!'}
#         from apps.pojo.notify import NotifyBeanEncoder
#         json=simplejson.dumps(args,cls=NotifyBeanEncoder)
#         return HttpResponse(json)
#     except Exception as e:
#         logger.exception('获取我和指定异性之间所有私信出错，出错原因')
#         args={'result':'error','error_message':'获取我和指定异性之间所有私信出错!'}
#         json=simplejson.dumps(args)
#         return HttpResponse(json)

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
        receiver_id=request.GET.get('receiver_id')
        reply_content=request.GET.get('reply_content')
        add_system_message_121(user.id,receiver_id,reply_content)
        args={'result':'success'}   
    except Exception ,e:    
        logger.error('私信   发送,出粗')
        args={'result':'error','error_message':'发送私信出错!'}   
    json = simplejson.dumps(args)
    return HttpResponse(json)
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
    
'''
根据id获取信息
attribute：
   userIdList：用户id列表
return：
  messageList：列表
'''
def get_messge_by_id(request):
    userIdString=request.GET.get('userIdList')
    userIdList=[int(x) for x in userIdString.split(',')]
    excludeMessageList=[]
    if 'messageList' in request.session.keys():
        excludeMessageList=request.session['messageList']
    messageList=Message.objects.filter( receiver=request.user,isRead=False,isDeletereceiver=False).exclude(id__in=excludeMessageList)
    for message in messageList:
        excludeMessageList.append(message.id)
    request.session['messageList']=excludeMessageList
    result=[message.as_json_for_id_conent() for message in messageList ]
    json = simplejson.dumps(result)
    return HttpResponse(json, mimetype="application/json")

'''
获得所有未读消息
'''
def get_noread_messges_by_userid(request):
    userId=request.GET.get('userId')
    user=request.user
    #获取未读的message和最近发出的三条message
    sqlList=[user.id,userId,0,0,userId,user.id]
    messageList=Message.objects.raw('SELECT * from message where receiver_id=%s and sender_id=%s and isRead=%s and isDeletereceiver=%s or id in(select id from (SELECT id from message m where m.receiver_id=%s and m.sender_id=%s ORDER BY sendTime DESC  limit 3) as s) ORDER BY sendTime',
                                sqlList)
# messageList=Message.objects.filter(receiver_id=request.user,sender_id=userId,isRead=False,isDeletereceiver=False).order_by('sendTime')
    result=[message.as_json_for_id_conent() for message in messageList ]
    json = simplejson.dumps(result)
    return HttpResponse(json, mimetype="application/json")

