# -*- coding: utf-8 -*-
'''
Created on Jul 4, 2013

@author: jin
'''
from django.shortcuts import render_to_response, render
from apps.user_app.models import user_basic_profile, Friend, user_study_work
from django.contrib.flatpages.tests import csrf
from django.db import connection, transaction
from util.connection_db import connection_to_db
 
def simple_search(request):
     return render(request, 'search.html')


def search_result(request):
    print request.method
    if request.method == 'POST':
       a_sex = request.POST['sex']
       minAge = request.POST['minAge']
       maxAge = request.POST['maxAge']
       if request.POST.get('image')!= None:
           image = 'and avatar_name is not null'
       else:
           image=''
       frends_flag = []  # 判断是否已经添加好友
       sql='''select c1.id,c1.username,c2.age,c2.gender,c2.height,c2.income,c3.jobIndustry,c4.avatar_name
       from user_app_user_basic_profile c2 
       LEFT JOIN auth_user c1 on c1.id=c2.user_id 
       LEFT JOIN user_app_user_study_work c3 on c1.id=c3.user_id  
       LEFT JOIN user_app_user c4 on c1.id=c4.user_id  
       where  c2.age>='''+minAge+' and c2.age<='+maxAge+image
       # 需要映射到field choices 的字段
       field_mapping=[[user_basic_profile.INCOME_CHOICES,'income'],[user_study_work.JOB_INDUSRY_CHOICE,'jobIndustry'],]
       searchRsultList=connection_to_db(sql,field_mapping)
#        searchRsultList =user_basic_profile.objects.raw(sql)
#        else:
#             userList = user_basic_profile.objects.filter(age__gte=minAge).filter(age__lte=maxAge).filter(gender=a_sex).exclude(user_id=request.user.id).filter(myPhoto__isnull=False)
       friends = Friend.objects.filter(myId=request.user.id)
       temp = 0    
       for user in searchRsultList:
           for friend in friends:
               if user.user_id == friend.friendId.id:
                   temp = 1;
           if temp == 1:
                frends_flag.append(1)
           else:
                 frends_flag.append(0)
           temp = 0
                
           
    return render(request, 'search_result.html', {'userList':searchRsultList, 'frends_flag':frends_flag, })

