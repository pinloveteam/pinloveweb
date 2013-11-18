# -*- coding: utf-8 -*-
from django.shortcuts import render
from apps.user_app.models import UserProfile
import httplib
from xml.dom import minidom
def GetIp(request):
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        return request.META['HTTP_X_FORWARDED_FOR']
    else:
        return request.META['REMOTE_ADDR']
    
def GetLocation(request):  
    httpClient = None
    
    try:
        httpClient = httplib.HTTPConnection('192.151.154.154', 80, timeout=30)
        httpClient.request('GET', '/xml/'+GetIp(request))
    
        response = httpClient.getresponse()
        dom = minidom.parseString(response.read())      
        root = dom.firstChild      
        childs = root.childNodes    
        for child in childs:  
            if child.nodeName == 'City':
                return child.childNodes[0].data
    
    except Exception, e:
        print e
    finally:
        if httpClient:
            httpClient.close()
        
def the_people_nearby(request):
    arg = {}
    arg['the_people_nearby'] =  UserProfile.objects.filter(lastLoginAddress=GetLocation(request))
    return render(request, 'the_people_nearby.html',arg)    
