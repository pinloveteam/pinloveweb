# -*- coding: utf-8 -*-
'''
Created on Jul 4, 2013

@author: jin
'''
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.views.decorators.csrf import csrf_protect
from django.template.context import RequestContext
from apps.user_app.models import UserProfile,UserContactLink,Follow,Verification,\
    UserTag
from apps.user_app.forms import UserBasicProfileForm, UserContactForm,UserAppearanceForm, UserStudyWorkForm, UserPersonalHabitForm,\
    UserFamilyInformationForm, UserProfileForm
from django.core.context_processors import csrf 

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from PIL import ImageFile
from apps.upload_avatar import get_uploadavatar_context
from django.contrib import auth
from apps.recommend_app.models import Grade, UserExpect
from util.page import page
import logging
from util.singal import cal_recommend_user
from apps.pojo.card import MyEncoder
from django.utils import simplejson
from django.db import transaction
from pinloveweb.forms import ChangePasswordForm
logger=logging.getLogger(__name__)

'''
推荐页面移除不喜欢用户
attribute：
 userId： int 移除用户id
 page：  int 当前页面页数
'''
def dislike(request):
    arg={}
    try:
        userId=int(request.GET.get('userId'))
        page=int(request.GET.get('page'))
    except Exception:
            raise '转换失败'
    from apps.recommend_app.method import update_no_recommend_update_black_list
    from util.cache import set_no_recomend_list_by_cache
    if update_no_recommend_update_black_list(request.user.id,userId)==1:
        set_no_recomend_list_by_cache(request.user.id,int(userId))
    #如果没有下一页，则直接移除卡片
    if  page < 0:
        arg['result']='remove_card'
        json=simplejson.dumps(arg)
        return HttpResponse(json)
    #获取分页数据
    from pinloveweb.views import get_recommend_list
    matchResult=get_recommend_list(request,page=page,card=True)
    arg['card']=matchResult.object_list[7]
    if page+1<=matchResult.paginator.num_pages:
        arg['has_next']=True
#     arg['next_page']=matchResult.has_next()
    arg['result']='success'
    json=simplejson.dumps(arg,cls=MyEncoder)
    return HttpResponse(json)
'''
用户详细信息
userId： int 用户id
'''
def detailed_info(request):
    try:
        args={}
        userId=int(request.GET.get('userId'))
        compareId=request.GET.get('compareId',None)
        from apps.user_app.method import detailed_info_div
        if not compareId is None:
            args=detailed_info_div(request.user.id,userId,compareId)
        else:
            args=detailed_info_div(request.user.id,userId)
        #引导
        guide=UserProfile.objects.get(user=request.user).guide
        from util.util import is_guide
        if not is_guide(request.user.id,guide,'compareButton'):
            args['compare_guide']=True
        else:
            args['compare_guide']=False
    except Exception as e:
        logger.exception('用户详细信息，出错!')
        args={'result':'error','error_message':e.message}
    json=simplejson.dumps(args)
    return HttpResponse(json)
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
def follow(request,type,ajax='false'):
    arg={}
    if request.user.is_authenticated() :
        try:
            type=int(type)
        except ValueError:
            raise Http404()
        if type==1:
            #获得我的关注列表
            fllowList=Follow.objects.filter(my=request.user)
        elif type==2:
            #获得我的粉丝列表
            fllowList=Follow.objects.filter(follow=request.user)   
        elif  type==3:
            #获得相互关注列表
            fllowList=Follow.objects.follow_each(request.user.id)
          
        userProfile=UserProfile.objects.get(user_id=request.user.id)
        #分页
        arg=page(request,fllowList)
        cardList=arg.get('pages')
        #将关注列表转换成Card列表
        if len(cardList.object_list)>0:
            from apps.pojo.card import fllowList_to_CardList
            cardList.object_list=fllowList_to_CardList(request.user.id,cardList.object_list,type)
        else:
            cardList.object_list=[]
        if cardList.has_next():
            arg['next_page_number']=cardList.next_page_number()
        else:
            arg['next_page_number']=-1
        if request.is_ajax():
            data={}
            if cardList.has_next():
                data['next_page_number']=arg['next_page_number']
            else:
                data['next_page_number']=-1
            data['result']='success'
            data['cards']=cardList.object_list
            json=simplejson.dumps(data,cls=MyEncoder)
            return HttpResponse(json)
        cardList.object_list=simplejson.dumps(cardList.object_list,cls=MyEncoder)
        arg['pages']=cardList
        from pinloveweb.method import init_person_info_for_card_page
        arg.update(init_person_info_for_card_page(userProfile))
        return render(request, 'member/follow.html',arg )
    else:
        arg = {}
        arg.update(csrf(request))
        return render(request, 'login.html', arg) 
'''
修改关注情况：
attribute：
    userId ：int 用户id
    type:1 关注
return：
    type：
        1 ,-1 我关注的
        2 ,-2 双向关注
        3 ,-3 他关注我的
    content:
         返回提示
'''
def update_follow(request):
  try:
    arg = {}
    type=int(request.GET.get('type',False))
    offset =int(request.GET.get('userId'))
    from util.cache import is_black_list
    if is_black_list(offset,int(request.user.id)):
        arg={'type':'error','error_message':'该用户已经将你拉入黑名单，你不能添加关注!'} 
    elif Follow.objects.filter(my=request.user,follow_id=offset).exists():
        if type==1:
            return HttpResponse(simplejson.dumps({'result':'follow'}))
        Follow.objects.filter(my=request.user,follow=offset).delete()
        if Follow.objects.filter(my_id=offset,follow=request.user).exists():
            arg['type']=-3
        else:
            arg['type']=-1
        arg['content'] = "取消关注"
    else:
        Follow(my_id=request.user.id,follow_id=offset).save()
        #发送消息费被关注的人
        from apps.user_app.user_settings import FOLLOW_MESSAGE
        reply_content=FOLLOW_MESSAGE%(request.user.username,request.user.id)
        from apps.message_app.method import add_message_121
        add_message_121(request.user.id,offset,reply_content,2)
        if Follow.objects.filter(my_id=offset,follow=request.user).exists():
            arg['type']=2
        else:
            arg['type']=1
        arg['content'] = '关注成功'
  except Exception as e:
    arg={'type':'error','error_message':e.message}
  json = simplejson.dumps(arg)
  return HttpResponse(json)

'''
初始化个人信息页面


'''       
def user_profile(request):
        args=get_uploadavatar_context()
        useBasicrProfile = UserProfile.objects.get(user_id=request.user.id)
        #判断出生年月日是否填写
        check_birth=useBasicrProfile.check_birth()
        args['check_birth']=check_birth
        request.session['user_original_data']={'height':useBasicrProfile.height,'education':useBasicrProfile.education,'educationSchool':useBasicrProfile.educationSchool,'income':useBasicrProfile.income}
        #获取自己个人标签
        tags=UserTag.objects.get_tags_by_type(user_id=request.user.id,type=0)
        from apps.pojo.tag import tag_to_tagbean
        tagbeanList=tag_to_tagbean(tags)
        #获取对另一半期望标签
        tagsForOther=UserTag.objects.get_tags_by_type(user_id=request.user.id,type=1)
        tagbeanForOtherList=tag_to_tagbean(tagsForOther)
        args['tagbeanForOtherList']=tagbeanForOtherList
        #获取权重
        from apps.recommend_app.method import get_weight_star
        args.update(get_weight_star(request.user.id))
        #获得另一半身高期望   
        userExpect=UserExpect.objects.get_user_expect_by_uid(request.user.id)
        if userExpect==None:
            args['grade_for_other']=False
        else:
            args['grade_for_other']=userExpect
        args['tagbeanList']=tagbeanList
        args['user_profile_form'] = UserProfileForm(instance=useBasicrProfile) 
        fields=['country','city','stateProvince','profileFinsihPercent','gender','age']
        for field in fields:
           args[field]=getattr(useBasicrProfile,field)
        args['gender_name']=useBasicrProfile.get_gender_display()
        
        #认证
        from apps.verification_app.views import verification
        args.update(verification(request))
        from pinloveweb.method import init_person_info_for_card_page
        args.update(init_person_info_for_card_page(useBasicrProfile))
        return render(request,'member/user_profile.html',args)
'''
修改个人信息
'''
@transaction.commit_on_success
def update_profile(request):
    if request.is_ajax():
        userProfile = UserProfile.objects.get(user_id=request.user.id)
        import copy
        oldUserProfile=copy.deepcopy(userProfile)
        POSTdata=request.POST.copy()
        #如果出生年月已经存在填充userProfileForm
        userProfileForm = UserProfileForm(POSTdata, instance=userProfile) 
        if userProfileForm.is_valid():
            #保存 user_profle信息
            userProfile = userProfileForm.save(commit=False)
            #计算资料完成度
            from apps.user_app.method import get_profile_finish_percent_and_score
            userProfile=get_profile_finish_percent_and_score(userProfile,oldUserProfile)
            userProfile.save(oldUserProfile=oldUserProfile)
            data={}
            #判断推荐条件是否完善
            from apps.recommend_app.recommend_util import cal_recommend
            cal_recommend(request.user.id,['info'])     
            data['result']='success'
        else:
            errors=userProfileForm.errors.items()
            data={'errors':errors,'result':'error'}
        json=simplejson.dumps(data)
        return HttpResponse(json, mimetype='application/json')
 

'''
修改密码

'''
#change_password
def change_password(request,tempate_name):
    args={}
    if request.method=="POST":
        changePasswordForm=ChangePasswordForm(request.POST)
        if changePasswordForm.is_valid():
            if not request.user.check_password(changePasswordForm.cleaned_data['oldpassword']):
                args['changePasswordForm']=changePasswordForm
                args['oldpasswordError']='旧密码不正确!'
            else:
                user=request.user
                user.set_password(changePasswordForm.cleaned_data['newpassword'])
                user.save()
                args={'change_result':True}
        else:
            args['changePasswordForm']=changePasswordForm
            errors=changePasswordForm.errors.items()
            for error in errors:
                args[error[0]+'Error']=error[1][0]
    else:
        changePasswordForm=ChangePasswordForm()
        args['changePasswordForm']=changePasswordForm
    return render(request,tempate_name,args)


#reset the password
def reset_password(request):
    args={}
    if request.REQUEST.get('username',False) and request.REQUEST.get('user_code',False):
      user_code=request.REQUEST.get('user_code')
      username=request.REQUEST.get('username')
      args={'user_code':user_code,'username':username}
      if Verification.objects.filter(verification_code=user_code).exists():
       if request.method=="POST":
        newpassword=request.POST.get('newpassword','')
        import re
        match=re.match(r'^[0-9a-zA-Z\xff_]{6,20}$',newpassword)
        if newpassword!=request.POST.get('repassword',''):
             args={'error_message':u'输入密码不相等!'}
             return render(request,'reset_password.html',args)
        elif  match is None :
            args={'error_message':u'密码个数错误!'}
            return render(request,'reset_password.html',args)
        
        Verification.objects.filter(verification_code=user_code).delete()
        user=User.objects.get(username=username)
        user.set_password(newpassword)
        args['reset_result']=True
        user.save()
        return render(request,'reset_password.html',args)
       else:
          return render(request,'reset_password.html',args)
      else:
            args={'error_message':u'该连接已过期或被使用!'}
    else:
        args={'error_message':u'该链接无效!'}
    return render(request,'error.html',args)

'''
更新黑名单
'''
@transaction.commit_on_success
def black_list(request):
    args={}
    try:
        userId=int(request.REQUEST.get('userId'))
        if userId==request.user.id:
            raise Exception('自己不能拉自己进黑名单!')
        from apps.user_app.method import update_black_list
        result=update_black_list(request.user.id,userId)
        if result==1:
            from util.cache import set_black_list_by_cache
            set_black_list_by_cache(request.user.id,userId)
            if Follow.objects.filter(my_id=request.user.id,follow_id=userId).exists():
                Follow.objects.filter(my_id=request.user.id,follow_id=userId).delete()
        elif result==-1:
            from util.cache import del_attribute_black_list_by_cache
            del_attribute_black_list_by_cache(request.user.id,userId)
        args={'result':'success','type':result}
    except Exception ,e:
        logger.exception('更新黑名单出错')
        args={'result':'error','error_message':'黑名单错误:'+e.message}
    json=simplejson.dumps(args)
    return HttpResponse(json)
        
#######################################################
#上面是改版页面
#######################################################


# update user basic information
def update_Basic_Profile_view(request): 
    
    if request.user.is_authenticated() :
        args = {}
        args.update(csrf(request))
        user = request.user
        if request.method == 'POST' :
            userProfile = UserProfile.objects.get(user_id=user.id)
            userProfileForm = UserBasicProfileForm(request.POST,  instance=userProfile) 
            if userProfileForm.is_valid() :
                stateProvince = request.POST['stateProvince']
                city = request.POST['city']
                country = request.POST['country']
                
#                 if request.FILES :
#                   # uppload image
#                   f = request.FILES["photo"] 
#                   parser = ImageFile.Parser()  
#                   for chunk in f.chunks():
#                     parser.feed(chunk)  
#                   img = parser.close()
#                   path = settings.MEDIA_ROOT
#                   img.save('jin', 'jpeg') 
                userProfile = userProfileForm.save(commit=False)
#                 print userProfile.avatar_name
                #get user id
                userProfile.id = UserProfile.objects.get(user_id=user.id).id
                userProfile.user = request.user
                userProfile.cal_age()
                userProfile.cal_sunSign()
                userProfile.cal_zodiac()
                userProfile.stateProvince = stateProvince;
                userProfile.city = city
                userProfile.country = country
                
                map=request.session['user_original_data']
                cal_recommend_user.send(sender=None,userProfile=userProfile,height=map.get('height'),
                                        education=map.get('education'),educationSchool=map.get('educationSchool'),income=map.get('income'))
                userProfile.save() 
                return HttpResponseRedirect('/user/update_profile_success/') 
            else:
                args['user_profile_form'] = userProfileForm 
    
        else : 
                useBasicrProfile = UserProfile.objects.get(user_id=request.user.id)
                args['user_profile_form'] = UserBasicProfileForm(instance=useBasicrProfile) 
                args['photo']=useBasicrProfile.avatar_name
                args['photo_status']=useBasicrProfile.avatar_name_status
                args['age']=useBasicrProfile.age
                args['sunSign']=useBasicrProfile.get_sunSign_display()
                args['zodiac']=useBasicrProfile.get_zodiac_display()
                args['country']=useBasicrProfile.country
                args['city']=useBasicrProfile.city
                args['stateProvince']=useBasicrProfile.stateProvince
                map={'height':useBasicrProfile.height,'education':useBasicrProfile.education,'educationSchool':useBasicrProfile.educationSchool,'income':useBasicrProfile.income}
                request.session['user_original_data']=map
        return render(request, 'member/update_Basic_Profile.html', args,)
    
    else : 
        
        args = {}
        args.update(csrf(request))
        return render(request, 'login.html', args) 
    
def update_profile_success(request): 
    return render(request, 'member/update_profile_success.html')

#修改个人联系信息
def user_contact_view(request):
     if request.user.is_authenticated() :
         args = {}
         args.update(csrf(request))
         count=UserContactLink.objects.filter(user_id=request.user.id).count()
         if request.method == 'POST' :
              userContactForm=UserContactForm(request.POST)
              if userContactForm.is_valid():
                  
                  userContact = userContactForm.save(commit=False)
                  if count !=0:
                       userContact.id=UserContactLink.objects.get(user_id=request.user.id).id
                  userContact.user=request.user
                  userContact=get_household_home(request,userContact)
                  userContact.save()
                  return render(request,'member/update_profile_success.html',args,)
                  
              else:
                   args['user_contact_form']=userContactForm
         else:
              userContactForm=UserContactForm()
              if count!=0:
                  userContact=UserContactLink.objects.get(user_id=request.user.id)
                  userContactForm=UserContactForm(instance=userContact)
                  args['userContact']=userContact
              args['user_contact_form']=userContactForm
         return render(request, 'member/user_contact.html', args,)
         
     else:
        args = {}
        args.update(csrf(request))
        return render(request, 'login.html', args) 
    
def get_household_home(request,userContact):
    stateProvinceHome = request.POST['stateProvinceHome']
    cityHome = request.POST['cityHome']
    CountryHome = request.POST['CountryHome']
    userContact.stateProvinceHome=stateProvinceHome
    userContact.cityHome=cityHome
    userContact.CountryHome=CountryHome
    userContact.userContact=userContact
    return userContact
    
#个人外貌
def user_appearance_view(request):
     if request.user.is_authenticated() :
         args = {}
         args.update(csrf(request))
         count=UserProfile.objects.filter(user_id=request.user.id).count()
         if request.method == 'POST' :
              userProfile = UserProfile.objects.get(user_id=request.user.id)
              userAppearanceForm=UserAppearanceForm(request.POST,instance=userProfile)
              if userAppearanceForm.is_valid:
                  userAppearance = userAppearanceForm.save(commit=False)
                  if count !=0:
                       userAppearance.id=UserProfile.objects.get(user_id=request.user.id).id
                  userAppearance.user=request.user
                  userAppearance.save()
                  return render(request,'member/update_profile_success.html',args,)
                  
              else:
                   args['user_appearance_form']=userAppearanceForm
         else:
              userAppearanceForm=UserAppearanceForm()
              if count!=0:
                  userAppearance=UserProfile.objects.get(user_id=request.user.id)
                  userAppearanceForm=UserAppearanceForm(instance=userAppearance)
              args['user_appearance_form']=userAppearanceForm
         return render(request, 'member/user_appearance.html', args,)
         
     else:
        args = {}
        args.update(csrf(request))
        return render(request, 'login.html', args) 

#学习工作    
def user_study_work_view(request):
     if request.user.is_authenticated() :
         args = {}
         args.update(csrf(request))
         count=UserProfile.objects.filter(user_id=request.user.id).count()
         if request.method == 'POST' :
              userProfile = UserProfile.objects.get(user_id=request.user.id)
              userStudyWorkForm=UserStudyWorkForm(request.POST,instance=userProfile)
              if userStudyWorkForm.is_valid:
                  userStudyWork = userStudyWorkForm.save(commit=False)
                  if count !=0:
                       userStudyWork.id=UserProfile.objects.get(user_id=request.user.id).id
                  userStudyWork.user=request.user
                  userStudyWork.save()
                  return render(request,'member/update_profile_success.html',args,)
                  
              else:
                   args['user_study_work_form']=userStudyWorkForm
         else:
              userStudyWorkForm=UserStudyWorkForm()
              if count!=0:
                  userStudyWork=UserProfile.objects.get(user_id=request.user.id)
                  userStudyWorkForm=UserStudyWorkForm(instance=userStudyWork)
              args['user_study_work_form']=userStudyWorkForm
         return render(request, 'member/study_work.html', args,)
         
     else:
        args = {}
        args.update(csrf(request))
        return render(request, 'login.html', args) 
    
    
#个人习惯
def personal_habit_view(request):
     if request.user.is_authenticated() :
         args = {}
         args.update(csrf(request))
         count=UserProfile.objects.filter(user_id=request.user.id).count()
         if request.method == 'POST' :
              userProfile = UserProfile.objects.get(user_id=request.user.id)
              userPersonalHabitForm=UserPersonalHabitForm(request.POST,instance=userProfile)
              if userPersonalHabitForm.is_valid:
                  userPersonalHabit = userPersonalHabitForm.save(commit=False)
                  if count !=0:
                       userPersonalHabit.id=UserProfile.objects.get(user_id=request.user.id).id
                  userPersonalHabit.user=request.user
                  userPersonalHabit.save()
                  return render(request,'member/update_profile_success.html',args,)
                  
              else:
                   args['personal_habit_form']=userPersonalHabitForm
         else:
              userPersonalHabitForm=UserPersonalHabitForm()
              if count!=0:
                  userPersonalHabit=UserProfile.objects.get(user_id=request.user.id)
                  userPersonalHabitForm=UserPersonalHabitForm(instance=userPersonalHabit)
              args['personal_habit_form']=userPersonalHabitForm
         return render(request, 'member/personal_habit.html', args,)
         
     else:
        args = {}
        args.update(csrf(request))
        return render(request, 'login.html', args) 
    
#家庭情况
def family_information_view(request):
     if request.user.is_authenticated() :
         args = {}
         args.update(csrf(request))
         count=UserProfile.objects.filter(user_id=request.user.id).count()
         if request.method == 'POST' :
              userProfile = UserProfile.objects.get(user_id=request.user.id)
              userFamilyInformationForm=UserFamilyInformationForm(request.POST,instance=userProfile)
              if userFamilyInformationForm.is_valid:
                  userFamilyInformation = userFamilyInformationForm.save(commit=False)
                  if count !=0:
                       userFamilyInformation.id=UserProfile.objects.get(user_id=request.user.id).id
                  userFamilyInformation.user=request.user
                  userFamilyInformation.save()
                  return render(request,'member/update_profile_success.html',args,)
                  
              else:
                   args['personal_habit_form']=userFamilyInformationForm
         else:
              userFamilyInformationForm=UserFamilyInformationForm()
              if count!=0:
                  userFamilyInformation=UserProfile.objects.get(user_id=request.user.id)
                  userFamilyInformationForm=UserFamilyInformationForm(instance=userFamilyInformation)
              args['user_family_information_form']=userFamilyInformationForm
         return render(request, 'member/family_information.html', args,)
         
     else:
        args = {}
        args.update(csrf(request))
        return render(request, 'login.html', args) 
    



# get userinfor
def userInfor(request, offset):
    if request.method == 'GET':
         try:
             offset = int(offset)
         except ValueError:
             raise Http404()
         userInfor = UserProfile.objects.get(user_id=offset)
         return render(request, 'member/userInfor.html', {'userInfor':userInfor})
    else:
         return render(request, 'search/search.html')





def friend(request):
    count = Follow.objects.filter(my_id=request.user.id).count()
    if count == 0:
        return render(request, 'member/friend.html', {'count':count})
    else :
        friendList = Follow.objects.filter(my_id=request.user.id)
        return render(request, 'member/friend.html', {'count':count, 'friendList':friendList})



# get userinfor
def removeFriend(request, offset):
    if request.method == 'GET':
         try:
             offset = int(offset)
         except ValueError:
             raise Http404()
         Follow.objects.filter(follow_id=offset).delete()
         return HttpResponseRedirect("/user/friend/")
    else:
         return HttpResponseRedirect("/user/friend/")

    


#commit the password
@csrf_protect
def commit_password(request):
    oldpassword = request.REQUEST.get('oldpassword','')
    newpassword = request.REQUEST.get('newpassword','')
    repassword = request.REQUEST.get('repassword','')
    if newpassword == repassword:
        if isIdAuthen(request): 
            user = User.objects.get(username=request.REQUEST.get('username',''))
        elif auth.authenticate(username=request.user.username, password=oldpassword) is not None :
            user = request.user
        else :
            return render(request, 'error.html') 
        user.set_password(newpassword)
        user.save()
        return render(request, 'success.html') 
    else :
        return render(request, 'error.html') 
    
def  isIdAuthen(request):  
    username = request.REQUEST.get('username','')
    user_code = request.REQUEST.get('user_code','')
    if username != '' :
        try :
            verification = Verification.objects.get(username=username)
            if verification.verification_code == user_code:
                verification.delete()
                return True
        except Exception:
            return False
    else :
        return False   
    


# def generate_verification(username) :
#     if Verification.objects.get(username=username) is not None :
#          user_code = random_str()
#          verification = Verification()
#          verification.username = username
#          verification.verification_code = user_code
#          verification.save()

#上传头像 
@login_required
def upload(request):
     return render_to_response(
         'member/upload.html',
        get_uploadavatar_context(),
         context_instance = RequestContext(request)
     )

def photo_check(request):
    arg={}
    if request.user.is_authenticated():
        if request.method=="POST":
            score=int(request.POST['score'])
            UserProfile.objects.filter(user_id=request.user.id).update(avatar_name_status='3')
            if Grade.objects.filter(user_id=request.user.id).exists():
                    Grade.objects.filter(user_id=request.user.id).update(appearancescore=score)
            else:
                    Grade.objects.create(user_id=request.user.id,appearancescore=score)
            #判断推荐条件是否完善
            from apps.recommend_app.recommend_util import cal_recommend
            cal_recommend(request.user.id,['userProfile','grade'])     
            return render(request,'member/update_profile_success.html',arg,)
        else:
             useBasicrProfile=UserProfile.objects.get(user_id=request.user.id)
             arg['photo']=useBasicrProfile.avatar_name
             arg['photo_status']=useBasicrProfile.get_avatar_name_status_display()
             return render(request,'member/photo_check.html',arg)
    else:
        return render(request,'login.html',arg)
    
'''
会员页面
'''
def member(request):
    return render(request,'member/member.html')

def become_member(request):
    UserProfile.objects.filter(user=request.user).update(member=1)
    return render(request,'member/member.html',{'result':'开通成功'})
def cancel_member(request):
    UserProfile.objects.filter(user=request.user).update(member=0)
    return render(request,'member/member.html',{'result2':'取消成功'})