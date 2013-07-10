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
from apps.user_app.models import User_Profile 
from apps.user_app.forms import UserProfileForm
from django.core.context_processors import csrf 
from django.http.response import HttpResponseRedirect
import time
import string
from PIL import ImageFile

#######    user models       ############# 
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
            streetAddress = request.POST['streetAddress']
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
                userProfile.streetAddress=streetAddress
                
                userProfile.save() 
                return HttpResponseRedirect('/user/update_profile_success/') 
            else : 
                args['user_profile_form'] = userProfileForm 
    
        else : 
            if count!=0:
                userProfile=User_Profile.objects.get(user_id=user.id)
                args['user_profile_form'] = UserProfileForm(instance =userProfile) 
            else :
                args['user_profile_form'] =UserProfileForm()
        
        return render(request, 'member/update_profile.html', args)
    
    else : 
        
        args = {}
        args.update(csrf(request))
        return render(request, 'login.html', args) 
    
def update_profile_success(request): 
    return render(request, 'member/update_profile_success.html')
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
       if maxAge == 0:
           userList = User_Profile.objects.filter(age__gte=minAge).filter(gender=a_sex)
       else:
           userList = User_Profile.objects.filter(age__gte=minAge).filter(age__lte=maxAge).filter(gender=a_sex)
       if userList:
             flag=True
    return render_to_response('search/search_Result.html',{'userList':userList,'flag':flag},context_instance=RequestContext(request))

#######     search models       ############# 