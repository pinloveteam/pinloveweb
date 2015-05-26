# -*- coding: utf-8 -*-
'''
Created on Sep 3, 2013

@author: jin
'''
from apps.user_app.models import UserProfile, UserTag,\
    BrowseOherScoreHistory
from apps.recommend_app.models import MatchResult, Grade, UserExpect, WeightStar
from django.utils import simplejson
from django.http import HttpResponse
import logging
from django.db import transaction
from apps.recommend_app.method import get_matchresult
from pinloveweb.settings import ADMIN_ID
from apps.recommend_app.recommend_settings import BUY_SCORE_FOR_OTHER_MESSAGE_TEMPLATE
from django.views.decorators.http import require_POST
from apps.recommend_app.form import StartForm
logger = logging.getLogger(__name__)  
#######################################
#1.0使用版本
#######################################
'''
 更新权重
'''
@require_POST
@transaction.commit_on_success    
def update_weight(request):
    args={}
    try:
        userId=request.user.id
        weightStar=WeightStar.objects.filter(user_id=userId)
        if len(weightStar)>0:
            startFrom=StartForm(request.POST,instance=weightStar[0],)
        else:
            startFrom=StartForm(request.POST)
        if startFrom.is_valid():
            weightStar=startFrom.save(commit=False)
            weightStar.user=request.user
            weightStar.save()
            #判断推荐条件是否完善
            from apps.recommend_app.recommend_util import cal_recommend
            cal_recommend(request.user.id,['weight'])
            args['result']='success'
        else:
            args['result']='error'
            args['error_message']=''
            errors=startFrom.errors.items()
            for error in errors:
                args['error_message']+=error[1][0]
    except Exception as e:
        args['result']='error'
        args['error_message']=e.message
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
                 from util.cache import get_has_recommend,has_recommend
                 for field in ['userExpect','weight','tag','info',"avatar"]:
                     has_recommend(userId,field)
                 if get_has_recommend(userId):
                     from apps.recommend_app.method import match_score
                     matchResult=match_score(userId,otherId)
                     args={'result':'success','matchResult':matchResult.get_dict(matchResult.is_permission(userId=userId))} 
                 else:
                     args={'result':'less'}
#              else:
#                  from apps.pojo.recommend import MarchResult_to_RecommendResult
#                  matchResult=MarchResult_to_RecommendResult(matchResult)
#                  args={'result':'success','matchResult':matchResult.get_dict(matchResult.is_permission(userId=userId))} 
        else:
            args={'result':'error','error_messge':'用户id不存在!'}
        return args
    except Exception as e:
        logger.exception('%s%s' %('获得对自己对另一半的打分，出错原因：',e))
    
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
            type=0
            try:
                UserTag.objects.bulk_insert_user_tag(request.user.id,type,tagMyList)
                type=1
                UserTag.objects.bulk_insert_user_tag(request.user.id,type,tagOhterList)
            except Exception as e:
                error_messsage=e.message
                content="TA的性格标签" if type==1 else "我的性格标签"
                if e.message=='less':
                    error_messsage='%s要全部选择！'%(content)
                elif e.message=='more':
                    error_messsage='%s选择的个数超标了！'%(content)
                raise Exception(error_messsage)
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
        
