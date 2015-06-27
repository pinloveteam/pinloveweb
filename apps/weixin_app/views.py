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
from pinloveweb import STAFF_MEMBERS
import urllib2
from util.connection_db import connection_to_db
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
        again=request.REQUEST.get('again',False)
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
            scoreRankBeanbList=ScoreRank.objects.get_rank_list(request.user.id)
            scoreRankList=[]
            for scoreRankBean in scoreRankBeanbList:
                avatar_name=UserProfile.objects.get(user_id=scoreRankBean.other_id).avatar_name
                scoreRankList.append({'nickname':scoreRankBean.nickname,'score':int(scoreRankBean.score),\
                                  'avatar_name':avatar_name,'other_id':scoreRankBean.other_id,'rank':scoreRankBean.rank})
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
                #期望身高计算
                from apps.weixin_app.method import cal_expect_height_in_game
                expectHeightList=cal_expect_height_in_game(userProfile.gender,int(userProfile.height)-5 if userProfile.gender=='M' else int(userProfile.height)+5)
                UserExpect.objects.create_update_by_uid(user_id=request.user.id,heighty1=expectHeightList[0],heighty2=expectHeightList[1],heighty3=expectHeightList[2],heighty4=expectHeightList[3],\
                                                heighty5=expectHeightList[4] ,heighty6=expectHeightList[5],heighty7=expectHeightList[6],heighty8=expectHeightList[7])
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
        if ScoreRank.objects.filter(my_id=otherId,other_id=request.user.id).exists() and not again:
            return HttpResponseRedirect("/weixin/score/?userKey=%s"%(userKey))
        elif UserProfile.objects.filter(user_id=request.user.id).exclude(income=-1,education=-1).exists() and not again:
           if UserTag.objects.filter(user_id=request.user.id,type=0).exists():
             return HttpResponseRedirect("/weixin/score/?userKey=%s"%(userKey))
           else:
            return my_character(request)
        try:
            ip=request.META['HTTP_X_FORWARDED_FOR'] if 'HTTP_X_FORWARDED_FOR' in request.META else  request.META['REMOTE_ADDR']
            f=urllib2.urlopen('%s%s'%('http://freegeoip.net/json/',ip),timeout = 6).read()
            locationInfo= simplejson.loads(f)
            country=locationInfo.get('country_code',None)
        except Exception as e:
            country=None
        args['infoForm']=InfoForm(instance=userProfile,initial={'country':country})
        return render(request,'selfInfo.html',args)
 
   
def my_character(request,template_name='character_tag.html'):
    '''
    填写我的性格标签
    '''
    args={}
    try:
        userKey=request.REQUEST.get('userKey')
        args=common(request)
        args.update({"userKey":userKey,"tag_name":"选择最符合您的性格描述:","step":"第二步","title":"再测测您的软实力,请选择性格标签",'url':'/weixin/my_character/'})
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
        args['userId']=request.user.id
        args['userKey']=userKey
        try:
            otherProfile=UserProfile.objects.select_related('user').get(link=userKey)
            otherId=otherProfile.user_id
            args['username']=otherProfile.user
        except UserProfile.DoesNotExist as e:
            return render(request,'error.html',{'result':'error','error_message':'没有这个用户，请联系客服!'})
        except UserProfile.MultipleObjectsReturned as e:
                return render(request,'error.html',{'result':'error','error_message':'有多个用户，请联系客服!'})

        from apps.recommend_app.method import match_score
        socreForOther=match_score(otherId,request.user.id).get_dict()
        args.update({'data' : [int(socreForOther['edcationScore']),int(socreForOther['characterScore']),\
                int(socreForOther['incomeScore']),\
                int(socreForOther['heighScore']),],'score' :int(socreForOther['scoreOther'])})
        data=simplejson.loads(ThirdPsartyLogin.objects.get(user_id=request.user.id).data)
        nickname=data['nickname']
        if not ScoreRank.objects.filter(my_id=otherId,other_id=request.user.id).exists():
            ScoreRank(my_id=otherId,other_id=request.user.id,score=args['score'],nickname=nickname,data=simplejson.dumps(args['data'])).save()
        else:
            ScoreRank.objects.filter(my_id=otherId,other_id=request.user.id).update(score=args['score'],nickname=nickname,data=simplejson.dumps(args['data']))
       
        args['rank']=(ScoreRank.objects.filter(my_id=otherId,score__gt=args['score']).count()+1)
        filedList={'MM':u'你和%s的基友指数'%(otherProfile.user),'FF':u'你和%s的闺蜜指数'%(otherProfile.user),'MF':u'你在女神%s心中的亲密指数'%(otherProfile.user),'FM':u'你在男神%s心中的亲密指数'%(request.user),}
        args['score_content']=filedList[u'%s%s'%(userProfile.gender,otherProfile.gender)]
        #判断他的条件是否成立
        if (not Grade.objects.filter(user_id=request.user.id,heightweight=None,incomeweight=None,educationweight=None,characterweight=None)) and UserTag.objects.filter(user_id=request.user.id).exists():
            args['is_recommend']=True
            args['has_share']=True
        else:
            args['is_recommend']=False
            args['next_url']='/weixin/ta_character/'
        scoreRankBeanbList=ScoreRank.objects.get_rank_list(otherId)
        scoreRankList=[]
        for scoreRankBean in scoreRankBeanbList:
            avatar_name=UserProfile.objects.get(user_id=scoreRankBean.other_id).avatar_name
            is_self=False
            if int(scoreRankBean.other_id)==int(request.user.id):
                is_self=True
            scoreRankList.append({'nickname':scoreRankBean.nickname,'score':int(scoreRankBean.score),\
                                  'avatar_name':avatar_name,'other_id':scoreRankBean.other_id,'rank':scoreRankBean.rank,'is_self':is_self})
        args.update({'scoreRankList':scoreRankList,'count':len(scoreRankList)})
            
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
                if Grade.objects.filter(user_id=request.user.id,heightweight=None).exists():
                    from apps.user_score_app.method import get_score_by_weight
                    get_score_by_weight(request.user.id)
                grade=taInfoForm.cal_weight(request.user.id)
                grade.save()
                args.update({'result':'success'})
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
        args.update({"step":"第三步","tag_name":"希望Ta具备的性格:","title":"选出你心目中男神、女神的标准",'next_url':'/weixin/other_info/'})
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
    
def share_userlist(request,template_name="share_user.html",remcommend_limit=5,limit=18):
    '''
    分享用户列表
    '''
    args={}
    try:
        userProfile=UserProfile.objects.get(user=request.user)
        #推荐用户
        userProfileList=UserProfile.objects.select_related('user').filter(avatar_name_status='3').exclude(gender=userProfile.gender).exclude(user_id__in=STAFF_MEMBERS)[:remcommend_limit]
        userlist=[{'userId':user.user_id,'username':user.user.username,'avatar':user.avatar_name} for user in userProfileList]
        userIdList=[str(user['userId']) for user in userlist]
        count=len(userProfileList)
        sql='''
        SELECT %s from third_party_login u1 left join user_profile u4 on u1.user_id =u4.user_id 
left join auth_user u2 on u1.user_id=u2.id
 where u1.provider='3' and exists (select my_id from weixin_score_rank u3 where u1.user_id=u3.my_id) 
and u4.gender !='%s'  and u1.user_id not in (1%s)
order by  u2.last_login desc %s
        '''
        #分享人数
        count+=connection_to_db(sql%('count(*)',userProfile.gender,','+','.join(userIdList),''))[0][0]
        scoreRankList=connection_to_db(sql%('u1.user_id,u2.username,u4.avatar_name',userProfile.gender,','+','.join(userIdList),'limit %s'%(limit)),type=True)
        userlist+=[{'userId':user['user_id'],'username':user['username'],'avatar':user['avatar_name']} for user in scoreRankList]
        args['userlist']=userlist
        args['count']=count
    except Exception as e:
        logger.exception('完善我对别人打分信息：%s'%(e.message))
        args={'result':'error','error_message':(e.message)}
        template_name='error.html'
    return render(request,template_name,args)
        
def compare(request,template_name=None):
    '''
    雷达图对比
    '''
    args={'result':'success'}
    try:
        link=request.GET.get('link')
        userId=int(request.GET.get('userId'))
        userProfile=UserProfile.objects.get(link=link)
        scoreRankList=ScoreRank.objects.filter(my_id=userProfile.user_id,other_id__in=[userId,request.user.id])
        args['data']=[simplejson.loads(scoreRank.data) for scoreRank in scoreRankList]
        
    except Exception as e:
        logger.exception('雷达图对比：%s'%(e.message))
        args={'result':'error','error_message':(e.message)}
    json=simplejson.dumps(args)
    return HttpResponse(json)
def test(request):
    return render(request,'index_1.html',{})
    