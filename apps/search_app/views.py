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
################################
##1.0
def search(request):
    args={}
    try:
        userProfile=UserProfile.objects.get_user_info(request.user.id)
        if request.method=='POST':
                searchForm=SearchForm(request.POST)
                if searchForm.is_valid():
                    searchSql={}
                    minAge=searchForm.cleaned_data['minAge'] if searchForm.cleaned_data['minAge']!=u'' else 0
                    maxAge=searchForm.cleaned_data['maxAge'] if searchForm.cleaned_data['maxAge']!=u'' else 10000
                    education=searchForm.cleaned_data['education'] if searchForm.cleaned_data['education'] !=u'' else -1
                    minIcome=searchForm.cleaned_data['minIcome'] if searchForm.cleaned_data['minIcome']!=u'' else 0
                    maxIncome=searchForm.cleaned_data['maxIncome'] if searchForm.cleaned_data['maxIncome'] !=u'' else 100000 
                    #最大收入为不限
                    if maxIncome=='-1':
                        maxIncome='100000'
                    minHeigh=searchForm.cleaned_data['minHeigh'] if searchForm.cleaned_data['minHeigh']!=u'' else 0
                    maxHeigh=searchForm.cleaned_data['maxHeigh'] if searchForm.cleaned_data['maxHeigh']!=u'' else 1000
                    sunSign=request.REQUEST.get('sunSign','').rstrip()
                    if len(sunSign)>0:
                        sunSign=[int(sunSignBean)for sunSignBean in sunSign.split(',')]
                        searchSql['sunSign__in']=sunSign
                    jobIndustry=searchForm.cleaned_data['jobIndustry']
                    if jobIndustry!='None' and jobIndustry!=u'':
                        searchSql['jobIndustry']=jobIndustry
                    if education=='0':
                        searchSql['education']=education
                    userProfileList=UserProfile.objects.select_related('user').filter(age__gte=minAge,age__lte=maxAge,education__gte=education,income__gte=minIcome,income__lte=maxIncome,
                                               height__gte=minHeigh,height__lte=maxHeigh,**searchSql).exclude(gender=userProfile.gender).exclude(user=request.user).filter(avatar_name_status='3').exclude(user_id__in=STAFF_MEMBERS)
                    searchList=get_recommend_list(request,userProfile,userProfileList)
        
        else:
            userProfileList=UserProfile.objects.filter().exclude(user=request.user).exclude(gender=userProfile.gender).filter(avatar_name_status='3').exclude(user_id__in=STAFF_MEMBERS)
            searchList=get_recommend_list(request,userProfile,userProfileList)
            from apps.pojo.card import MyEncoder
            searchList.object_list=simplejson.dumps(searchList.object_list,cls=MyEncoder)
            args['pages']=searchList
            initial=init_search_condition(request.user.id)
            searchForm=SearchForm(initial=initial)
            args.update(get_disable_condition(userProfile))
            args['searchForm']=searchForm
            from apps.search_app.forms import SUN_SIGN_CHOOSICE
            args['sunSign']=SUN_SIGN_CHOOSICE
            from pinloveweb.method import get_no_read_web_count
            args.update(get_no_read_web_count(request.user.id,fromPage=u'card'))
        if request.is_ajax():
            from pinloveweb.method import load_cards_by_ajax
            return load_cards_by_ajax(request,searchList)
        else:
            return render(request, 'simple_search.html',args)
    except Exception as e:
        print e

################################
def get_recommend_list(request,userProfile,userProfileList,**kwargs):
    args=page(request,userProfileList)
    matchResultList=args['pages']
    from apps.pojo.card import userProfileList_to_CardList
    matchResultList.object_list=userProfileList_to_CardList(request.user.id,matchResultList.object_list)
    return matchResultList

'''
初始化搜索条件
attribute：
   user_id 用户id
 
'''
def init_search_condition(user_id):
    initial={}
    userProfile=UserProfile.objects.get(user_id=user_id)
    initial['isAvatar']=True
    initial['maxIncome']=-1
    initial['minIcome']=-1
    initial['jobIndustry']=None
    if userProfile.height==None:
        initial['minHeigh']=155
        initial['maxHeigh']=195
    if userProfile.age==None:
        initial['minAge']=18
        initial['maxAge']=30
    initial['education']=-1
    if userProfile.gender=='F':
        if userProfile.height!=None:
            initial['minHeigh']=userProfile.height
            max=userProfile.height+30
            if max>226:
                initial['maxHeigh']=226
            else:
                initial['maxHeigh']=int(max)
        if userProfile.age!=None:
            initial['minAge']=int(userProfile.age)
            initial['maxAge']=int(userProfile.age+10)
    else:
        if userProfile.height!=None:
            initial['minHeigh']=int(userProfile.height-25)
            initial['maxHeigh']=int(userProfile.height)
        if userProfile.age!=None:
            initial['minAge']=int(userProfile.age-10)
            initial['maxAge']=int(userProfile.age)
    return initial

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
