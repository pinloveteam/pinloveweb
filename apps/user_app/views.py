# -*- coding: utf-8 -*-
'''
Created on Jul 4, 2013

@author: jin
'''
from pinloveweb import  settings
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response, render
from django.views.decorators.csrf import csrf_protect
from django.template.context import RequestContext
from django.core.mail import send_mail
import random, string
from apps.user_app.models import user_basic_profile,user_contact_link,user_verification,user_appearance,user_study_work,user_hobby_interest,user_personal_habit,user_family_information,user_family_life,Friend,\
    Verification
from apps.user_app.forms import UserBasicProfileForm, UserContactForm,UserAppearanceForm, UserStudyWorkForm, UserPersonalHabitForm,\
    UserFamilyInformationForm
from django.core.context_processors import csrf 
from django.http.response import HttpResponseRedirect
import time

import string
from django.contrib.auth.models import User
from django.utils import simplejson
from django.db import connection
from django.contrib.auth.decorators import login_required
from PIL import ImageFile
from apps.upload_avatar import get_uploadavatar_context
from django.contrib import auth
from apps.upload_avatar import app_settings




#######    user models       ############# 
# update user basic information
def update_Basic_Profile_view(request): 
    
    if request.user.is_authenticated() :
        
        args = {}
        args.update(csrf(request))
        user = request.user
        if request.method == 'POST' :
            userProfileForm = UserBasicProfileForm(request.POST, request.FILES) 
            if userProfileForm.is_valid() :
                stateProvince = request.POST['stateProvince']
                city = request.POST['city']
                country = request.POST['country']
            
                if request.FILES :
                  # uppload image
                  f = request.FILES["photo"] 
                  parser = ImageFile.Parser()  
                  for chunk in f.chunks():
                    parser.feed(chunk)  
                  img = parser.close()
                  path = settings.MEDIA_ROOT
                  img.save('jin', 'jpeg') 
                
                userProfile = userProfileForm.save(commit=False)
                #get user id
                userProfile.id = user_basic_profile.objects.get(user_id=user.id).id
                userProfile.user = request.user
                userProfile.cal_age()
                userProfile.cal_sunSign()
                userProfile.cal_zodiac()
                userProfile.stateProvince = stateProvince;
                userProfile.city = city
                userProfile.country = country
                
                userProfile.save() 
                return HttpResponseRedirect('/user/update_profile_success/') 
            else:
                args['user_profile_form'] = userProfileForm 
    
        else : 
                useBasicrProfile = user_basic_profile.objects.get(user_id=request.user.id)
                from apps.user_app.models import User
                count =User.objects.filter(user_id=request.user.id).count()
                if count>0:
                    userImage=User.objects.get(user_id=request.user.id)
                    args['userImage']=settings.MEDIA_URL+'user_img/'+userImage.get_avatar_name(app_settings.UPLOAD_AVATAR_DEFAULT_SIZE)
                else:
                    args['userImage']=settings.MEDIA_URL+'user_img/image.png'
                args['user_profile_form'] = UserBasicProfileForm(instance=useBasicrProfile) 
                args['useBasicrProfile']=useBasicrProfile
                
        
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
         count=user_contact_link.objects.filter(user_id=request.user.id).count()
         if request.method == 'POST' :
              userContactForm=UserContactForm(request.POST)
              if userContactForm.is_valid():
                  
                  userContact = userContactForm.save(commit=False)
                  if count !=0:
                       userContact.id=user_contact_link.objects.get(user_id=request.user.id).id
                  userContact.user=request.user
                  userContact=get_household_home(request,userContact)
                  userContact.save()
                  return render(request,'member/update_profile_success.html',args,)
                  
              else:
                   args['user_contact_form']=userContactForm
         else:
              userContactForm=UserContactForm()
              if count!=0:
                  userContact=user_contact_link.objects.get(user_id=request.user.id)
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
         count=user_appearance.objects.filter(user_id=request.user.id).count()
         if request.method == 'POST' :
              userAppearanceForm=UserAppearanceForm(request.POST)
              if userAppearanceForm.is_valid:
                  userAppearance = userAppearanceForm.save(commit=False)
                  if count !=0:
                       userAppearance.id=user_appearance.objects.get(user_id=request.user.id).id
                  userAppearance.user=request.user
                  userAppearance.save()
                  return render(request,'member/update_profile_success.html',args,)
                  
              else:
                   args['user_appearance_form']=userAppearanceForm
         else:
              userAppearanceForm=UserAppearanceForm()
              if count!=0:
                  userAppearance=user_appearance.objects.get(user_id=request.user.id)
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
         count=user_study_work.objects.filter(user_id=request.user.id).count()
         if request.method == 'POST' :
              userStudyWorkForm=UserStudyWorkForm(request.POST)
              if userStudyWorkForm.is_valid:
                  userStudyWork = userStudyWorkForm.save(commit=False)
                  if count !=0:
                       userStudyWork.id=user_study_work.objects.get(user_id=request.user.id).id
                  userStudyWork.user=request.user
                  userStudyWork.save()
                  return render(request,'member/update_profile_success.html',args,)
                  
              else:
                   args['user_study_work_form']=userStudyWorkForm
         else:
              userStudyWorkForm=UserStudyWorkForm()
              if count!=0:
                  userStudyWork=user_study_work.objects.get(user_id=request.user.id)
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
         count=user_personal_habit.objects.filter(user_id=request.user.id).count()
         if request.method == 'POST' :
              userPersonalHabitForm=UserPersonalHabitForm(request.POST)
              if userPersonalHabitForm.is_valid:
                  userPersonalHabit = userPersonalHabitForm.save(commit=False)
                  if count !=0:
                       userPersonalHabit.id=user_personal_habit.objects.get(user_id=request.user.id).id
                  userPersonalHabit.user=request.user
                  userPersonalHabit.save()
                  return render(request,'member/update_profile_success.html',args,)
                  
              else:
                   args['personal_habit_form']=userPersonalHabitForm
         else:
              userPersonalHabitForm=UserPersonalHabitForm()
              if count!=0:
                  userPersonalHabit=user_personal_habit.objects.get(user_id=request.user.id)
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
         count=user_family_information.objects.filter(user_id=request.user.id).count()
         if request.method == 'POST' :
              userFamilyInformationForm=UserFamilyInformationForm(request.POST)
              if userFamilyInformationForm.is_valid:
                  userFamilyInformation = userFamilyInformationForm.save(commit=False)
                  if count !=0:
                       userFamilyInformation.id=user_family_information.objects.get(user_id=request.user.id).id
                  userFamilyInformation.user=request.user
                  userFamilyInformation.save()
                  return render(request,'member/update_profile_success.html',args,)
                  
              else:
                   args['personal_habit_form']=userFamilyInformationForm
         else:
              userFamilyInformationForm=UserFamilyInformationForm()
              if count!=0:
                  userFamilyInformation=user_family_information.objects.get(user_id=request.user.id)
                  userFamilyInformationForm=UserFamilyInformationForm(instance=userFamilyInformation)
              args['user_family_information_form']=userFamilyInformationForm
         return render(request, 'member/family_information.html', args,)
         
     else:
        args = {}
        args.update(csrf(request))
        return render(request, 'login.html', args) 
    
#change_password
def change_password(request):
     if request.user.is_authenticated() :
         if request.method=="POST":
             password=request.POST['password1']
             user=request.user
             user.set_password(password)
             user.save()
             return render(request, 'member/change_password_success.html')
         else:
             return render(request, 'member/change_password.html')
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
         userInfor = user_basic_profile.objects.get(user_id=offset)
         return render(request, 'member/userInfor.html', {'userInfor':userInfor})
    else:
         return render(request, 'search/search.html')

#######    user models       ############# 


#######    search models       ############# 
def simple_search(request):
    return render(request, 'search/search.html')

@csrf_protect
def search_result(request):
    print request.method
    if request.method == 'POST':
       a_sex = request.POST['sex']
       minAge = int(request.POST['minAge'])
       maxAge = int(request.POST['maxAge'])
       if request.POST.get('image')!= None:
           image = int(request.POST.get('image'))
       else:
           image=0
       frends_flag = []  # 判断是否已经添加好友
       if image == 0:
           userList = user_basic_profile.objects.filter(age__gte=minAge).filter(age__lte=maxAge).filter(gender=a_sex).exclude(user_id=request.user.id)
       else:
            userList = user_basic_profile.objects.filter(age__gte=minAge).filter(age__lte=maxAge).filter(gender=a_sex).exclude(user_id=request.user.id).filter(myPhoto__isnull=False)
       friends = Friend.objects.filter(myId=request.user.id)
       temp = 0    
       for user in userList:
           for friend in friends:
               if user.user_id == friend.friendId.id:
                   temp = 1;
           if temp == 1:
                frends_flag.append(1)
           else:
                 frends_flag.append(0)
           temp = 0
                
           
    return render(request, 'search/search_result.html', {'userList':userList, 'frends_flag':frends_flag, })

#######     search models       ############# 

def addFriend(request):
     if request.user.is_authenticated() :
         offset = request.GET.get('userId')
         count = Friend.objects.filter(friendId=offset).count();
         if count == 0:
             Myfriend = User.objects.get(id=offset)
             friend = Friend()
             friend.myId = request.user
             friend.friendId = Myfriend
             friend.type = '0'
             friend.save()
             result = '添加成功'
         else:
             result = "已添加好友"
        
         json = simplejson.dumps(result)
         return HttpResponse(json)
     else:
           args = {}
           args.update(csrf(request))
           return render(request, 'login.html', args) 
       
def friend(request):
    count = Friend.objects.filter(myId=request.user.id).count()
    if count == 0:
        return render(request, 'member/friend.html', {'count':count})
    else :
        friendList = Friend.objects.filter(myId=request.user.id)
        return render(request, 'member/friend.html', {'count':count, 'friendList':friendList})



# get userinfor
def removeFriend(request, offset):
    if request.method == 'GET':
         try:
             offset = int(offset)
         except ValueError:
             raise Http404()
         Friend.objects.filter(friendId=offset).delete()
         return HttpResponseRedirect("/user/friend/")
    else:
         return HttpResponseRedirect("/user/friend/")

    
#forget the password
def forget_password(request):
     if request.method == 'POST':
         querystr = request.REQUEST.get('forget_account','')
         user = User()
         if request.REQUEST.get('forget_type','') == 'email':
            try :
               user = User.objects.get(email=querystr)
            except Exception:
                return render(request, 'error.html')
         elif request.REQUEST.get('forget_type','') == 'nickname':
             try :
               user = User.objects.get(username=querystr)
             except Exception:
                return render(request, 'error.html')
         else :
            return render(request, 'error.html') 
         #user verification
         user_code = random_str()
         verification = Verification()
         verification.username = user.username
         verification.verification_code = user_code
         verification.save()
            # we need to generate a random number as</font> the verification key 
            
            # user needs email verification 
         domain_name = u'http://www.pinpinlove.com/user/reset_password/'
         email_verification_link = domain_name + '?username=' + user.username + '&' + 'user_code=' + user_code
         email_message = u"请您点击下面这个链接修改密码："
         email_message += email_verification_link
#        send_mail(u'拼爱网，密码找回', email_message,'pinloveteam@pinpinlove.com', [user.email])     
         send_mail(u'拼爱网，密码找回', email_message,'pinloveteam@pinpinlove.com',[user.email]) 
         return render(request, 'success.html')  

#reset the password
def reset_password(request):
    if request.REQUEST.get('username','') != '' and request.REQUEST.get('user_code','') != '':
        return render_to_response('reset_password.html',{'username':request.REQUEST.get('username',''),'user_code':request.REQUEST.get('user_code','')}, RequestContext(request) )
    else :
        return render(request, 'error.html')


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
    
def random_str(randomlength=32):
    a = list(string.ascii_letters)
    random.shuffle(a)
    return ''.join(a[:randomlength])

def alter_password(request) : 
    return render(request, 'alter_password.html',{'username': request.user.username})   

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
