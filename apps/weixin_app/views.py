# -*- coding: utf-8 -*-
'''
Created on 2014年5月23日

@author: jin
'''
from django.http.response import HttpResponse
from apps.weixin_app.forms import InfoForm
import logging
from django.shortcuts import render
from apps.user_app.models import UserProfile, UserTag
from django.utils import simplejson
from apps.recommend_app.models import UserExpect, Grade
from apps.weixin_app.models import ScoreRank
from apps.third_party_login_app.setting import PublicWeiXinAppID,\
    WEIXIN_CHECK_AUTHORIZATION_URL
from apps.third_party_login_app.models import ThirdPsartyLogin
logger=logging.getLogger(__name__)
'''
完善个人信息
'''
def self_info(request):
    args={'PublicWeiXinAppID':PublicWeiXinAppID,'WEIXIN_CALLBACK_URL':'%s%s'%(WEIXIN_CHECK_AUTHORIZATION_URL[:-1],'_url/'),'has_share':False}
    try:
        userKey=request.REQUEST.get('userKey')
        args['userKey']=userKey
        if userKey==None:
            raise Exception('没有用户标识')
        otherId=UserProfile.objects.get(link=userKey).user_id
        userProfile=UserProfile.objects.get(user=request.user)
        args['link']=userProfile.link
        if otherId==request.user.id:
            scoreRankList=ScoreRank.objects.filter(my_id=request.user.id).order_by("-score")
            args['scoreRankList']=scoreRankList
            args['count']=len(scoreRankList)
            return render(request,'Rank.html',args)
        if request.method=="POST":
            import copy
            oldUserProfile=copy.deepcopy(userProfile)
            POSTdata=request.POST.copy()
            infoFrom = InfoForm(POSTdata, instance=userProfile) 
            if infoFrom.is_valid():
                userProfile = infoFrom.save(commit=False)
                tagMyList=request.REQUEST.get('tagMyList','').split(',')
                schoolType=request.REQUEST.get('schoolType')
                country=request.REQUEST.get('country')
                if not UserTag.objects.filter(user_id=request.user.id).exists():
                    from apps.user_score_app.method import get_score_by_character_tag
                    get_score_by_character_tag(request.user.id)
                #保存tag
                UserTag.objects.bulk_insert_user_tag(request.user.id,0,tagMyList)
                userProfile.save(oldUserProfile=oldUserProfile)
                #计算学历
                from apps.weixin_app.method import cal_eduction_in_game
                eductionScore=cal_eduction_in_game(int(infoFrom.cleaned_data['education']),int(schoolType),int(country))
                Grade.objects.filter(user_id=request.user.id).update(educationscore=eductionScore)
                args['result']='success'
                args['score']=int(score(request.user.id,otherId))
                if not ScoreRank.objects.filter(my_id=otherId,other_id=request.user.id).exists():
                    data=simplejson.loads(ThirdPsartyLogin.objects.get(user_id=request.user.id).data)
                    nickname=data['nickname']
                    ScoreRank(my_id=otherId,other_id=request.user.id,score=args['score'],nickname=nickname).save()
                args['rank']=ScoreRank.objects.filter(score__gte=args['score']).count()
                return render(request,'Sorce.html',args,)
            else:
                errors=infoFrom.errors.items()
                args={'errors':errors,'result':'error'}
            json=simplejson.dumps(args)
            return HttpResponse(json, mimetype='application/json')
        elif ScoreRank.objects.filter(my_id=otherId,other_id=request.user.id).exists():
            args['score']=int(ScoreRank.objects.get(my_id=otherId,other_id=request.user.id).score)
            args['rank']=ScoreRank.objects.filter(score__gte=args['score']).count()
            from apps.weixin_app.method import has_share_in_game
            args['has_share']=has_share_in_game(request.user.id)
            return render(request,'Sorce.html',args,)
        elif UserProfile.objects.filter(user_id=request.user.id).exclude(income=-1,education=-1).exists() \
             and UserTag.objects.filter(user_id=request.user.id,type=0).exists():
             args['result']='success'
             args['score']=int(score(request.user.id,otherId))
             if not ScoreRank.objects.filter(my_id=otherId,other_id=request.user.id).exists():
                data=simplejson.loads(ThirdPsartyLogin.objects.get(user_id=request.user.id).data)
                nickname=data['nickname']
                ScoreRank(my_id=otherId,other_id=request.user.id,score=args['score'],nickname=nickname).save()
             args['rank']=ScoreRank.objects.filter(score__gte=args['score']).count()
             from apps.weixin_app.method import has_share_in_game
             args['has_share']=has_share_in_game(request.user.id)
             return render(request,'Sorce.html',args,)
        else:
            #获取自己个人标签
            tags=UserTag.objects.get_tags_by_type(user_id=request.user.id,type=0)
            from apps.pojo.tag import tag_to_tagbean
            tagbeanList=tag_to_tagbean(tags)
            args['tagbeanList']=tagbeanList
            args['infoForm']=InfoForm(initial={'height':175,'income':20,'education':2})
            args['country']= 1 if userProfile.country ==None else userProfile.country
        return render(request,'selfInfo.html',args)
    except Exception as e:
        logger.exception('完善信息出错：%s'%(e))
        json=simplejson.dumps({'result':'error','error_message':'出错%s'%(e.message)})
        return HttpResponse(json, mimetype='application/json')
        
'''
别人对我的打分
'''
def score(userId,otherId):
    try:
        from apps.recommend_app.method import get_matchresult
        matchResult=get_matchresult(userId,otherId)
        return matchResult.scoreMyself
    except Exception as e:
        raise e
   
'''
完善我对别人打分信息
'''
def other_info(request):
    args={'PublicWeiXinAppID':PublicWeiXinAppID,'WEIXIN_CALLBACK_URL':'%s%s'%(WEIXIN_CHECK_AUTHORIZATION_URL[:-1],'_url/'),'has_share':False}
    try:
        userProfile=UserProfile.objects.get(user=request.user)
        args['link']=userProfile.link
        from apps.weixin_app.method import has_share_in_game
        if request.method=="POST":
            expectHeight=int(request.REQUEST.get('expectHeight'))
            heightweight=int(request.REQUEST.get('heightweight'))
            incomeweight=int(request.REQUEST.get('incomeweight'))
            educationweight=int(request.REQUEST.get('educationweight'))
            characterweight=int(request.REQUEST.get('characterweight'))
            tagOtherList=request.REQUEST.get('tagOtherList','').split(',')
            from apps.weixin_app.method import cal_expect_height_in_game
            expectHeightList=cal_expect_height_in_game(userProfile.gender,expectHeight)
            UserExpect.objects.create_update_by_uid(user_id=request.user.id,heighty1=expectHeightList[0],heighty2=expectHeightList[1],heighty3=expectHeightList[2],heighty4=expectHeightList[3],\
                                                heighty5=expectHeightList[4] ,heighty6=expectHeightList[5],heighty7=expectHeightList[6],heighty8=expectHeightList[7])
            
            #标签
            if not UserTag.objects.filter(user_id=request.user.id).exists():
                    from apps.user_score_app.method import get_score_by_character_tag
                    get_score_by_character_tag(request.user.id)
            UserTag.objects.bulk_insert_user_tag(request.user.id,1,tagOtherList)
                    
            if Grade.objects.filter(user_id=request.user.id,heightweight=None).exists():
                from apps.user_score_app.method import get_score_by_weight
                get_score_by_weight(request.user.id)
            from apps.weixin_app.method import cal_weight_in_game
            kwargs=cal_weight_in_game({'heightweight':heightweight,\
                                          'incomeweight':incomeweight,'educationweight':educationweight,'characterweight':characterweight,'appearanceweight':0})
            Grade.objects.create_update_grade(request.user.id,**kwargs)
            args['has_share']=True
            args['result']='success'
            return render(request,'share.html',args)
        elif has_share_in_game(request.user.id):
            args.update({'result':'success','has_share':True})
            return render(request,'share.html',args)
        else:
            #获取对另一半期望标签
            tagsForOther=UserTag.objects.get_tags_by_type(user_id=request.user.id,type=1)
            from apps.pojo.tag import tag_to_tagbean
            tagbeanForOtherList=tag_to_tagbean(tagsForOther)
            args['tagbeanForOtherList']=tagbeanForOtherList
            args['gender']=userProfile.gender
            return render(request,'otherInfo.html',args)
        
    except Exception as e:
        logger.exception('完善我对别人打分信息：%s'%(e.message))
        json=simplejson.dumps({'result':'error','error_message':'出错%s:'%(e.message)})
        return HttpResponse(json, mimetype='application/json')
        
