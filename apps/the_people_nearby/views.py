# -*- coding: utf-8 -*-
import urllib2
from django.shortcuts import render
from apps.user_app.models import UserProfile
def GetIp(request):
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        return request.META['HTTP_X_FORWARDED_FOR']
    else:
        return request.META['REMOTE_ADDR']
    
def GetLocation(request):  
    try: 
        url = 'http://api.map.baidu.com/location/ip?ak=E1356a909570fb0e255f1f278dabd11b&ip='+GetIp(request)
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        return response.read().split('|')[2] #decode('raw_unicode_escape')
    except Exception, e:
        print e
        
def the_people_nearby(request):
    arg = {}
    arg['the_people_nearby'] =  UserProfile.objects.filter(lastLoginAddress=GetLocation(request))
#     arg['the_people_nearby']
#     for userprofile in userprofiles:
#         print userprofile.user.username
    return render(request, 'the_people_nearby.html',arg)    
