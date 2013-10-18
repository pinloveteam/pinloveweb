# -*- coding: utf-8 -*-
'''
Created on Aug 22, 2013

@author: jin
'''
from django.db import connection
from apps.user_app.models import UserProfile, user_hobby_interest
def connection_to_db(sql):
    cursor=connection.cursor();
    cursor.execute(sql)
    desc=cursor.description
    fields = [dict(zip([col[0] for col in desc], row))
    for row in cursor.fetchall()]
#     for field in fields:
#        for i in field_mapping:
#             field[i[1]]=dict(i[0])[field[i[1]]]
   
    return  fields
    

