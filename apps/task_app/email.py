# -*- coding: utf-8 -*-
'''
Created on 2015年4月2日

@author: jin
'''
from apps.user_app.models import UserProfile
from util.email import Email
from pinloveweb.settings import WEBSITE
from apps.task_app.models import EmailRecommendHistory
import logging
from boto.exception import BotoServerError
from apps.message_app import models 
from apps.message_app.models import MessageLog
from apps.friend_dynamic_app.models import FriendDynamicComment,\
    FriendDynamicArgee
logger=logging.getLogger(__name__)
def send_notify_email(userIdList=None):
    if userIdList is None:
        userProfileList=UserProfile.objects.select_related('user').all()
    else:
        userProfileList=UserProfile.objects.select_related('user').filter(user_id__in=userIdList)
    for userProfile in userProfileList:
      try:
        if userProfile.user.email is not None:
            recommendList=UserProfile.objects.get_email_recommed_list(userProfile.user_id,userProfile.gender)
            if recommendList=='less':
                raise Exception('推荐人数不足!')
            args={'username':userProfile.user.username,'email':userProfile.user.email,'WEBSITE':WEBSITE}
            args['recommendList']=[{'username':recommend.user.username,'age':recommend.age,'avatar_name':('%s/media/%s-100.jpeg'%(WEBSITE,recommend.avatar_name)),
                                    'url':('%s/mobile/info_detail/%s/'%(WEBSITE,recommend.user.id)),'userId':recommend.user.id,'country':recommend.country}for recommend in recommendList]
            email=Email(args['email'],'帮你找到8名符合你择偶要求的人，千万别错过缘分！【拼爱网】')
            email.html('Email_Template.html', args)
            email.send()
            #添加发送推荐人记录
            emailRecommendHistoryList=[EmailRecommendHistory(user_id=userProfile.user_id,recommender_id=recommend['userId']) for recommend in args['recommendList']]
            EmailRecommendHistory.objects.bulk_create(emailRecommendHistoryList)
      except BotoServerError as e:
        logger.error('%s%s%s%s'%('发送推荐邮件出错，出错用户id为',userProfile.user_id,'错误内容：',e.body))
      except Exception as e:
        logger.exception('%s%s%s%s'%('发送推荐邮件出错，出错用户id为',userProfile.user_id,'错误内容：',e.message))
        
        
'''
发送消息邮件
'''
def send_message_email(userIdList=None):
    #发送的信息
    send_message='发送成功的用户信息:'
    #获取用户信息
    if userIdList is None:
        userProfileList=UserProfile.objects.select_related('user').all()
    else:
        userProfileList=UserProfile.objects.select_related('user').filter(user_id__in=userIdList)
    #遍历用户
    for userProfile in userProfileList:
      try:
        #判断邮箱和未读信息
        if userProfile.user.email is not None :
            args={'username':userProfile.user.username,'email':userProfile.user.email,'WEBSITE':WEBSITE}
            count=getattr(models,'get_no_read_message_dynamic_list_count')(userProfile.user_id)
            if count<=0:
                continue
            messageCount=MessageLog.objects.get_no_read_private_msessge_count(userProfile.user_id)
            
            followCount=MessageLog.objects.get_no_read_follow_message_count(userProfile.user_id)
            dynamicCommentCount=FriendDynamicComment.objects.get_no_read_comment_count(userProfile.user_id)
            dynamicArgeeCount=FriendDynamicArgee.objects.get_no_read_agree_count(userProfile.user_id)
            messageStr='<a href="%s/message/message_list/">收到%s条未读私信</a>,'%(WEBSITE,messageCount) if messageCount>0 else ''
            followStr='<a href="%s/message/follow_list/">新增了%s个新粉丝</a>,'%(WEBSITE,followCount) if followCount>0 else ''
            dynamicCommentStr='<a href="%s/dynamic/comment_list/">收到了%s条动态评论</a>,'%(WEBSITE,dynamicCommentCount) if dynamicCommentCount>0 else ''
            dynamicArgeeStr='<a href="%s/dynamic/agree_list/">获得了%s个赞</a>,'%(WEBSITE,dynamicArgeeCount) if dynamicArgeeCount>0 else ''
            args['messageStr']='您在不在拼爱网的这段时间，%s%s%s%s快登陆查看吧！'%(messageStr,followStr,dynamicCommentStr,dynamicArgeeStr)
            email=Email(args['email'],'您不在拼爱网的时间收到了%s消息，千万别错过缘分！【拼爱网】'%(count))
            email.html('message_Email_Template.html', args)
            email.send()
            send_message='%s用户名:%s email:%s ;'%(send_message,args['email'],args['username'])
      except BotoServerError as e:
        logger.error('%s%s%s%s'%('发送推荐邮件出错，出错用户id为',userProfile.user_id,'错误内容：',e.body))
      except Exception as e:
        logger.exception('%s%s%s%s'%('发送推荐邮件出错，出错用户id为',userProfile.user_id,'错误内容：',e.message))
    return send_message
    
