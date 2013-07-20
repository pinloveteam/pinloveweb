# coding: utf-8 
'''
Created on Jul 4, 2013

@author: jin
'''
from pinloveweb import  settings
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response, render
from django.views.decorators.csrf import csrf_protect
from django.template.context import RequestContext
from apps.user_app.models import User_Profile,Friend
from apps.user_app.forms import UserProfileForm
from django.core.context_processors import csrf 
from django.http.response import HttpResponseRedirect
import time
import string
from PIL import ImageFile
from django.contrib.auth.models import User
from django.utils import simplejson
from django.db import connection

#######    user models       ############# 
# update user information
def update_profile(request): 
    
    if request.user.is_authenticated() :
        
        args = {}
        args.update(csrf(request))
        user = request.user
        count=User_Profile.objects.filter(user_id=user.id).count()
        if request.method == 'POST' : 

            userProfileForm = UserProfileForm(request.POST,request.FILES) 
            stateProvince = request.POST['stateProvince']
            city = request.POST['city']
            country = request.POST['country']
            if userProfileForm.is_valid() :
                #uppload image
                f = request.FILES["myPhoto"] 
                parser = ImageFile.Parser()  
                for chunk in f.chunks():
                    parser.feed(chunk)  
                img = parser.close()
                path=settings.MEDIA_ROOT
                img.save('jin','jpeg') 
                
                userProfile = userProfileForm.save(commit=False)
                if count!=0:
                    userProfile_id=User_Profile.objects.get(user_id=user.id).id
                    userProfile.id=userProfile_id
                userProfile.user = request.user
                current_year=time.strftime('%Y',time.localtime(time.time()))
                userProfile.age= string.atoi(current_year)-userProfile.year_of_birth
                userProfile.stateProvince=stateProvince;
                userProfile.city=city
                userProfile.country=country
                
                userProfile.save() 
                return HttpResponseRedirect('/user/update_profile_success/') 
            else : 
                args['user_profile_form'] = userProfileForm 
    
        else : 
            if count!=0:
                userProfile=User_Profile.objects.get(user_id=user.id)
                args['user_profile_form'] = UserProfileForm(instance =userProfile) 
                args['country']=userProfile.country
                args['city']=userProfile.city
                args['stateProvince']=userProfile.stateProvince
            else :
                args['user_profile_form'] =UserProfileForm()
        
        return render(request, 'member/update_profile.html', args)
    
    else : 
        
        args = {}
        args.update(csrf(request))
        return render(request, 'login.html', args) 
    
def update_profile_success(request): 
    return render(request, 'member/update_profile_success.html')

#get userinfor
def userInfor(request,offset):
    if request.method== 'GET':
         try:
             offset = int(offset)
         except ValueError:
             raise Http404()
         userInfor=User_Profile.objects.get(user_id=offset)
         return render(request, 'member/userInfor.html',{'userInfor':userInfor})
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
       cursor = connection.cursor()
       if maxAge == 0:
           userList = User_Profile.objects.filter(age__gte=minAge).filter(gender=a_sex).exclude(user_id=request.user.id)
       else:
            userList = User_Profile.objects.filter(age__gte=minAge).filter(age__lte=maxAge).filter(gender=a_sex).exclude(user_id=request.user.id)
            friends = Friend.objects.filter(myId=request.user.id)
            frends_flag=[]
           
    return render(request,'search/search_result.html',{'userList':userList})

#######     search models       ############# 

def addFriend(request):
     if request.user.is_authenticated() :
         offset=request.GET.get('userId')
         count=Friend.objects.filter(friendId=offset).count();
         if count==0:
             Myfriend=User.objects.get(id=offset)
             friend=Friend()
             friend.myId=request.user
             friend.friendId=Myfriend
             friend.type='0'
             friend.save()
             result ='添加成功'
         else:
             result="已添加好友"
        
         json=simplejson.dumps(result)
         return HttpResponse( json )
     else:
           args = {}
           args.update(csrf(request))
           return render(request, 'login.html', args) 
       
def friend(request):
    count=Friend.objects.filter(myId=request.user.id).count()
    if count==0:
        return render(request, 'member/friend.html', {'count':count})
    else :
        friendList=Friend.objects.filter(myId=request.user.id)
        return render(request, 'member/friend.html', {'count':count,'friendList':friendList})



#get userinfor
def removeFriend(request,offset):
    if request.method== 'GET':
         try:
             offset = int(offset)
         except ValueError:
             raise Http404()
         Friend.objects.filter(friendId=offset).delete()
         return HttpResponseRedirect("/user/friend/")
    else:
         return HttpResponseRedirect("/user/friend/")