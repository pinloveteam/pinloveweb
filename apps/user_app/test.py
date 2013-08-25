# coding: utf-8 
'''
Created on Jul 4, 2013

@author: jin
'''

import os
from django.db import connection
import MySQLdb
from apps.user_app.models import Friend, user_basic_profile
from pinloveweb.settings import UPLOAD_AVATAR_UPLOAD_ROOT
from PIL import ImageFile
from django.conf import settings
# db = MySQLdb.connect(user='root', db='django', passwd='jin521436', host='localhost')
cursor=connection.cursor();
sql='''select c1.id,c1.username,c2.age,c2.gender,c2.height,c2.income,c3.jobIndustry,c4.avatar_name
       from user_app_user_basic_profile c2 
       LEFT JOIN auth_user c1 on c1.id=c2.user_id 
       LEFT JOIN user_app_user_study_work c3 on c1.id=c3.user_id  
       LEFT JOIN user_app_user c4 on c1.id=c4.user_id  
       where  c2.age>=10 and c2.age<=100'''
cursor.execute(sql)
desc=cursor.description
fields =  [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]
print fields
for i in fields:
    i['income']=dict(user_basic_profile.INCOME_CHOICES)[i['income']]
    print i['income']
print fields
# row=cursor.fetchall()
# for r in row:
#      print dict(user_basic_profile.INCOME_CHOICES)[r[fields['income']]]

# userList = User_Profile.objects.filter(age__gte=21).filter(age__lte=28).filter(gender='M').exclude(user_id=1)
# friends = Friend.objects.filter(myId=1)
# frends_flag={}
# temp=0
# for user in userList:
#     for friend in friends:
#         if user.user_id == friend.friendId.id:
#             temp=1;
#     if temp==1:
#         user.append(1)
#     else:
#        user.append(1)
# print userList
# print frends_flag

print  dict(user_basic_profile.INCOME_CHOICES)[5]
