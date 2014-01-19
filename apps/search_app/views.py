# -*- coding: utf-8 -*-
'''
Created on Jul 4, 2013

@author: jin
'''
from django.shortcuts import render_to_response, render
from apps.user_app.models import UserProfile, Follow
from django.contrib.flatpages.tests import csrf
from django.db import connection, transaction
from util.connection_db import connection_to_db
from apps.upload_avatar import app_settings
from apps.search_app.forms import AdvanceSearchForm
from util.page import page
from django.template import context
from django.db.models.query_utils import Q
from django.core.paginator import Paginator
from apps.pojo.search import SearchRsult

 
def simple_search(request):
     return render(request, 'search.html')

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
       avatar_name=searchRsult.avatar_name
       isFriend=False
       searchRsult=SearchRsult(userId,username,avatar_name,height,age,education,income,jobIndustry,isFriend)
       searchRsultList.append(searchRsult)
    return searchRsultList

def advance_search(request):
    arg={}
    arg['advance_search_form']=AdvanceSearchForm()
    return render(request,'advanced_search.html',arg)
def advance_search_result(request):
   if request.user.is_authenticated():
     if request.method == 'POST':
#        a_sex = request.POST['sex']
       minAge = request.POST['minAge']
       maxAge = request.POST['maxAge']
       maxHeight = request.POST['maxHeight']
       minHeight = request.POST['minHeight']
       if request.POST.get('image')!= None:
           image = ' and c2.avatar_name !="user_img/image.png" '
       else:
           image=' and c2.avatar_name ="user_img/image.png" '
       advanceSearchForm=AdvanceSearchForm(request.POST)
       if advanceSearchForm.is_valid() : 
            user_basic=UserProfile.objects.get(user_id=request.user.id)
            frends_flag = []  # 判断是否已经添加好友
            sql=advance_search_sql(str(request.user.id),minAge,maxAge,image,user_basic.gender,maxHeight,minHeight,
                             advanceSearchForm)
            searchRsultList=UserProfile.objects.raw(sql)
            request.session['advanceSearchSql']=sql 
            # 需要映射到field choices 的字段
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
            return render(request, 'advanced_search_result.html',arg)
     else:     
       arg={}
       searchRsultList=UserProfile.objects.raw(request.session['advanceSearchSql'])
       arg=page(request,searchRsultList) 
       searchRsultList=searchRsultBeanList_to_searchRsultList(arg.get('pages'))
       friends = Follow.objects.filter(my=request.user.id)
       i=0 
       for user in searchRsultList:
            for friend in friends:
                if user.user_id == friend.friend.id:
                   searchRsultList[i].isFriend=True
            i+=1
       arg['pages']=searchRsultList
       return render(request, 'advanced_search_result.html', arg)
   else:
        arg={}
        return render(request, 'login.html', arg)
def advance_search_sql(id,minAge,maxAge,image,gender,maxHeight,minHeight,advanceSearchFrom):
     sql='''select c1.id as id,c1.username as username,c2.age as age,c2.gender as gender,
       c2.education as education,c2.height,c2.income as income,c2.jobIndustry,c2.avatar_name
       from user_app_userprofile c2 
       LEFT JOIN auth_user c1 on c1.id=c2.user_id 
       where c1.id!='''+id+' and c2.age>='+minAge+' and c2.age<='+maxAge+image+' and c2.gender!='+"'"+gender+"'"\
       +' and c2.height>='+minHeight+' and c2.height<='+maxHeight
     education=advanceSearchFrom.cleaned_data['education']
     income=advanceSearchFrom.cleaned_data['income']
     sunSign=advanceSearchFrom.cleaned_data['sunSign']
     jobIndustry=advanceSearchFrom.cleaned_data['jobIndustry']
     companyType= advanceSearchFrom.cleaned_data['companyType']
     hasCar = advanceSearchFrom.cleaned_data['hasCar']
     hasHouse =  advanceSearchFrom.cleaned_data['hasHouse']
     isOnlyChild = advanceSearchFrom.cleaned_data['isOnlyChild']
     if not (education==None or education==-1):
         sql+=" and c2.education ="+str(education)
     if not (income==None or income==-1):
        sql+=" and c2.income >="+ str(income)
     if not (sunSign==None or sunSign==-1):
        sql+=" and c2.sunSign ="+ str(sunSign)
     if not (jobIndustry==None or jobIndustry==-1):
        sql+=" and c2.jobIndustry ="+ str(jobIndustry)
     if not (companyType==None or companyType=='N'):
        sql+=" and c2.companyType ="+ str(companyType)
     if not (hasCar==None or hasCar==0):
        sql+=" and c2.hasCar ="+ str(hasCar)
     if not (hasHouse==None or hasHouse==0):
        sql+=" and c2.hasHouse ="+ str(hasHouse)
     if not (isOnlyChild==None or isOnlyChild==0):
        sql+=" and c2.isOnlyChild ="+str(isOnlyChild)
     return sql
    
        
