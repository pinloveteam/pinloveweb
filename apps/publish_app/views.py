# -*- coding: utf-8 -*-
'''
Created on Sep 8, 2013

@author: jin
'''
from apps.publish_app.models import Publish
from util.page import page
from django.shortcuts import render
from django.http.response import Http404, HttpResponse
from PIL import ImageFile
from pinloveweb import settings

def list(request):
     arg={}
     if request.user.is_authenticated():
         publishList=Publish.objects.all()
         arg=page(request,publishList)
         return render(request,'publish_list.html',arg)
     else:
          return render(request, 'login.html', arg,) 
def publish(request,offset):
     arg={}
     if request.user.is_authenticated():
         try:
             offset = int(offset)
         except ValueError:
            raise Http404()
         publish=Publish.objects.get(id=offset)
         arg["publish"]=publish
         return render(request,'publish.html',arg)
     else:
          return render(request, 'login.html', arg,) 
      
      
      
      
      
"""#############admin#################"""
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def upload_image(request, encoding='utf-8'): 
    if request.method == 'POST': 
        if "upload_file" in request.FILES: 
            f = request.FILES["upload_file"] 
            parser = ImageFile.Parser()  
            for chunk in f.chunks():
                  parser.feed(chunk)  
            img = parser.close()
            path = settings.MEDIA_ROOT
            from util import util_settings
            name = '%s%s' % (util_settings.PUBLIC_IMAGE_UPLOAD_PATH,f.name)
            img.save(name)    
            return HttpResponse('%s/%s' % ("/media/publish_img/",f.name))
    return HttpResponse(u"Some error!Upload faild!格式：jpeg") 
    
    
def test(request):
     return render(request, 'test.html', ) 