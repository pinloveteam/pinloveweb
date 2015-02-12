# -*- coding: utf-8 -*-
'''
Created on Sep 3, 2013

@author: jin
'''
from apps.user_app.models import UserProfile, Follow, UserTag,\
    BrowseOherScoreHistory
from apps.recommend_app.models import MatchResult, Grade, UserExpect
from util.page import page
from django.shortcuts import render
from apps.upload_avatar import app_settings
from apps.pojo.recommend import RecommendResult
from apps.recommend_app.form import WeightForm
from django.utils import simplejson
from django.core.context_processors import csrf
from django.http import HttpResponse
import logging
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from apps.recommend_app.method import get_matchresult
from pinloveweb.settings import ADMIN_ID
from apps.recommend_app.recommend_settings import BUY_SCORE_FOR_OTHER_MESSAGE_TEMPLATE
logger = logging.getLogger(__name__)  
#######################################
#1.0使用版本
#######################################
'''
 更新权重
'''
def update_weight(request):
    args={}
    flag=True
    try:
        height=float(request.POST.get('height',-1))/100
        income=float(request.POST.get('income',-1))/100
        appearance=float(request.POST.get('appearance',-1))/100
        education=float(request.POST.get('education',-1))/100
        character=float(request.POST.get('character',-1))/100
   
        if ( int(education)<0 and int(character)<0 and int(income)<0 and int(appearance)<0 and int(height)<0):
           flag=False
           args['result']='error'
           args['msg']='传输参数错误!'
        if int(education+character+income+appearance+height)!=1:
            flag=False
            args['result']='error'
            args['msg']='数值总和不为100!'
        if flag:
            if Grade.objects.filter(user_id=request.user.id,heightweight=None).exists():
                from apps.user_score_app.method import get_score_by_weight
                get_score_by_weight(request.user.id)
            Grade.objects.create_update_grade(request.user.id,heightweight=height,\
                                          incomeweight=income,educationweight=education,appearanceweight=appearance,characterweight=character)
            #判断推荐条件是否完善
            from apps.recommend_app.recommend_util import cal_recommend
            cal_recommend(request.user.id,['grade'])
            args['result']='success'
        else:
            args['result']='error'
    
    except Exception as e:
        flag=False
        args['result']='error'
        args['msg']=e.message
        logger.exception('更新权重错误！')
    json=simplejson.dumps(args)
    return HttpResponse(json)


def grade_for_other(request):
    args={}
    if request.method=="POST":
        flag=True
        try:
            result=request.POST.get('result',False)
        except Exception as e:
            flag=False
            args['result']='error'
            args['msg']='传输参类型错误！'
            logger.error('传输参类型错误！',e)
        if not result :
            flag=False
            args['result']='error'
            args['msg']='传输参数错误！'
        s=result.split(',')
        for temp in s:
            if float(temp)>100.00:
               flag=False
               args['result']='error'
               args['msg']='数据不得大于100！' 
               break;
        if flag:
            UserExpect.objects.create_update_by_uid(user_id=request.user.id,heighty1=float(s[0]),heighty2=float(s[1]),heighty3=float(s[2]),heighty4=float(s[3]),heighty5=float(s[4]) ,heighty6=float(s[5]),heighty7=float(s[6]),heighty8=float(s[7]))
            #判断推荐条件是否完善
            from apps.recommend_app.recommend_util import cal_recommend
            cal_recommend(request.user.id,['userExpect'])     
            args['result']='success'
        json=simplejson.dumps(args)
        return HttpResponse(json)
 
'''
 获取另一半对自己打分
'''
def check_score_and_PLprice_for_socre_my(request):
    try:
        from apps.pay_app.method import check_score_and_PLprice
        args=check_score_and_PLprice(request.user.id,"score_my")
        json=simplejson.dumps(args)
        return HttpResponse(json)
    except Exception as e:
        logging.error('%s%s'%('check_score_and_PLprice_for_pintu,出错原因：',e))
        
'''
 获取另一半对自己打分
'''   
def socre_my(request):
    args={}
    try:
        otherId=int(request.REQUEST.get('userId',False))
        if otherId:
            member=UserProfile.objects.get(user_id=request.user.id).member
            flag=BrowseOherScoreHistory.objects.filter(my_id=request.user.id,other_id=otherId).exists();
            if member>0 or flag:
                matchResult=get_matchresult(request.user.id,otherId)
                args={'result':'success','scoreMyself':int(matchResult.scoreMyself)}
            else:
                from apps.user_score_app.method import use_score_by_other_score
                result=use_score_by_other_score(request.user.id,otherId)
                if result=='success':
                    matchResult=get_matchresult(request.user.id,otherId)
                    #保存浏览记录
                    BrowseOherScoreHistory(my_id=request.user.id,other_id=otherId).save()
                    args={'result':'success','scoreMyself':int(matchResult.scoreMyself)}
                elif result=='less':
                    from apps.pay_app.method import use_charge_by_other_score
                    chargeResult=use_charge_by_other_score(request.user.id,otherId)
                    if chargeResult=='success':
                        matchResult=get_matchresult(request.user.id,otherId)
                        #保存浏览记录
                        BrowseOherScoreHistory(my_id=request.user.id,other_id=otherId).save()
                        args={'result':'success','scoreMyself':int(matchResult.scoreMyself)}
                    elif chargeResult=='less':
                        args={'result':'error','error_messge':'请充值!'}
        else:
            args={'result':'error','error_messge':'用户id不存在!'}
        json=simplejson.dumps(args)
        return HttpResponse(json)
    except Exception as e:
        logger.error('%s%s' %('获取另一半对自己打分出错',e))
        args={'result':'error','error_messge':'%s%s' %('获取另一半对自己打分出错',e)}
#         args={'result':'error','error_messge':'系统出错!'}
        json=simplejson.dumps(args)
        return HttpResponse(json)


'''
获得对自己对另一半的打分
'''
def get_socre_for_other(userId,otherId):    
    args={}
    try:
        if otherId:
#              from apps.recommend_app.method import get_match_score_other
#              matchResult=get_match_score_other(userId,otherId)
#              if matchResult==None:
                 #判断是否可用匹配
                 from util.cache import get_has_recommend,get_recommend_status,has_recommend
                 for field in ['userExpect','grade','tag']:
                     has_recommend(userId,field)
                 if get_has_recommend(userId):
                     from apps.recommend_app.method import match_score
                     matchResult=match_score(userId,otherId)
                     args={'result':'success','matchResult':matchResult.get_dict(matchResult.is_permission(userId=userId))} 
                 else:
                     recommendStatus=get_recommend_status(userId)
                     dict={'userProfile':u'个人信息  ','userExpect':u'身高期望  ','grade':u'权重  ','tag':u'标签  '}
                     errorMessge=''
                     for key in recommendStatus.keys():
                         if not recommendStatus[key]:
                             errorMessge+=dict[key]
                     args={'result':'error','error_message':'%s%s' %(errorMessge,u'未填写完整!')}
#              else:
#                  from apps.pojo.recommend import MarchResult_to_RecommendResult
#                  matchResult=MarchResult_to_RecommendResult(matchResult)
#                  args={'result':'success','matchResult':matchResult.get_dict(matchResult.is_permission(userId=userId))} 
        else:
            args={'result':'error','error_messge':'用户id不存在!'}
        return args
    except Exception as e:
        logger.exception('%s%s' %('获得对自己对另一半的打分，出错原因：',e))
        args={'result':'error','error_messge':'系统出错!'}
        return args
    
'''
性格标签
'''    
@transaction.commit_on_success     
def character_tags(request):
    args={}
    try:
        if request.method=="POST":
            tagMyList=request.REQUEST.get('tagMyList','').split(',')
            tagOhterList=request.REQUEST.get('tagOhterList','').split(',')
            if not UserTag.objects.filter(user_id=request.user.id).exists():
                from apps.user_score_app.method import get_score_by_character_tag
                get_score_by_character_tag(request.user.id)
            #保存tag
            UserTag.objects.bulk_insert_user_tag(request.user.id,0,tagMyList)
            UserTag.objects.bulk_insert_user_tag(request.user.id,1,tagOhterList)
            #判断推荐条件是否完善
            from apps.recommend_app.recommend_util import cal_recommend
            cal_recommend(request.user.id,['userExpect','tag']) 
            args['result']='success'
            json=simplejson.dumps(args)
        return HttpResponse(json)
    except Exception as e:
        logger.error('%s%s' %('性格标签，出错原因：',e))
        args={'result':'error','error_messge':e.message}
        json=simplejson.dumps(args)
        return HttpResponse(json)
    
'''
为对方买分，即对方将能看到我对对方的打分
'''
@transaction.commit_on_success  
def buy_score_for_other(request):
    args={}
    try:
        flag=False
        type=1
        otherId=int(request.REQUEST.get('otherId'))
        from apps.user_score_app.method import use_score_by_other_score
        result=use_score_by_other_score(request.user.id,otherId)
        if result=='success':
            flag=True
        elif result=='less':
            from apps.pay_app.method import use_charge_by_other_score
            chargeResult=use_charge_by_other_score(request.user.id,otherId)
            if chargeResult=='success':
               flag=True
            elif chargeResult=='less':
                flag=False
        if flag:
            args={'result':'success'}
            if not BrowseOherScoreHistory.objects.filter(my_id=otherId,other_id=request.user.id).exists():
                BrowseOherScoreHistory(my_id=otherId,other_id=request.user.id).save()
            #判断对方是否浏览过我的分数
            if BrowseOherScoreHistory.objects.filter(my_id=request.user.id,other_id=otherId).exists():
                type=2
            args['type']=type
            #发系统消息给对应用户
            from apps.message_app.method import add_system_message_121
            add_system_message_121(ADMIN_ID, otherId, BUY_SCORE_FOR_OTHER_MESSAGE_TEMPLATE%(request.user.username,request.user.id))
        else:
            args={'result':'error','error_message':'请充值!'}
        json=simplejson.dumps(args)
        return HttpResponse(json)
    except Exception,e:
        logger.exception('为对方买分,出错!')
        
        
'''
  用户投票
'''    
def user_vote(request):
    args={}
    try:
        score = float(request.REQUEST.get('score').strip())
        otherId=int(request.REQUEST.get('otherId')) if len(request.REQUEST.get('otherId'))!=0 else None
        userId=int(request.REQUEST.get('userId'))
#         if AppearanceVoteRecord.objects.filter(user_id=request.user.id,other_id=userId).exists():
#             args={'result':'error','error_message':u'你已打过分'}
        if score <0 or score >100:
            args={'result':'error','error_message':u'分数必须在1~100范围内!'}
        elif score=='':
            args={'result':'error','error_message':u'不能为空!'}
        else:
            geadeInstance=Grade.objects.get(user_id=userId)
            from apps.recommend_app.recommend_util import cal_user_vote
            score=cal_user_vote(request.user.id,userId,score,geadeInstance.appearancescore,geadeInstance.appearancesvote,1)
            Grade.objects.filter(user_id=userId).update(appearancescore=score['score'],appearancesvote=geadeInstance.appearancesvote if score['flag'] else geadeInstance.appearancesvote+1)
            #获取雷达图分数
            socreForOther=get_socre_for_other(request.user.id,userId)
            diagData=[socreForOther['matchResult']['edcationScore'],socreForOther['matchResult']['characterScore'],socreForOther['matchResult']['incomeScore'],socreForOther['matchResult']['appearanceScore'],socreForOther['matchResult']['heighScore'],]
            score=int(socreForOther['matchResult']['scoreOther'])
            data={userId:diagData}
            if not otherId is None:
                compareSocreForOther=get_socre_for_other(request.user.id,otherId)
                compareDiagData=[compareSocreForOther['matchResult']['edcationScore'],compareSocreForOther['matchResult']['characterScore'],compareSocreForOther['matchResult']['incomeScore'],compareSocreForOther['matchResult']['appearanceScore'],compareSocreForOther['matchResult']['heighScore'],]
                data[otherId]=compareDiagData
            args={'result':'success','data' :data,'score' : score}
        json = simplejson.dumps(args)
        return HttpResponse(json)
    except Exception,e:
        logger.exception('用户投票,出错!')
        args={'result':'error','error_message':e.message}
        json = simplejson.dumps(args)
        return HttpResponse(json)
        
##########################################

     
    

       
def test_match(request):
    args={}
    userId=int(request.GET.get('userId'))
    gradeMy=Grade.objects.get(user_id=request.user.id)
    matchResult=MatchResult.objects.get(my_id=request.user.id,other_id=userId)
    grade=Grade.objects.get(user_id=userId)
    args['我的收入得分']=gradeMy.incomescore
    args['我的学历得分']=gradeMy.educationscore
    args['我的外貌得分']=gradeMy.appearancescore
    #对方得分
    args['对方的收入得分']=grade.incomescore
    args['对方的学历得分']=grade.educationscore
    args['对方的外貌得分']=grade.appearancescore
    #相互打分
    args['异性对我的打分和']=matchResult.scoreMyself
    args['我对异性的打分和']=matchResult.scoreMyself
#     args['macthScore']=matchResult.macthScore
    args['我对异性的身高打分（权重）']=matchResult.heighMatchOther
    args['异性对我的身高打分（权重）']=matchResult.heighMatchMy
    args['异性对我的收入打分（权重）']=matchResult.incomeMatchMy
    args['我对异性的收入打分（权重）']=matchResult.incomeMatchOther
    args['我对异性的学历打分（权重）']=matchResult.edcationMatchOther
    args['异性对我的学历打分（权重）']=matchResult.edcationMatchMy
    args['我对异性的外貌打分（权重）']=matchResult.appearanceMatchOther
    args['异性对我的外貌打分（权重）']=matchResult.appearanceMatchMy
    args['异性对我的性格打分（权重）']= matchResult.characterMatchMy
    args['异性对我的性格打分（权重）']=matchResult.characterMatchMy 
    
    args['我匹配标签得分']=matchResult.tagMatchOtherScore
    args['异性对我的匹配标签得分']=matchResult.tagMatchMyScore
    args['我匹配身高得分']=matchResult.heighMatchOtherScore
    args['异性对我的身高标签得分']=matchResult.heighMatchMyScore
    json=simplejson.dumps(args)
    return HttpResponse(json)