# -*- coding: utf-8 -*-
'''
Created on 2014年1月9日

@author: jin
'''
#用于初始化用户所需要的信息
from apps.user_app.models import Follow, Verification, UserVerification,\
    UserProfile
from django.utils import simplejson
from django.http.response import HttpResponse
from apps.friend_dynamic_app.models import FriendDynamic
import hashlib
from django.contrib import auth
def init_person_info_for_card_page(userProfile,**kwargs):
    arg={}
    arg['avatar_name']=userProfile.avatar_name
    arg['age']=userProfile.age
    arg['gender']=userProfile.gender
    arg['height']=userProfile.height
    arg['income']=userProfile.income
    arg['education']=userProfile.get_education_display()
    arg['jobIndustry']=userProfile.jobIndustry
    arg['member']=userProfile.member
    if kwargs.get('myFollowCount')==None:
        myFollowCount=Follow.objects.filter(my=userProfile.user).count()
    else:
        myFollowCount=kwargs.get('follow')
    if kwargs.get('follow')==None:
        fansCount=Follow.objects.filter(follow=userProfile.user).count()
    else:
        fansCount=kwargs.get('followEachCount')
    if kwargs.get('followEachCount')==None:
        followEachCount=Follow.objects.follow_each_count(userProfile.user_id)
    else:
        followEachCount=kwargs.get('followEachCount')   
    #相互关注的人的id
    arg['myFollow']=myFollowCount
    arg['fans']=fansCount
    arg['follow']=followEachCount
    #获取拼爱币数量
    from apps.pay_app.method import get_charge_amount
    arg['pinLoveCion']=get_charge_amount(userProfile.user_id)
    #获得最近一条动态
    #arg['dynamic']=get_dymainc_late(userProfile.user_id)
    arg.update(get_no_read_web_count(userProfile.user_id),fromPage=u'card')
    return arg

'''
获取未读的消息数量
@param userId:用户id
@return: dict
         messageNoReadCount 获取未读信息
         dynamicCommentCount 读取未读动态评论
         noReadCount  未读总信息
'''
def get_no_read_web_count(userId,fromPage=None):
    args={}
    from apps.message_app.models import get_no_read_message_dynamic_list_count
    args['noReadCount']= get_no_read_message_dynamic_list_count(userId)
    if fromPage==u'card':
        from apps.message_app.method import get_no_read_private_message_count
        args['noReadMessageCount']=get_no_read_private_message_count(userId)
    elif fromPage==u'message':
        from apps.message_app.method import get_no_read_follow_message_count,get_no_read_private_message_count
        args['noReadMessageCount']=get_no_read_private_message_count(userId)
        from apps.friend_dynamic_app.method import get_no_read_agree_count,get_no_read_comment_count
        args['noReadAgreeCount']=get_no_read_agree_count(userId)
        args['noReadFollowMessageCount']=get_no_read_follow_message_count(userId)
        args['noReadCommentCount']=get_no_read_comment_count(userId)
    return args
'''
判断是否是相互关注
attribute：
  CardList :List[Card] Card 类的列表
  focusEachOtherList：list 相互关注用户id
'''
def is_focus_each_other(userId,cardList):
    i=0
    cardIds=[card.user_id for card in cardList]
    focus = Follow.objects.select_related().filter(my_id=userId,follow_id__in=cardIds)
    follows=Follow.objects.select_related().filter(my_id__in=cardIds,follow_id=userId)
    followEach=Follow.objects.follow_each(userId,userIdList=cardIds)
    focusIds=[f.follow_id for f in focus] 
    followsIds=[follow.my_id for follow in follows] 
    followEachIds=[f.my_id for f in followEach] 
    for user in cardList:
        if user.user_id in followEachIds:
            cardList[i].followStatus=2
        i+=1
    i=0
    for user in cardList:
        if user.user_id in followsIds:
            if  cardList[i].followStatus==0:
                cardList[i].followStatus=3
        if user.user_id in focusIds:
            if  cardList[i].followStatus==0:
                cardList[i].followStatus=1
        i+=1
    return cardList



'''
通过ajax加载页面card
'''
def load_cards_by_ajax(request,cardList,chanel='web'):
    data={}
    data['has_next']=cardList.has_next()
    if cardList.has_next():
        data['next_page_number']=cardList.next_page_number()
    else:
        data['next_page_number']=-1
    if cardList.has_previous():
        data['previous_page_number']=cardList.previous_page_number()
    data['has_previous']=cardList.has_previous()
    data['result']='success'
    if request.GET.get('choseCards[]')!=None:
        choseCardslist=request.GET.getlist('choseCards[]')
        cardList.object_list = [card for card in cardList.object_list if str(card.user_id) not in choseCardslist]
        if len(cardList.object_list)<8:
            data['removeCard']=True
    data['cards']=cardList.object_list
    if chanel =='mobile':
        from apps.pojo.card import CardMobileEncoder
        json=simplejson.dumps(data,cls=CardMobileEncoder)
    else:
        from apps.pojo.card import MyEncoder
        json=simplejson.dumps(data,cls=MyEncoder)
    return HttpResponse(json)
     
'''
生成邀请码
'''
def create_invite_code(userId):
    import random
    randomInt=random.randint(1001, 9999)
    from util.util import random_str
    randomStr=random_str(randomlength=5)
    return '%s%s%s' % (userId,randomInt,randomStr)

'''
获得最近一条动态
'''
def get_dymainc_late(userId):
    dynamic=FriendDynamic.objects.filter(publishUser_id=userId).order_by('-publishTime')[:1]
    if len(dynamic)>0:
        dynamic=dynamic[0]
    else:
        return None
    data=[]
    LEN=60
    EXPRESSION_LEN=14
    #content长度
    flag=False
    #获得最近动态
    from util.util import regex_expression
    if len(dynamic.content)>LEN:
        flag=True
        from util.util_settings import EXPRESSION_REGEX
        regex=EXPRESSION_REGEX
        import re
        result=re.search(regex, dynamic.content[(LEN-EXPRESSION_LEN):(LEN+EXPRESSION_LEN)])
        if result is None:
            data.append(regex_expression(dynamic.content[0:LEN]))
        else:
            temp=dynamic.content.index(result.group(0),(LEN-EXPRESSION_LEN),(LEN+EXPRESSION_LEN))+len(result.group(0))
            data.append(regex_expression(dynamic.content[0:temp]))
    else:
        data.append(regex_expression(dynamic.content))
    data.append(dynamic.content)
    if not dynamic.data=='':
        pics=(u'[图片]'*len(simplejson.loads(dynamic.data)))
        if not flag:
            data[0]='%s%s'%(data[0],pics)
        data[1]=data[1]+pics
    if flag:
            data[0]=data[0]+'......'
    return data

'''
初始化注册所需的表
'''
def init_table_in_register(user_id,username,user_code):
    #认证表
    verification= Verification()
    verification.username = username
    verification.verification_code = user_code
    verification.save()
    #创建用户验证信息
    userVerification=UserVerification()
    userVerification.user_id=user_id
    userVerification.save()
    #用户积分表
    from apps.user_score_app.models import UserScore
    UserScore(user_id=user_id).save()
    #拼爱币表
    from apps.pay_app.models import Charge
    Charge(user_id=user_id).save()
    #分数表
    from apps.recommend_app.models import Grade
    Grade(user_id=user_id).save()
    
'''
发送激活邮件
'''
def send_active_email(user,user_code):
    from pinloveweb.settings import DEFAULT_FROM_EMAIL,DOMAIN
    domain_name = '%s%s%s'%('www.',DOMAIN,u'/account/verification/')
    email_verification_link = domain_name + '?username=' + user.username + '&' + 'user_code=' + user_code
    email_message = u"请您点击下面这个链接完成注册："
    email_message += email_verification_link
    try :
       from django.core.mail import send_mail
       send_mail(u'拼爱网注册电子邮件地址验证', email_message,DEFAULT_FROM_EMAIL,[user.email]) 
    except Exception as e:
        raise 
      
def send_reset_password(user,user_code):
    from pinloveweb.settings import DEFAULT_FROM_EMAIL,DOMAIN
    domain_name = '%s%s'%(DOMAIN,u'/user/reset_password/')
    email_verification_link = domain_name + '?username=' + user.username + '&' + 'user_code=' + user_code
    email_message = '%s%s%s'%(u"尊敬的",user.username,u"拼爱用户，请您点击下面这个链接重置密码：")
    email_message += email_verification_link
    try :
       from django.core.mail import send_mail
       send_mail(u'拼爱网重置用户密码', email_message,DEFAULT_FROM_EMAIL,[user.email]) 
    except Exception as e:
        raise 
'''
加密通道
使用用户名和密码加密通道
'''
def sign_channel(request):
    return hashlib.md5(simplejson.dumps({'id':request.user.id,'username':request.user.username})).hexdigest()

'''
初始化除了user的所有表
'''
def create_register_extra_user(request,userId,username,password,gender,link,**kwargs):
    #创建二维码
    Userlink=create_invite_code(userId)
    UserProfile(user_id=userId,gender=gender,link=Userlink,**kwargs).save()
    #生成激活码
    from util.util import random_str
    user_code = random_str()
    #初始化所需表
    init_table_in_register(userId,username,user_code)
    #注册成功赠送积分
    from apps.user_score_app.method import get_score_by_invite_friend_register
    if link:
        get_score_by_invite_friend_register(link)
        