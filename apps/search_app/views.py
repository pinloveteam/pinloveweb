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
                    userProfileList=UserProfile.objects.select_related('user').filter(age__gte=minAge,age__lte=maxAge,education__gte=education,income__gte=minIcome,income__lte=maxIncome,
                                               height__gte=minHeigh,height__lte=maxHeigh,avatar_name_status='3',**searchSql).exclude(gender=userProfile.gender,user=request.user)
                    searchList=get_recommend_list(request,userProfile,userProfileList)
                    from pinloveweb.method import load_cards_by_ajax
                    return load_cards_by_ajax(request,searchList)
        
        else:
            userProfileList=UserProfile.objects.filter().exclude(user=request.user)
            searchList=get_recommend_list(request,userProfile,userProfileList)
            if request.GET.get('ajax')=='true':
                from pinloveweb.method import load_cards_by_ajax
                return load_cards_by_ajax(request,searchList)
            from apps.pojo.card import MyEncoder
            searchList.object_list=simplejson.dumps(searchList.object_list,cls=MyEncoder)
            args['pages']=searchList
            initial=init_search_condition(request.user.id)
            searchForm=SearchForm(initial=initial)
            args.update(get_disable_condition(userProfile))
            args['searchForm']=searchForm
            from apps.search_app.forms import SUN_SIGN_CHOOSICE
            args['sunSign']=SUN_SIGN_CHOOSICE
            return render(request, 'simple_search.html',args)
    except Exception as e:
        print e

################################
def get_recommend_list(request,userProfile,userProfileList,**kwargs):
    args=page(request,userProfileList)
    matchResultList=args['pages']
    from apps.pojo.card import userProfileList_to_CardList
    matchResultList.object_list=userProfileList_to_CardList(matchResultList.object_list)
    from pinloveweb.method import is_focus_each_other
    matchResultList=is_focus_each_other(request,matchResultList)
    return matchResultList
'''
简单搜索
根据 年龄，身高，学历，收入，所在地
   可能要删除
'''
def simple_search(request):
    args={}
    if request.method=='POST':
        searchForm=SearchForm(request.POST)
        if searchForm.is_valid():
            minAge=searchForm.cleaned_data['minAge']
            maxAge=searchForm.cleaned_data['maxAge']
            education=searchForm.cleaned_data['education']
            minIcome=searchForm.cleaned_data['minIcome']
            maxIncome=searchForm.cleaned_data['maxIncome']
            minHeigh=searchForm.cleaned_data['minHeigh']
            maxHeigh=searchForm.cleaned_data['maxHeigh']
            isAvatar=searchForm.cleaned_data['isAvatar']
            userProfile=UserProfile.objects.get(user=request.user)
            if isAvatar==True:
                userProfileList=UserProfile.objects.select_related('user').filter(age__gte=minAge,age__lte=maxAge,education__gte=education,income__gte=minIcome,income__lte=maxIncome,
                                               height__gte=minHeigh,height__lte=maxHeigh,avatar_name_status='3').exclude(gender=userProfile.gender)
            else:
                userProfileList=UserProfile.objects.select_related('user').filter(age__gte=minAge,age__lte=maxAge,education__gte=education,income__gte=minIcome,income__lte=maxIncome,
                                               height__gte=minHeigh,height__lte=maxHeigh,).exclude(gender=userProfile.gender)
            searchRsultList=searchRsultBeanList_to_searchRsultList(userProfileList)
            from apps.pojo.search import SearchRsultEncoder
            json=simplejson.dumps(searchRsultList,cls=SearchRsultEncoder)
        return HttpResponse(json, mimetype='application/json')
    else:
        initial=SearchForm(request.user.id)
        searchForm=SearchForm(initial=initial)
        args['searchForm']=searchForm
    return render(request, 'search.html',args)


# def advance_search(request):
#     args={}
#     if request.method=='POST':
#         advanceSearchForm=searchForm(request.POST)
#         if advanceSearchForm.is_valid():
#             searchSql={}
#             minAge=advanceSearchForm.cleaned_data['minAge']
#             maxAge=advanceSearchForm.cleaned_data['maxAge']
#             education=advanceSearchForm.cleaned_data['education']
#             minIcome=advanceSearchForm.cleaned_data['minIcome']
#             maxIncome=advanceSearchForm.cleaned_data['maxIncome']
#             minHeigh=advanceSearchForm.cleaned_data['minHeigh']
#             maxHeigh=advanceSearchForm.cleaned_data['maxHeigh']
#             isAvatar=advanceSearchForm.cleaned_data['isAvatar']
#             searchFields=['sunSign','jobIndustry','hasHouse','hasCar']
#             for field in searchFields:
#                 if advanceSearchForm.cleaned_data[field]!='None':
#                     searchSql[field]=advanceSearchForm.cleaned_data[field]
#             for field in ['stateProvince','country','city']:
#                 if not advanceSearchForm.cleaned_data[field] in [u'None',u'国家',u'省份、州',u'地级市、县']:
#                     searchSql[field]=advanceSearchForm.cleaned_data[field]
#             if isAvatar==True:
#                 searchSql['avatar_name_status']='3'
#             userProfile=UserProfile.objects.get(user=request.user)
#             userProfileList=UserProfile.objects.select_related('user').filter(age__gte=minAge,age__lte=maxAge,education__gte=education,income__gte=minIcome,income__lte=maxIncome,
#                                                height__gte=minHeigh,height__lte=maxHeigh,**searchSql).exclude(gender=userProfile.gender)
#             searchRsultList=searchRsultBeanList_to_searchRsultList(userProfileList)
#             from apps.pojo.search import SearchRsultEncoder
#             json=simplejson.dumps(searchRsultList,cls=SearchRsultEncoder)
#         return HttpResponse(json, mimetype='application/json')
#     else:
#         initial=init_search_condition(request.user.id)
#         advanceSearchForm=AdvanceSearchForm(initial=initial)
#         args['advanceSearchForm']=advanceSearchForm
#         return render(request,'advanced_search.html',args)

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
# def simple_search(request):
#      return render(request, 'search.html')

#简单搜索结果
def search_result(request):
  arg={}
  if request.user.is_authenticated():
    if request.method == 'POST':
#        a_sex = request.POST['sex']
       minAge = request.POST['minAge']
       maxAge = request.POST['maxAge']
       user_basic=UserProfile.objects.get(user_id=request.user.id)
       if request.POST.get('image')!= None:
           searchRsultList=UserProfile.objects.select_related().filter(age__gte=minAge).filter(age__lte=maxAge ).exclude(gender=user_basic.gender).exclude(avatar_name='user_img/image.png')
       else:
          searchRsultList=UserProfile.objects.select_related().filter(age__gte=minAge).filter(age__lte=maxAge ).exclude(gender=user_basic.gender)
       request.session['searchQuery']=searchRsultList
       arg=page(request,searchRsultList)  
       searchRsultList=arg.get('pages')
       searchRsultList.object_list=searchRsultBeanList_to_searchRsultList(searchRsultList.object_list)
       friends = Follow.objects.filter(my=request.user.id)
       i=0 
       for user in searchRsultList:
            for friend in friends:
                if user.user_id == friend.friend.id:
                   searchRsultList[i].isFriend=True
            i+=1
       arg['pages']=searchRsultList
       return render(request, 'search_result.html',arg)
    else:
       arg=page(request,request.session['searchQuery']) 
       searchRsultList=searchRsultBeanList_to_searchRsultList(arg.get('pages'))
       friends = Follow.objects.filter(my=request.user.id)
       i=0 
       for user in searchRsultList:
            for friend in friends:
                if user.user_id == friend.friend.id:
                   searchRsultList[i].isFriend=True
            i+=1
       arg['pages']=searchRsultList
       return render(request, 'search_result.html',arg) 
       
  else: 
       return render(request, 'login.html', arg,)           
#映射到django 对象
# def search_result_mapping_field(searchRsultList):
#     for i in searchRsultList:
#         if i['jobIndustry']!=None:
#             i['jobIndustry']=dict(UserProfile.JOB_INDUSRY_CHOICE)[i['jobIndustry']]
#         else :
#             i['jobIndustry']='未填'
#         i['income']=dict(UserProfile.INCOME_CHOICES)[i['income']]
#         i['education']=dict(UserProfile.EDUCATION_DEGREE_CHOICES)[i['education']]
#         if i['avatar_name']!=None:
#              i['avatar_name']='user_img/'+ i['avatar_name']+'-'+str(app_settings.UPLOAD_AVATAR_DEFAULT_SIZE)+'.jpeg'
#         else :
#             i['avatar_name']='user_img/image.png'
# #     print searchRsultList 
#     return searchRsultList

'''
 推荐结果querySet转换 searchRsultList
'''
def searchRsultBeanList_to_searchRsultList(searchRsultBeanList):
    searchRsultList=[]
    for searchRsult in searchRsultBeanList:
       userId=searchRsult.user_id
       username=searchRsult.user.username
       height=searchRsult.height
       age=searchRsult.age
       education=searchRsult.get_education_display()
       income=searchRsult.income
       jobIndustry=searchRsult.get_jobIndustry_display()
       if searchRsult.avatar_name_status=='3':
           avatar_name=searchRsult.avatar_name
       else:
           avatar_name='/media/user_img/image'
       sunSign=searchRsult.get_sunSign_display()
       hasHouse=searchRsult.get_hasHouse_display()
       hasCar=searchRsult.get_hasCar_display()
       stateProvince=searchRsult.stateProvince
       country=searchRsult.country
       city=searchRsult.city
       searchRsult=SearchRsult(userId,username,avatar_name,height,age,education,income,jobIndustry,sunSign,hasHouse,hasCar,stateProvince,country,city)
       searchRsultList.append(searchRsult)
    return searchRsultList


    
        
