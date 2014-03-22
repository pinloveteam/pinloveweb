# -*- coding: utf-8 -*-
from django.shortcuts import render
from apps.user_app.models import UserProfile, Follow
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
    userProfile=UserProfile.objects.get_user_info(request.user.id)
    userProfileList =  UserProfile.objects.filter(lastLoginAddress=GetLocation(request)).exclude(user=request.user)
    #相互关注的人的id
    follows=Follow.objects.follow_each(request.user.id)
    focusEachOtherList=[follow.my.id for follow in follows ]
    #分页
    from util.page import page
    arg=page(request,userProfileList)
    userList=arg['pages']
    from apps.pojo.card import userProfileList_to_CardList
    userList.object_list=userProfileList_to_CardList(userList.object_list)
    from pinloveweb.method import is_focus_each_other
    userList=is_focus_each_other(request,userList,focusEachOtherList)
    if request.GET.get('ajax')=='true':
        from pinloveweb.method import load_cards_by_ajax
        return load_cards_by_ajax(request,userList)
    from apps.pojo.card import MyEncoder
    from django.utils import simplejson
    userList.object_list=simplejson.dumps(userList.object_list,cls=MyEncoder)
    arg['pages']=userList
    from pinloveweb.method import init_person_info_for_card_page
    arg.update(init_person_info_for_card_page(userProfile,followEachCount=len(focusEachOtherList)))
    return render(request, 'the_people_nearby.html',arg )
