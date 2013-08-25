# -*- coding: utf-8 -*-
'''
Created on Aug 22, 2013

@author: jin
'''
from django.db import connection
from apps.user_app.models import user_basic_profile, user_contact_link,\
    user_appearance, user_study_work, user_hobby_interest,\
    user_family_information, user_personal_habit, user_family_life
def connection_to_db(sql,field_mapping):
    cursor=connection.cursor();
#     sql='''select c1.username,c2.trueName,c2.myPhoto,c2.age,
#     from user_app_user_profile c2 LEFT JOIN auth_user c1 on c1.id=c2.user_id LEFT JOIN user_app_friend c3 on c1.id=c3.myId_id  where  c2.gender='M' and
#     c1.id!=1 and  c2.age between 21 and 28 '''
    cursor.execute(sql)
    desc=cursor.description
    fields = [dict(zip([col[0] for col in desc], row))
     for row in cursor.fetchall()]
    for field in fields:
        for i in field_mapping:
            field[i[1]]=dict(i[0])[field[i[1]]]
   
    return  field
    

