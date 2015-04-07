# -*- coding: utf-8 -*-
'''
Created on 2015年4月2日

@author: jin
'''
from apps.user_app.models import UserProfile
from util.cache import get_has_recommend
from apps.recommend_app.recommend_util import cal_recommend
from util.email import Email
from pinloveweb.settings import WEBSITE
from apps.task_app.models import EmailRecommendHistory
import logging
from boto.exception import BotoServerError
logger=logging.getLogger(__name__)
def send_notify_email(userIdList=None):
    if userIdList is None:
        userProfileList=UserProfile.objects.select_related('user').all()
    else:
        userProfileList=UserProfile.objects.select_related('user').filter(user_id__in=userIdList)
    for userProfile in userProfileList:
      try:
        if userProfile.user.email is not None:
            'sds'.toSting()
            recommendList=UserProfile.objects.get_email_recommed_list(userProfile.user_id)
            if recommendList=='less':
                raise Exception('推荐人数不足!')
            args={'username':userProfile.user.username,'email':userProfile.user.email,'WEBSITE':WEBSITE}
            args['recommendList']=[{'username':recommend.user.username,'age':recommend.age,'avatar_name':('%s/media/%s-100.jpeg'%(WEBSITE,recommend.avatar_name)),
                                    'url':('%s/mobile/detail_info/%s/'%(WEBSITE,recommend.user.id)),'userId':recommend.user.id}for recommend in recommendList]
            email=Email(args['email'],'帮你找到8名符合你择偶要求的人，千万别错过缘分！【拼爱网】')
            email.html('Email_Template.html', args)
#             email.send()
            #添加发送推荐人记录
            emailRecommendHistoryList=[EmailRecommendHistory(user_id=userProfile.user_id,recommender_id=recommend['userId']) for recommend in args['recommendList']]
            EmailRecommendHistory.objects.bulk_create(emailRecommendHistoryList)
      except BotoServerError as e:
        logger.error('发送推荐邮件出错，出错用户id为'+userProfile.user_id+'错误内容：'+e.body)
      except Exception as e:
        logger.exception('发送推荐邮件出错，出错用户id为'+userProfile.user_id+'错误内容：'+e.message)
