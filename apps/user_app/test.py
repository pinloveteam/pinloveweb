# coding: utf-8 
'''
Created on Jul 4, 2013

@author: jin
'''

import os
from django.db import connection
import MySQLdb
from apps.user_app.models import Friend, UserProfile
from pinloveweb.settings import UPLOAD_AVATAR_UPLOAD_ROOT
from PIL import ImageFile
from django.conf import settings
from apps.upload_avatar import app_settings
import re
from django.contrib.auth.models import User
# db = MySQLdb.connect(user='root', db='django', passwd='jin521436', host='localhost')
# cursor=connection.cursor();
# sql='''select c1.id,c1.username,c2.age,c2.gender,c2.height,c2.income,c3.jobIndustry,c4.avatar_name
#        from user_app_user_basic_profile c2 
#        LEFT JOIN auth_user c1 on c1.id=c2.user_id 
#        LEFT JOIN user_app_user_study_work c3 on c1.id=c3.user_id  
#        LEFT JOIN user_app_user c4 on c1.id=c4.user_id  
#        where  c2.age>=10 and c2.age<=100'''
# cursor.execute(sql)
# desc=cursor.description
# fields =  [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]
# print fields
# for i in fields:
#     if i['jobIndustry']!=None:
#         i['jobIndustry']=dict(user_study_work.JOB_INDUSRY_CHOICE)[i['jobIndustry']]
#     else :
#          i['jobIndustry']='未填'
#     print i['jobIndustry']
#     if i['avatar_name']!=None:
#         i['avatar_name']='user_img/'+ i['avatar_name']+'-'+str(app_settings.UPLOAD_AVATAR_DEFAULT_SIZE)
#     else :
#          i['avatar_name']='未填'
# print fields
# row=cursor.fetchall()
# for r in row:
#      print dict(user_basic_profile.INCOME_CHOICES)[r[fields['income']]]

# userList = User_Profile.objects.filter(age__gte=21).filter(age__lte=28).filter(gender='M').exclude(user_id=1)
# friends = Friend.objects.filter(my=1)
# frends_flag={}
# temp=0
# for user in userList:
#     for friend in friends:
#         if user.user_id == friend.friend.id:
#             temp=1;
#     if temp==1:
#         user.append(1)
#     else:
#        user.append(1)
# print userList
# print frends_flag ((P|S)\.\d{7})|((G|S)\d{8})|(1(4|5)\d{7})
# ereg=re.compile('^..\d{5,7}$')
# print re.match(ereg,'P.1111111')
# sql= "%s%d%s%d%s" %("select * from user_app_friend where friend_id=",1," and my_id in (SELECT friend_id from user_app_friend where my_id=",1,")")
# fllowList=Friend.objects.raw(sql)
# for follow in fllowList:
#     print follow.my.id
# UserProfile.objects.filter(user_id=2).update(lastLoginAddress='本机地址')
# u=UserProfile.objects.get(user_id=2)
# print u.lastLoginAddress
# user=UserProfile.objects.select_related().get(QQopenId='61C5FF21E0D49DD32BBF4E6571B536E3').user
# User(username='sdsd',password="None").save()
print User.objects.get(username='sdsd').password

