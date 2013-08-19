# coding: utf-8 
'''
Created on Jul 4, 2013

@author: jin
'''

import os
from django.db import connection
import MySQLdb
from apps.user_app.models import Friend
from pinloveweb.settings import UPLOAD_AVATAR_UPLOAD_ROOT
from PIL import ImageFile
from django.conf import settings
# db = MySQLdb.connect(user='root', db='django', passwd='jin521436', host='localhost')
cursor=connection.cursor();
# sql='''select c1.username,c2.trueName,c2.myPhoto,c2.age,
# from user_app_user_profile c2 LEFT JOIN auth_user c1 on c1.id=c2.user_id LEFT JOIN user_app_friend c3 on c1.id=c3.myId_id  where  c2.gender='M' and
# c1.id!=1 and  c2.age between 21 and 28 '''
# cursor.execute(sql)



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

print settings.STATICFILES_DIRS
print settings.STATIC_ROOT