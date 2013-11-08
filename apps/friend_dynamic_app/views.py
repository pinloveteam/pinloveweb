# -*-coding: utf-8 -*-
'''
Created on Nov 5, 2013

@author: jin
'''
from django.shortcuts import render
from apps.friend_dynamic_app.models import FriendDynamic, Picture
from pinloveweb import settings
from PIL import ImageFile 
from django.http.response import HttpResponseRedirect, HttpResponse
import time
import simplejson
from apps.user_app.models import UserProfile
def send_dynamic(request):
    arg={}
    if request.user.is_authenticated():
        if request.method=="POST":
            flag=True
            type=request.POST.get('type').strip()
            content=request.POST.get('content').strip()
            #判断失败条件
            if int(type)>=3:
                arg['error']={'error':u'发布失败！'}
                flag=False
            if content.rstrip()=='':
                arg['error']={'error':u'发布内容不能为空！'}
                flag=False
            friendDynamic=FriendDynamic()
            friendDynamic.publishUser=request.user
            friendDynamic.type=type
            friendDynamic.content=content
            if type=='2':
                friendDynamic.data=request.session['images_path']
            friendDynamic.save()
            if type=='2':
                photoList=simplejson.loads(request.session['images_path'])
                for photo in photoList:
                    picture=Picture()
                    picture.user=request.user
                    picture.friendDynamic=friendDynamic
                    picture.description=content
                    from util import util_settings
                    picture.picPath='%s%s' % (util_settings.RELATRVE_IMAGE_UPLOAD_PATH_M,photo)
                    picture.save()
                del request.session['images_path']
            if flag:
                return render(request, 'send_dynamic.html', arg,)
            else:
                return render(request, 'send_dynamic.html', arg,)
        else:
            friendDynamicList=FriendDynamic.objects.filter(publishUser=request.user)
            for friendDynamic in friendDynamicList:
                if friendDynamic.type==2:
                    friendDynamic.data=simplejson.loads(friendDynamic.data)
                    print friendDynamic.data
            arg['friendDynamicList']=friendDynamicList
            return render(request, 'send_dynamic.html', arg,)      
    else:
        return render(request, 'login.html', arg,)   
def dynamic_list(request):
    arg={}
    if request.user.is_authenticated():
        friendDynamicList=FriendDynamic.objects.filter(publishUser=request.user)
    else:
        return render(request, 'login.html', arg,)   
def update_photo(request): 
    if request.method == 'POST':
      if request.FILES :
        # uppload image
        f = request.FILES["file"]
        parser = ImageFile.Parser()  
        for chunk in f.chunks():
            parser.feed(chunk)  
        img = parser.close()
        from util.common_util import random_str
        from util import util_settings
        pictureName='%s%s%s%s%s' % (request.user.id,'_',time.strftime('%Y%m%d',time.localtime(time.time())),random_str(randomlength=10),f.name[f.name.find('.'):])
        if 'images_path' in request.session.keys():
            list=simplejson.loads(request.session['images_path'])
            list.append(pictureName)
            request.session['images_path']=simplejson.dumps(list)
        else:
            request.session['images_path']=simplejson.dumps([pictureName,])
        name = '%s%s' % (util_settings.IMAGE_UPLOAD_PATH_M,pictureName)
        img.save(name) 
        return HttpResponseRedirect('/dynamic/send/')
#     return render(request, 'test111.html',)   
def update_video(request): 
    arg={}
    if request.user.is_authenticated():
        if request.method == 'POST':
            if request.FILES :
                f = request.FILES["file"]
    else:
        return HttpResponse("请先登录")
    