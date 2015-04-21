# -*- coding: utf-8 -*-
'''
Created on 2014年5月23日

@author: jin
'''
from django.http.response import HttpResponse, HttpResponseRedirect
from apps.weixin_app.forms import InfoForm, TaInfoForm
import logging
from django.shortcuts import render
from apps.user_app.models import UserProfile, UserTag
from django.utils import simplejson
from apps.recommend_app.models import UserExpect, Grade
from apps.weixin_app.models import ScoreRank
from apps.third_party_login_app.setting import PublicWeiXinAppID,\
    WEIXIN_CHECK_AUTHORIZATION_URL
from apps.third_party_login_app.models import ThirdPsartyLogin
from apps.weixin_app.method import get_jsapi_ticket, get_signature
from django.db import transaction
import datetime
logger=logging.getLogger(__name__)
def common(request):
    '''
    微信公共函数
    '''
    args={'PublicWeiXinAppID':PublicWeiXinAppID,'WEIXIN_CALLBACK_URL':'%s%s'%(WEIXIN_CHECK_AUTHORIZATION_URL[:-1],'_url/'),'has_share':False}
    if ("jsapi_ticket_expires" not in request.session) or (request.session['jsapi_ticket_expires']>datetime.datetime.now()):
        get_jsapi_ticket(request) 
    args.update(get_signature(request.session['jsapi_ticket'],request.build_absolute_uri()))  
    return args    
    
'''
完善个人信息
'''
def self_info(request):
        userKey=request.REQUEST.get('userKey')
        args=common(request)
        args['userKey']=userKey
        if userKey==None:
            return render(request,'error.html',{'result':'error','error_message':'没有用户标识，请联系客服!'})
        userProfile=UserProfile.objects.get(user=request.user)
        args['link']=userProfile.link
        #查看排名
        if userKey!=u'rank':
            try:
                otherId=UserProfile.objects.get(link=userKey).user_id
            except UserProfile.DoesNotExist as e:
                return render(request,'error.html',{'result':'error','error_message':'没有这个用户，请联系客服!'})
            except UserProfile.MultipleObjectsReturned as e:
                return render(request,'error.html',{'result':'error','error_message':'有多个用户，请联系客服!'})
        if userKey==u'rank' or otherId==request.user.id  :
            scoreRankBeanbList=ScoreRank.objects.filter(my_id=request.user.id).order_by("-score")
            scoreRankList=[]
            for scoreRankBean in scoreRankBeanbList:
                scoreRankBean.score=int(scoreRankBean.score)
                scoreRankList.append(scoreRankBean)
            args.update({'scoreRankList':scoreRankList,'count':len(scoreRankList),'has_share':True})
            return render(request,'Rank.html',args)
        if request.method=="POST":
            import copy
            oldUserProfile=copy.deepcopy(userProfile)
            POSTdata=request.POST.copy()
            infoFrom = InfoForm(POSTdata, instance=userProfile) 
            if infoFrom.is_valid():
                userProfile = infoFrom.save(commit=False)
                userProfile.save(oldUserProfile=oldUserProfile)
                #计算学历
                from apps.weixin_app.method import cal_eduction_in_game
                eductionScore=cal_eduction_in_game(int(infoFrom.cleaned_data['education']),int(infoFrom.cleaned_data['schoolType']))
#                 logging.error('233esddfsd-----%s %s %s %s'%(int(infoFrom.cleaned_data['education']),int(schoolType),int(country),eductionScore))
                Grade.objects.filter(user_id=request.user.id).update(educationscore=eductionScore)
                transaction.commit()
                args['result']='success'
                args['next_url']='/weixin/my_character/?userKey='+userKey
            else:
               errors=infoFrom.errors.items()
               args={'result':'error','error_message':errors[0][1][0]if errors[0][0]==u'__all__' else '%s %s'%(InfoForm.base_fields[errors[0][0]].label,errors[0][1][0])}
            json=simplejson.dumps(args)
            return HttpResponse(json)
        elif ScoreRank.objects.filter(my_id=otherId,other_id=request.user.id).exists():
            return HttpResponseRedirect("/weixin/score/?userKey=%s"%(userKey))
        elif UserProfile.objects.filter(user_id=request.user.id).exclude(income=-1,education=-1).exists():
           if UserTag.objects.filter(user_id=request.user.id,type=0).exists():
             return HttpResponseRedirect("/weixin/score/?userKey=%s"%(userKey))
           else:
            return my_character(request)
        args['infoForm']=InfoForm(instance=userProfile)
        return render(request,'selfInfo.html',args)
 
   
def my_character(request,template_name='character_tag.html'):
    '''
    填写我的性格标签
    '''
    args={}
    try:
        userKey=request.REQUEST.get('userKey')
        args=common(request)
        args.update({"userKey":userKey,"step":"第二步","title":"再测测您的软实力,请选择情商标签",'url':'/weixin/my_character/'})
        if userKey==None:
            return render(request,'error.html',{'result':'error','error_message':'没有用户标识，请联系客服!'})
        try:
            otherId=UserProfile.objects.get(link=userKey).user_id
        except UserProfile.DoesNotExist as e:
            return render(request,'error.html',{'result':'error','error_message':'没有这个用户，请联系客服!'})
        except UserProfile.MultipleObjectsReturned as e:
                return render(request,'error.html',{'result':'error','error_message':'有多个用户，请联系客服!'})
        if request.method=="POST":
            tagMyList=request.REQUEST.get('tagList','').split(',')
            if not UserTag.objects.filter(user_id=request.user.id).exists():
                from apps.user_score_app.method import get_score_by_character_tag
                get_score_by_character_tag(request.user.id)
            #保存tag
            gltNum=5
            try:
                UserTag.objects.bulk_insert_user_tag(request.user.id,0,tagMyList,gltNum=gltNum)
            except Exception as e:
                error_messsage=e.message
                if e.message=='less':
                    error_messsage='亲！起码要选择%s个哦！'%(gltNum)
                elif e.message=='more':
                    error_messsage=error_messsage='亲！你选择的个数超标了！'
                raise Exception(error_messsage)
            args.update({'next_url':"/weixin/score/?userKey=%s"%(userKey),"result":'success'})
        else:
            #获取自己个人标签
            tags=UserTag.objects.get_tags_by_type(user_id=request.user.id,type=0)
            from apps.pojo.tag import tag_to_tagbean
            tagbeanList=tag_to_tagbean(tags)
            args['tagbeanList']=[tagbean for tagbean in tagbeanList if tagbean[0].id not in[14,27,4]]
        args['result']='success'
    except Exception as e:
        args={'result':'error','error_message':e.message}
        template_name='error.html'
    if request.is_ajax():
        json=simplejson.dumps(args)
        return HttpResponse(json)
    else:
        return render(request,template_name,args)
    
def score(request,template_name="Score.html"):
    '''
    获得得分
    '''
    args={}
    try:
        userKey=request.REQUEST.get('userKey')
        args=common(request)
        userProfile=UserProfile.objects.get(user=request.user)
        args['link']=userProfile.link
        try:
            otherProfile=UserProfile.objects.select_related('user').get(link=userKey)
            otherId=otherProfile.user_id
            args['username']=otherProfile.user
        except UserProfile.DoesNotExist as e:
            return render(request,'error.html',{'result':'error','error_message':'没有这个用户，请联系客服!'})
        except UserProfile.MultipleObjectsReturned as e:
                return render(request,'error.html',{'result':'error','error_message':'有多个用户，请联系客服!'})
        if not ScoreRank.objects.filter(my_id=otherId,other_id=request.user.id).exists():
            from apps.recommend_app.method import match_score
            socreForOther=match_score(otherId,request.user.id).get_dict()
            args.update({'data' : [int(socreForOther['edcationScore']),int(socreForOther['characterScore']),\
                   int(socreForOther['incomeScore']),\
                   int(socreForOther['heighScore']),],'score' :int(socreForOther['scoreOther'])})
            data=simplejson.loads(ThirdPsartyLogin.objects.get(user_id=request.user.id).data)
            nickname=data['nickname']
            scoreRank=ScoreRank(my_id=otherId,other_id=request.user.id,score=args['score'],nickname=nickname,data=simplejson.dumps(args['data'])).save()
        else:
            scoreRank=ScoreRank.objects.get(my_id=otherId,other_id=request.user.id)
            args['data']=simplejson.loads(scoreRank.data)
            args['score']=int(scoreRank.score)
        args['rank']=(ScoreRank.objects.filter(my_id=otherId,score__gt=args['score']).count()+1)
        filedList={'MM':u'你和%s的基友指数'%(otherProfile.user),'FF':u'你和%s的闺蜜指数'%(otherProfile.user),'MF':u'你在女神%s心中的亲密指数'%(otherProfile.user),'FM':u'你在男神%s心中的亲密指数'%(request.user),}
        args['score_content']=filedList[u'%s%s'%(userProfile.gender,otherProfile.gender)]
        #判断他的条件是否成立
        if (not Grade.objects.filter(user_id=request.user.id,heightweight=None,incomeweight=None,educationweight=None,characterweight=None)) and UserTag.objects.filter(user_id=request.user.id).exists():
            args['is_recommend']=True
            args['has_share']=True
        else:
            args['is_recommend']=False
            args['next_url']='/weixin/other_info/'
            
    except Exception as e:
        args={'result':'error','error_message':e.message}   
        template_name='error.html'
    return  render(request,template_name,args)   
'''
完善我对别人打分信息
'''
def other_info(request,template_name='otherInfo.html'):
    args={}
    try:
        args=common(request)
        userProfile=UserProfile.objects.get(user=request.user,)
        args['link']=userProfile.link
        if request.method=="POST":
            taInfoForm=TaInfoForm(request.POST,initial={'gender':userProfile.gender})
            if taInfoForm.is_valid():
                from apps.weixin_app.method import cal_expect_height_in_game
                expectHeightList=cal_expect_height_in_game(userProfile.gender,int(taInfoForm.cleaned_data['expectHeight']))
                UserExpect.objects.create_update_by_uid(user_id=request.user.id,heighty1=expectHeightList[0],heighty2=expectHeightList[1],heighty3=expectHeightList[2],heighty4=expectHeightList[3],\
                                                heighty5=expectHeightList[4] ,heighty6=expectHeightList[5],heighty7=expectHeightList[6],heighty8=expectHeightList[7])
                if Grade.objects.filter(user_id=request.user.id,heightweight=None).exists():
                    from apps.user_score_app.method import get_score_by_weight
                    get_score_by_weight(request.user.id)
                grade=taInfoForm.cal_weight(request.user.id)
                grade.save()
                args.update({'result':'success','next_url':'/weixin/ta_character/'})
            else:
                errors=taInfoForm.errors.items()
                args={'result':'error','error_message':errors[0][1][0]if errors[0][0]==u'__all__' else '%s %s'%(TaInfoForm.base_fields[errors[0][0]].label,errors[0][1][0])}
        else:
            args['TaInfoForm']=TaInfoForm(initial={'gender':userProfile.gender})
            args['gender']=userProfile.gender
    except Exception as e:
        logger.exception('完善我对别人打分信息：%s'%(e.message))
        args={'result':'error','error_message':(e.message)}
        template_name="error.html"
    if request.is_ajax():
        json=simplejson.dumps(args)
        return HttpResponse(json)
    else:
        return render(request,template_name,args)
    
        
        
def ta_character(request,template_name="character_tag.html"):
    args={}
    try:
        args=common(request)
        args.update({"step":"第四步","title":"选出你心目中男神、女神的标准–软实力EQ篇",'url':'/weixin/ta_character/'})
        userProfile=UserProfile.objects.get(user=request.user)
        args['link']=userProfile.link
        if request.method=="POST":
            tagOtherList=request.REQUEST.get('tagList','').split(',')
            #标签
            if not UserTag.objects.filter(user_id=request.user.id).exists():
                from apps.user_score_app.method import get_score_by_character_tag
                get_score_by_character_tag(request.user.id)
                
            gltNum=5
            try:
                UserTag.objects.bulk_insert_user_tag(request.user.id,1,tagOtherList,gltNum=gltNum)
            except Exception as e:
                error_messsage=e.message
                if e.message=='less':
                    error_messsage='亲！起码要选择%s个哦！'%(gltNum)
                elif e.message=='more':
                    error_messsage='亲！你选择的个数超标了！'
                raise Exception(error_messsage)
            
            args["result"]='success'
        else:
            #获取对另一半期望标签
            tagsForOther=UserTag.objects.get_tags_by_type(user_id=request.user.id,type=1)
            from apps.pojo.tag import tag_to_tagbean
            tagbeanForOtherList=tag_to_tagbean(tagsForOther)
            args['tagbeanList']=[tagbeanForOther for tagbeanForOther in tagbeanForOtherList if tagbeanForOther[0].id not in[14,27,4]]
            args['gender']=userProfile.gender
    except Exception as e:
        logger.exception('完善我对别人打分信息：%s'%(e.message))
        args={'result':'error','error_message':(e.message)}
        template_name='error.html'
    if request.is_ajax():
        json=simplejson.dumps(args)
        return HttpResponse(json)
    else:
        return render(request,template_name,args)
    
def test(request):
    eduction=request.GET.get('eduction')
    schoolType=request.GET.get('schoolType')
    country=int(request.GET.get('country'))
    from apps.weixin_app.method import cal_eduction_in_game
    result=cal_eduction_in_game(int(eduction),int(schoolType),country)
    return HttpResponse(result)