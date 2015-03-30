# -*- coding: utf-8 -*-
'''
Created on Jul 4, 2013

@author: jin
'''
from django.shortcuts import render
from apps.user_app.models import UserProfile, Follow
from apps.search_app.forms import SearchForm
from util.page import page
from apps.pojo.search import SearchRsult
from django.http.response import HttpResponse
from django.utils import simplejson
from pinloveweb import STAFF_MEMBERS
import urllib
import logging
logger=logging.getLogger(__name__)
################################
##1.0
def search(request,template_name='simple_search.html'):
    args={}
    try:
        userProfile=UserProfile.objects.get_user_info(request.user.id)
        if request.method=='POST':
                searchForm=SearchForm(request.POST)
                if searchForm.is_valid():
                    userProfileList=searchForm.select_data(request.REQUEST.get('sunSign','').rstrip(),userProfile.gender,request.user.id)
                    searchList=get_recommend_list(request,userProfile,userProfileList)
                    args['result']='success'
        elif request.is_ajax():
            searchForm=SearchForm(request.GET)
            if searchForm.is_valid():
                userProfileList=searchForm.select_data(request.REQUEST.get('sunSign','').rstrip(),userProfile.gender,request.user.id)
                searchList=get_recommend_list(request,userProfile,userProfileList)
                args['result']='success'
        else:
            searchForm=SearchForm()
            searchForm.init_search_condition(request.user.id)
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
                args['error_message'].append([SearchForm.base_fields[error[0]].label,error[1][0]])
            json=simplejson.dumps(args)
            return HttpResponse(json)
    except Exception as e:
        error_message='搜索也卖弄出错：出错原因：'+e.message
        logger.exception(error_message)
        args['result']='success'
        args['error_message']=error_message
        template_name='error.html'
    if request.is_ajax():
            url=''
            if request.method=="POST":
                POSTcopy=request.POST.copy()
                POSTcopy.pop('csrfmiddlewaretoken')
                url=(request.path+'?'+urllib.urlencode(POSTcopy))
            from pinloveweb.method import load_cards_by_ajax
            return load_cards_by_ajax(request,searchList,url=url)
    else:
        return render(request,template_name,args)

################################
def get_recommend_list(request,userProfile,userProfileList,**kwargs):
    args=page(request,userProfileList)
    matchResultList=args['pages']
    from apps.pojo.card import userProfileList_to_CardList
    matchResultList.object_list=userProfileList_to_CardList(request.user.id,matchResultList.object_list)
    return matchResultList


'''
根据个人信息获得不可搜索条件
条件age,heigh,education,icome,jobIndustry,sunSign
attribute： 
     userProfile 用户详细信息
'''
def get_disable_condition(userProfile):
    args={}
    fields=['age','height','education','income','jobIndustry','sunSign']
    for field in fields:
        if getattr(userProfile,field) in [None,-1,'-1']:
            args['disable_'+field]=True
    return args
#########################################
#以上是1.0版本
#####################################
