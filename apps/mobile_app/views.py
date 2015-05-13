#-*- coding: UTF-8 -*- 
from apps.user_app.models import UserProfile, UserTag, Follow
import logging
from django.shortcuts import render
from apps.recommend_app.models import Grade, MatchResult, UserExpect
from django.utils import simplejson
from util.page import page
from pinloveweb import settings, STAFF_MEMBERS
from django.db import transaction
from apps.mobile_app.forms import UserProfileMbolieForm
from django.http.response import HttpResponse, HttpResponseRedirect, Http404
from django.views.decorators.http import require_POST
from apps.pojo.card import CardMobileEncoder
from apps.upload_avatar.app_settings import DEFAULT_IMAGE_NAME
from apps.friend_dynamic_app.models import Picture, FriendDynamic
from util.cache import get_has_recommend
from apps.mobile_app.__init__ import ERROR_TEMLATE_NAMR
from apps.recommend_app.recommend_util import recommend_info_status
from apps.search_app.forms import SearchMobileForm
import urllib
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
        return render(request,ERROR_TEMLATE_NAMR,args)
        
   
def get_weight(request,template_name='mobile_weight.html'):
    '''
    获取用户权重
    '''
    args={}
    try:
        from apps.recommend_app.method import get_weight_star
        args=get_weight_star(request.user.id)
        if request.GET.get('guide')==u'1':
            args.update({'guide':True,'title':'第四步：完善权重','guide_next_url':'/mobile/grade_height/?guide=1'})
        return render(request,template_name,args)
    except Exception as e:
        logger.exception(e.message)
        args={'result':'error','error_message':e.message}
        return render(request,ERROR_TEMLATE_NAMR,args)
    
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
                cal_recommend(request.user.id,['info'])     
                args['result']='success'
            else:
                 errors=userProfileForm.errors.items()
                 args={'errors':errors,'result':'error'}
            json=simplejson.dumps(args)
            return HttpResponse(json, mimetype='application/json')
              
        else:
            args['user_profile_form'] = UserProfileMbolieForm(instance=userProfile) 
        from apps.common_app.method import get_school_list_by_country
        args['school_list']=get_school_list_by_country()
        fields=['country','city','stateProvince']
        for field in fields:
            args[field]=getattr(userProfile,field)
        if request.GET.get('guide')==u'1':
            args.update({'guide':True,'title':'第二步：完善个人信息','guide_next_url':'/mobile/character_tag/?guide=1'})
        return render(request,template_name,args)
    except Exception as e:
        logger.exception(e.message)
        args={'result':'error','error_message':e.message}
        return render(request,ERROR_TEMLATE_NAMR,args)


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
        if request.GET.get('guide')==u'1':
            args.update({'guide':True,'title':'第三步：填写性格标签','guide_next_url':'/mobile/get_weight/?guide=1'})
        return render(request,template_name,args)
    except Exception as e:
        logger.exception(e.message)
        args={'result':'error','error_message':e.message}
        return render(request,ERROR_TEMLATE_NAMR,args)
        
def pintu(request,template_name="mobile_pintu.html"):   
    args={}
    try:
        userProfile=UserProfile.objects.get_user_info(request.user.id)
        from pinloveweb.method import init_person_info_for_card_page
        args.update(init_person_info_for_card_page(userProfile))
        return render(request,template_name,args)
    except Exception as e:
        logger.exception(e.message)
        args={'result':'error','error_message':e.message}
        return render(request,ERROR_TEMLATE_NAMR,args)

def verification(request,template_name="mobile_authentication.html"):   
    args={}
    try:
        #认证
        from apps.verification_app.views import verification
        args.update(verification(request))
        return render(request,template_name,args)
    except Exception as e:
        logger.exception(e.message)
        args={'result':'error','error_message':e.message}
        return render(request,ERROR_TEMLATE_NAMR,args)
 
'''
查看关注信息
attribute：
    type(int) 关注类型 :
        1  我的关注   
        2  我的粉丝
        3  相互关注
return：
   page 
'''       
def follow(request,type,ajax='false',template_name="mobile_follow.html"):
    args={}
    try:
        try:
            type=int(type)
        except ValueError:
            raise Http404()
        if type==1:
            #获得我的关注列表
            fllowList=Follow.objects.filter(my=request.user)
            theme='关注'
        elif type==2:
            #获得我的粉丝列表
            fllowList=Follow.objects.filter(follow=request.user)   
            theme='粉丝'
        elif  type==3:
            #获得相互关注列表
            fllowList=Follow.objects.follow_each(request.user.id)
            theme='相互关注'
          
        userProfile=UserProfile.objects.get(user_id=request.user.id)
        #分页
        args=page(request,fllowList)
        cardList=args.get('pages')
        #将关注列表转换成Card列表
        if len(cardList.object_list)>0:
            from apps.pojo.card import fllowList_to_CardMobileList
            cardList.object_list=fllowList_to_CardMobileList(request.user.id,cardList.object_list,type)
        else:
            cardList.object_list=[]
        if cardList.has_next():
            args['next_page_number']=cardList.next_page_number()
        else:
            args['next_page_number']=-1
        #判断推荐完成情况
        recommend_status=recommend_info_status(request.user.id,channel='mobile')
        if recommend_status['result']:
            args['has_recommend']=True
        else:
            args['recommend_finish']=recommend_status['data']
        if request.is_ajax():
            data={}
            if cardList.has_next():
                data['next_page_number']=args['next_page_number']
            else:
                data['next_page_number']=-1
            data['result']='success'
            data['cards']=cardList.object_list
            json=simplejson.dumps(data,cls=CardMobileEncoder)
            return HttpResponse(json)
        cardList.object_list=simplejson.dumps(cardList.object_list,cls=CardMobileEncoder)
        args['pages']=cardList
        from pinloveweb.method import init_person_info_for_card_page
        args.update(init_person_info_for_card_page(userProfile))
        args['title']=theme
        return render(request, template_name,args )
    except Exception as e:
        logger.exception(e.message)
        args={'result':'error','error_message':e.message}
        return render(request,ERROR_TEMLATE_NAMR,args)  
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
        #判断推荐完成情况
        recommend_status=recommend_info_status(request.user.id,channel='mobile')
        if not recommend_status['result']:
            args['has_recommend']=True
        else:
            args['recommend_finish']=recommend_status['data']
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
        args={'result':'error','error_message':e.message}
        return render(request,ERROR_TEMLATE_NAMR,args)

def info_detail(request,userId,template_name='mobile_info.html'):
    args={}
    try:
        from apps.user_app.method import user_info_mobile
        args=user_info_mobile(int(userId),request.user.id,)
        from apps.friend_dynamic_app.method import get_pic
        args['picList']=get_pic(int(userId))
        #获取标签信息
        tagList=UserTag.objects.select_related('tag').filter(user_id=userId,type=0)
        tags=[]
        for tag in tagList:
           if tag.tag.id<24:
               tags.append(tag.tag.content)
        args['tags']=tags
        return render(request, template_name,args )
    except Exception as e:
        logger.exception(e.message)
        args={'result':'error','error_message':e.message}
        return render(request,ERROR_TEMLATE_NAMR,args)
    
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
        args['type']=type
        input='<input type="hidden" name="%s" value="%s">'
        textarea=' <textarea rows="6" class="form-control" id="content" name="%s"></textarea>'
        if type==u'message':
            args['url']='/message/send/'
            args['inputHtml']=input%('receiver_id',request.REQUEST.get('receiver_id'))
            args['textarea']=textarea%('reply_content')
        elif  type==u'dynamic_comment':
            args['url']='/dynamic/comment/'
            args['textarea']=textarea%('content')
            args['inputHtml']=input%('receiverId',request.REQUEST.get('receiver_id'))+' '+input%('dynamicId',request.REQUEST.get('dynamicId'))
        elif type==u'dynamic':
            args['url']='/dynamic/send/'
            args['upload']=True
            args['textarea']=textarea%('content')
        else:
            raise Exception()
        args['type']=type
        return render(request,template_name,args)
    except Exception,e:
        logger.exception('文本编辑页面,出错!')
        args={'result':'error','error_message':e.message}
        return render(request,ERROR_TEMLATE_NAMR,args)
    
def search(request,template_name='mobile_search.html'):
    '''
    搜索页面
    '''
    args={}
    try:
        userProfile=UserProfile.objects.get_user_info(request.user.id)
        if request.method=='POST':
                searchForm=SearchMobileForm(request.POST)
                if searchForm.is_valid():
                    userProfileList=searchForm.select_data(request.REQUEST.get('sunSign','').rstrip(),userProfile.gender,request.user.id)
                    args=page(request,userProfileList)
                    searchList=args['pages']
                    from apps.pojo.card import userProfileList_to_CardMobileList
                    searchList.object_list=userProfileList_to_CardMobileList(request.user.id,searchList.object_list)
                    searchList.object_list=simplejson.dumps(searchList.object_list,cls=CardMobileEncoder)
                    args['pages']=searchList
                    from pinloveweb.method import init_person_info_for_card_page
                    args.update(init_person_info_for_card_page(userProfile))
                    args['result']='success'
                    POSTcopy=request.POST.copy()
                    POSTcopy.pop('csrfmiddlewaretoken')
                    args['url']=(request.path+'?'+urllib.urlencode(POSTcopy))
                    return render(request, 'mobile_search_result.html',args)
        elif request.is_ajax():
            searchForm=SearchMobileForm(request.GET)
            if searchForm.is_valid():
                userProfileList=searchForm.select_data(request.REQUEST.get('sunSign','').rstrip(),userProfile.gender,request.user.id)
                args=page(request,userProfileList)
                searchList=args['pages']
                from apps.pojo.card import userProfileList_to_CardMobileList
                searchList.object_list=userProfileList_to_CardMobileList(request.user.id,searchList.object_list)
                searchList.object_list=simplejson.dumps(searchList.object_list,cls=CardMobileEncoder)
                args['pages']=searchList
                args['result']='success'
                
        else:
            searchForm=SearchMobileForm()
            searchForm.init_search_condition(request.user.id)
            from apps.search_app.views import get_disable_condition
            args.update(get_disable_condition(userProfile))
            args['searchForm']=searchForm
            from apps.search_app.forms import SUN_SIGN_CHOOSICE
            args['sunSign']=SUN_SIGN_CHOOSICE
            from pinloveweb.method import get_no_read_web_count
            args.update(get_no_read_web_count(request.user.id,fromPage=u'card'))
            args['result']='success'
        if args.get('result',False) !='success':
            args['result']='error'
            args['error_message']=[]
            errorList=searchForm.errors.items()
            for error in errorList:
                args['error_message'].append([SearchMobileForm.base_fields[error[0]].label,error[1][0]])
            json=simplejson.dumps(args)
            return HttpResponse(json)
    except Exception as e:
        error_message='搜索也卖弄出错：出错原因：'+e.message
        logger.exception(error_message)
        args['result']='success'
        args['error_message']=error_message
        template_name='error.html'
    if request.is_ajax():
            from pinloveweb.method import load_cards_by_ajax
            return load_cards_by_ajax(request,searchList,chanel='mobile')
    else:
        return render(request,template_name,args)
    
    
    
    
    
#     args={}
#     try:
#         userProfile=UserProfile.objects.get_user_info(request.user.id)
#         from apps.search_app.forms import SearchMobileForm
#         if request.method=='POST':
#                 searchForm=SearchMobileForm(request.POST)
#                 if searchForm.is_valid():
#                     searchSql={}
#                     minAge=searchForm.cleaned_data['minAge'] if searchForm.cleaned_data['minAge']!=u'' else 0
#                     maxAge=searchForm.cleaned_data['maxAge'] if searchForm.cleaned_data['maxAge']!=u'' else 10000
#                     education=searchForm.cleaned_data['education'] if searchForm.cleaned_data['education'] !=u'' else -1
#                     minIcome=searchForm.cleaned_data['minIcome'] if searchForm.cleaned_data['minIcome']!=u'' else 0
#                     maxIncome=searchForm.cleaned_data['maxIncome'] if searchForm.cleaned_data['maxIncome'] !=u'' else 100000 
#                     #最大收入为不限
#                     if maxIncome=='-1':
#                         maxIncome='100000'
#                     minHeigh=searchForm.cleaned_data['minHeigh'] if searchForm.cleaned_data['minHeigh']!=u'' else 0
#                     maxHeigh=searchForm.cleaned_data['maxHeigh'] if searchForm.cleaned_data['maxHeigh']!=u'' else 1000
#                     sunSign=request.REQUEST.get('sunSign','').rstrip()
#                     if len(sunSign)>0:
#                         sunSign=[int(sunSignBean)for sunSignBean in sunSign.split(',')]
#                         searchSql['sunSign__in']=sunSign
#                     jobIndustry=searchForm.cleaned_data['jobIndustry']
#                     if jobIndustry!='None' and jobIndustry!=u'':
#                         searchSql['jobIndustry']=jobIndustry
#                     if education=='0':
#                         searchSql['education']=education
#                     userProfileList=UserProfile.objects.select_related('user').filter(age__gte=minAge,age__lte=maxAge,education__gte=education,income__gte=minIcome,income__lte=maxIncome,
#                                                height__gte=minHeigh,height__lte=maxHeigh,**searchSql).exclude(gender=userProfile.gender).exclude(user=request.user).filter(avatar_name_status='3').exclude(user_id__in=STAFF_MEMBERS)
#                     args=page(request,userProfileList)
#                     searchList=args['pages']
#                     from apps.pojo.card import userProfileList_to_CardMobileList
#                     searchList.object_list=userProfileList_to_CardMobileList(request.user.id,searchList.object_list)
#                     searchList.object_list=simplejson.dumps(searchList.object_list,cls=CardMobileEncoder)
#                     args['pages']=searchList
#                     from pinloveweb.method import init_person_info_for_card_page
#                     args.update(init_person_info_for_card_page(userProfile))
#                     return render(request, 'mobile_search_result.html',args)
#         
#         else:
#             from apps.search_app.views import init_search_condition
#             initial=init_search_condition(request.user.id)
#             searchForm=SearchMobileForm(initial=initial)
#         from apps.search_app.views import get_disable_condition
#         args.update(get_disable_condition(userProfile))
#         args['searchForm']=searchForm
#         from apps.search_app.forms import SUN_SIGN_CHOOSICE
#         args['sunSign']=SUN_SIGN_CHOOSICE
# #             from pinloveweb.method import get_no_read_web_count
# #             args.update(get_no_read_web_count(request.user.id,fromPage=u'card'))
#         if request.is_ajax():
#             from pinloveweb.method import load_cards_by_ajax
#             return load_cards_by_ajax(request,searchList,chanel='mobile')
#         else:
#             return render(request, template_name,args)
#     except Exception as e:
#         logger.exception('搜索,出错!')
#         args={'result':'error','error_message':e.message}
#         return render(request,ERROR_TEMLATE_NAMR,args)
  
  
def update_radar_compare(request,template_name='mobile_recommend.html'):
    '''
    雷达图对比
    '''
    args={}
    try:
        type=request.REQUEST.get('type',False)
        url=request.REQUEST.get('prevUrl')
        if not type :
            raise Exception('传入参数错误!')
        if type=='add':
            request.session['radar_compare_id']=int(request.REQUEST['userId'])
            request.session['radar_compare']=True
            from util.util import is_guide
            guide=UserProfile.objects.get(user=request.user).guide
            if not is_guide(request.user.id,guide,'compareButton'):
                url='%s%s'%(url,'?compare_guide=true')
        elif type=='del':
            del request.session['radar_compare']
        else:
            raise Exception('传入参数错误!')
        return HttpResponseRedirect(url)
    except Exception as e:
        logger.exception(e.message)
        args={'result':'error','error_message':e.message}
        return render(request,ERROR_TEMLATE_NAMR,args)
    
def grade_height(request,template_name='mobile_height.html'):
    '''
    身高打分
    '''
    args={}
    try:
        #获得另一半身高期望   
        userExpect=UserExpect.objects.get_user_expect_by_uid(request.user.id)
        if userExpect==None:
            args['grade_for_other']=False
        else:
            args['grade_for_other']=userExpect
        if request.GET.get('guide')==u'1':
            args.update({'guide':True,'title':'第五步：Ta的身高打分','guide_next_url':'/mobile/loggedin/?previous_page=register'})
        return render(request,template_name,args)
    except Exception as e:
        logger.exception(e.message)
        args={'result':'error','error_message':e.message}
        return render(request,ERROR_TEMLATE_NAMR,args)
  

def update_avtar(request,template_name='mobile_upload_avatar.html'):
    '''
    上传头像
    '''
    args={}
    try:
        from apps.upload_avatar import get_uploadavatar_context
        args=get_uploadavatar_context()
        args['image']=request.GET.get('image')
        if request.GET.get('guide')==u'1':
            args.update({'image':'/static/img/信息设置-29.png','guide':True,'title':'第一步：上传头像','guide_next_url':'/mobile/profile/?guide=1'})
        return render(request,template_name,args)
    except Exception as e:
        logger.exception(e.message)
        args={'result':'error','error_message':e.message}
        return render(request,ERROR_TEMLATE_NAMR,args)
    
def radar(request,userId,template_name='mobile_radar.html'):
    '''
    雷达图
    '''
    args={}
    try:
        radarList=[]
        userIdList=[]
        radarCompare=request.session.get('radar_compare',False)
        from apps.recommend_app.views import get_socre_for_other
        if radarCompare:
            compareId=request.session.get('radar_compare_id')
            userIdList.append(compareId)
        userIdList.append(userId)
        for userId in userIdList:
            socreForOther=get_socre_for_other(request.user.id,userId)
            userProfile=UserProfile.objects.get(user_id=userId)
            radarList.append({
                         'head' : '%s%s%s'%('/media/', userProfile.avatar_name if userProfile.avatar_name_status=='3' else DEFAULT_IMAGE_NAME,'-100.jpeg'),
                    'userId':userProfile.user_id,
                     'score' :int(socreForOther['matchResult']['scoreOther']),
                        'scoreMy':int(socreForOther['matchResult'].get('scoreMyself',-3)),
                        'data' : [socreForOther['matchResult']['edcationScore'],socreForOther['matchResult']['characterScore'],socreForOther['matchResult']['incomeScore'],socreForOther['matchResult']['appearanceScore'],socreForOther['matchResult']['heighScore'],]
                     })
            
        args['radarList']=simplejson.dumps(radarList)
        return render(request, template_name,args )
    except Exception as e:
        logger.exception(e.message)
        args={'result':'error','error_message':e.message}
        return render(request,ERROR_TEMLATE_NAMR,args)
          
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
        #判断推荐完成情况
        recommend_status=recommend_info_status(request.user.id,channel='mobile')
        if not recommend_status['result']:
            args['has_recommend']=True
        else:
            args['recommend_finish']=simplejson.dumps(simplejson.dumps(recommend_status['data']))
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
        #推荐信息完善
        if request.session.get('recommendStatus',False):
            args['recommendStatus']=request.session.pop('recommendStatus')
        from pinloveweb.method import init_person_info_for_card_page
        args.update(init_person_info_for_card_page(userProfile))
        return render(request, template_name,args )
    except Exception as e:
        logger.exception(e.message)
        args={'result':'error','error_message':e.message}
        return render(request,ERROR_TEMLATE_NAMR,args)
    
    
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

