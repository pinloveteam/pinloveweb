#-*- coding: UTF-8 -*- 
from apps.user_app.models import UserProfile, UserTag
import logging
from django.shortcuts import render
from apps.recommend_app.models import Grade, MatchResult
from django.utils import simplejson
from util.page import page
from pinloveweb import settings, STAFF_MEMBERS
from django.db import transaction
from apps.mobile_app.forms import UserProfileMbolieForm
from django.http.response import HttpResponse
from django.views.decorators.http import require_POST
from apps.pojo.card import CardMobileEncoder
logger=logging.getLogger(__name__)

def account(request):
    '''
    获得账户信息
    '''
    args={}
    try:
        userProfile=UserProfile.objects.get(user=request.user) 
        args['avatar_name']=userProfile.avatar_name
        from apps.pay_app.method import get_charge_amount
        args['pinLoveIcon']=get_charge_amount(userId=request.user)
        return render(request,'mobile_account.html',args)
    except Exception as e:
        logger.exception('手机获取账户信息出错：'+e.message)
        args={'result':'error','error_message':e.message}
        return render(request,'error.html',args)
        
        
def get_weight(request,template_name='mobile_weight.html'):
    '''
    获取用户权重
    '''
    args={}
    try:
        grade=Grade.objects.filter(user_id=request.user.id)
        if len(grade)==0:
            for field in ['heightweight','incomeweight','educationweight','appearanceweight','characterweight']:
                args[field]=0
        else:
            for field in ['heightweight','incomeweight','educationweight','appearanceweight','characterweight']:
                value=getattr(grade[0],field)
                if value==None:
                    value=0;
                args[field]=int(value*100)
        return render(request,template_name,args)
    except Exception as e:
        logger.exception(e.message)
        args={'result':'error.html','error_message':e.message}
        return render(request,'error.html',args)
    
@transaction.commit_on_success   
def profile(request,template_name='mobile_profile.html'):
    '''
    个人信息页面
    '''
    args={}
    try:
        userProfile = UserProfile.objects.get(user_id=request.user.id)
        args['gender']=userProfile.get_gender_display()
        if request.method=="POST":
            import copy
            oldUserProfile=copy.deepcopy(userProfile)
            POSTdata=request.POST.copy()
            userProfileForm = UserProfileMbolieForm(POSTdata, instance=userProfile) 
            if userProfileForm.is_valid():
                #保存 user_profle信息
                userProfile = userProfileForm.save(commit=False)
                #计算资料完成度
                from apps.user_app.method import get_profile_finish_percent_and_score
                userProfile=get_profile_finish_percent_and_score(userProfile,oldUserProfile)
                userProfile.save(oldUserProfile=oldUserProfile)
                #判断推荐条件是否完善
                from apps.recommend_app.recommend_util import cal_recommend
                cal_recommend(request.user.id,['userProfile'])     
                args['result']='success'
                return render(request,template_name,args)
            else:
                args['user_profile_form'] = userProfileForm
              
        else:
            args['user_profile_form'] = UserProfileMbolieForm(instance=userProfile) 
        from apps.common_app.method import get_school_list_by_country
        args['school_list']=get_school_list_by_country()
        fields=['country','city','stateProvince']
        for field in fields:
            args[field]=getattr(userProfile,field)
        return render(request,template_name,args)
    except Exception as e:
        logger.exception(e.message)
        args={'result':'error.html','error_message':e.message}
        return render(request,'error.html',args)


def character_tag(request,template_name='mobile_personality.html'):
    '''
    性格标签页面
    '''
    args={}
    try:
        #获取自己个人标签
        tags=UserTag.objects.get_tags_by_type(user_id=request.user.id,type=0)
        from apps.pojo.tag import tag_to_tagbean
        args['tagbeanList']=tag_to_tagbean(tags)
        #获取对另一半期望标签
        tagsForOther=UserTag.objects.get_tags_by_type(user_id=request.user.id,type=1)
        tagbeanForOtherList=tag_to_tagbean(tagsForOther)
        args['tagbeanForOtherList']=tagbeanForOtherList
        return render(request,template_name,args)
    except Exception as e:
        logger.exception(e.message)
        args={'result':'error.html','error_message':e.message}
        return render(request,'error.html',args)
        
def pintu(request,template_name="mobile_pintu.html"):   
    args={}
    try:
        userProfile=UserProfile.objects.get_user_info(request.user.id)
        from pinloveweb.method import init_person_info_for_card_page
        args.update(init_person_info_for_card_page(userProfile))
        return render(request,template_name,args)
    except Exception as e:
        logger.exception(e.message)
        args={'result':'error.html','error_message':e.message}
        return render(request,'error.html',args)
 
 
def nearby(request,template_name="mobile_neardy.html"):
    '''
    附近的人
    '''
    args={}
    try:
        userProfile=UserProfile.objects.get_user_info(request.user.id)
        from apps.the_people_nearby.views import GetLocation
        userProfileList =  UserProfile.objects.filter(lastLoginAddress=GetLocation(request)).exclude(user=request.user).filter(avatar_name_status='3').exclude(gender=userProfile.gender)
        #分页
        args=page(request,userProfileList)
        userList=args['pages']
        if len(userList.object_list)>0:
            from apps.pojo.card import userProfileList_to_CardMobileList
            userList.object_list=userProfileList_to_CardMobileList(request.user.id,userList.object_list)
        else:
            userList.object_list=[]
        if request.is_ajax():
            from pinloveweb.method import load_cards_by_ajax
            return load_cards_by_ajax(request,userList,chanel='mobile')
        userList.object_list=simplejson.dumps(userList.object_list,cls=CardMobileEncoder)
        args['pages']=userList
        from pinloveweb.method import init_person_info_for_card_page
        args.update(init_person_info_for_card_page(userProfile))
        return render(request, template_name,args )
    except Exception as e:
        logger.exception(e.message)
        args={'result':'error.html','error_message':e.message}
        return render(request,'error.html',args)

def info_detail(request,userId,template_name='mobile_info.html'):
    args={}
    try:
        from apps.user_app.method import user_info_mobile
        args=user_info_mobile(int(userId),request.user.id,)
        from apps.friend_dynamic_app.method import get_pic
        args['picList']=get_pic(request.user.id)
        return render(request, template_name,args )
    except Exception as e:
        logger.exception(e.message)
        args={'result':'error.html','error_message':e.message}
        return render(request,'error.html',args)
    
@require_POST
def user_vote(request):
    '''
    用户投票
    '''
    args={}
    try:
        score = float(request.REQUEST.get('score').strip())
        userId=int(request.REQUEST.get('userId'))
        if score <0 or score >100:
            args={'result':'error','error_message':u'分数必须在1~100范围内!'}
        elif score=='':
            args={'result':'error','error_message':u'不能为空!'}
        else:
            geadeInstance=Grade.objects.get(user_id=userId)
            from apps.recommend_app.recommend_util import cal_user_vote
            score=cal_user_vote(request.user.id,userId,score,geadeInstance.appearancescore,geadeInstance.appearancesvote,1)
            Grade.objects.filter(user_id=userId).update(appearancescore=score['score'],appearancesvote=geadeInstance.appearancesvote if score['flag'] else geadeInstance.appearancesvote+1)
            args={'result':'success','score' : score}
        json = simplejson.dumps(args)
        return HttpResponse(json)
    except Exception,e:
        logger.exception('用户投票,出错!')
        args={'result':'error','error_message':e.message}
        json = simplejson.dumps(args)
        return HttpResponse(json)
    
def editer(request,template_name='mobile_editer.html'):
    '''
    文本编辑页面
    '''
    args={}
    try:
        type=request.REQUEST.get('type')
        if type==u'message':
            args['receiver_id']=request.REQUEST.get('receiver_id')
        else:
            args['receiver_id']=request.REQUEST.get('receiver_id')
        args['type']=type
        return render(request,template_name,args)
    except Exception,e:
        logger.exception('文本编辑页面,出错!')
        args={'result':'error.html','error_message':e.message}
        return render(request,'error.html',args)
    
def search(request,template_name='mobile_search.html'):
    '''
    搜索页面
    '''
    args={}
    try:
        userProfile=UserProfile.objects.get_user_info(request.user.id)
        from apps.search_app.forms import SearchMobileForm
        if request.method=='POST':
                searchForm=SearchMobileForm(request.POST)
                if searchForm.is_valid():
                    searchSql={}
                    minAge=searchForm.cleaned_data['minAge'] if searchForm.cleaned_data['minAge']!=u'' else 0
                    maxAge=searchForm.cleaned_data['maxAge'] if searchForm.cleaned_data['maxAge']!=u'' else 10000
                    education=searchForm.cleaned_data['education'] if searchForm.cleaned_data['education'] !=u'' else -1
                    minIcome=searchForm.cleaned_data['minIcome'] if searchForm.cleaned_data['minIcome']!=u'' else 0
                    maxIncome=searchForm.cleaned_data['maxIncome'] if searchForm.cleaned_data['maxIncome'] !=u'' else 100000 
                    #最大收入为不限
                    if maxIncome=='-1':
                        maxIncome='100000'
                    minHeigh=searchForm.cleaned_data['minHeigh'] if searchForm.cleaned_data['minHeigh']!=u'' else 0
                    maxHeigh=searchForm.cleaned_data['maxHeigh'] if searchForm.cleaned_data['maxHeigh']!=u'' else 1000
                    sunSign=request.REQUEST.get('sunSign','').rstrip()
                    if len(sunSign)>0:
                        sunSign=[int(sunSignBean)for sunSignBean in sunSign.split(',')]
                        searchSql['sunSign__in']=sunSign
                    jobIndustry=searchForm.cleaned_data['jobIndustry']
                    if jobIndustry!='None' and jobIndustry!=u'':
                        searchSql['jobIndustry']=jobIndustry
                    if education=='0':
                        searchSql['education']=education
                    userProfileList=UserProfile.objects.select_related('user').filter(age__gte=minAge,age__lte=maxAge,education__gte=education,income__gte=minIcome,income__lte=maxIncome,
                                               height__gte=minHeigh,height__lte=maxHeigh,**searchSql).exclude(gender=userProfile.gender).exclude(user=request.user).filter(avatar_name_status='3').exclude(user_id__in=STAFF_MEMBERS)
                    args=page(request,userProfileList)
                    searchList=args['pages']
                    from apps.pojo.card import userProfileList_to_CardMobileList
                    searchList.object_list=userProfileList_to_CardMobileList(request.user.id,searchList.object_list)
                    searchList.object_list=simplejson.dumps(searchList.object_list,cls=CardMobileEncoder)
                    args['pages']=searchList
                    return render(request, 'mobile_search_result.html',args)
        
        else:
            from apps.search_app.views import init_search_condition
            initial=init_search_condition(request.user.id)
            searchForm=SearchMobileForm(initial=initial)
            from apps.search_app.views import get_disable_condition
            args.update(get_disable_condition(userProfile))
            args['searchForm']=searchForm
            from apps.search_app.forms import SUN_SIGN_CHOOSICE
            args['sunSign']=SUN_SIGN_CHOOSICE
#             from pinloveweb.method import get_no_read_web_count
#             args.update(get_no_read_web_count(request.user.id,fromPage=u'card'))
        if request.is_ajax():
            from pinloveweb.method import load_cards_by_ajax
            return load_cards_by_ajax(request,searchList,chanel='mobile')
        else:
            return render(request, template_name,args)
    except Exception as e:
        logger.exception('搜索,出错!')
        args={'result':'error.html','error_message':e.message}
        return render(request,'error.html',args)
    
def recommend(request,template_name='mobile_recommend.html',**kwargs):
    '''
    推荐功能
    '''
    args={}
    try:
        #判断推荐分数是否生成
        flag=MatchResult.objects.is_exist_by_userid(request.user.id)
        userProfile=UserProfile.objects.get_user_info(request.user.id)
        #从缓存中获取不推荐用户id
        from util.cache import get_no_recomend_list_by_cache
        disLikeUserIdList=get_no_recomend_list_by_cache(request.user.id)
        #获取推荐列表
        matchResultList=get_recommend_list(request,flag,disLikeUserIdList,userProfile,**kwargs)
        from pinloveweb.method import get_no_read_web_count
        args.update(get_no_read_web_count(request.user.id,fromPage=u'card'))
        if kwargs.get('card')==True:
            return matchResultList
        if request.is_ajax():
            from pinloveweb.method import load_cards_by_ajax
            return load_cards_by_ajax(request,matchResultList,chanel='mobile')
        matchResultList.object_list=simplejson.dumps(matchResultList.object_list,cls=CardMobileEncoder)
        args['pages']=matchResultList
        #判断是否是从注册页面过来
        if request.GET.get('previous_page','')=='register':
            args['first']=True
        from pinloveweb.method import init_person_info_for_card_page
        args.update(init_person_info_for_card_page(userProfile))
        return render(request, template_name,args )
    except Exception as e:
        logger.exception(e.message)
        args={'result':'error.html','error_message':e.message}
        return render(request,'error.html',args)
    
    
def get_recommend_list(request,flag,disLikeUserIdList,userProfile,**kwargs):
    if flag:
         matchResultList=MatchResult.objects.get_match_result_by_userid(request.user.id,disLikeUserIdList)
         arg=page(request,matchResultList,**kwargs)
         matchResultList=arg['pages']
         from apps.pojo.card import matchResultList_to_CardMobileList
         matchResultList.object_list=matchResultList_to_CardMobileList(request.user.id,matchResultList.object_list)
    else:
          if disLikeUserIdList is None: 
              userProfileList=UserProfile.objects.filter(avatar_name_status='3').exclude(gender=userProfile.gender).exclude(user_id__in=STAFF_MEMBERS,)
          else:
              userProfileList=UserProfile.objects.filter(avatar_name_status='3').exclude(user_id__in=disLikeUserIdList).exclude(gender=userProfile.gender).exclude(user_id__in=STAFF_MEMBERS)
          arg=page(request,userProfileList,**kwargs)   
          matchResultList=arg['pages']
          from apps.pojo.card import userProfileList_to_CardMobileList
          matchResultList.object_list=userProfileList_to_CardMobileList(request.user.id,matchResultList.object_list)
    return matchResultList

