# -*- coding: utf-8 -*-
'''
Created on Aug 22, 2013

@author: jin
'''
from django.db import connection, transaction
def connection_to_db(sql,param=None,type=False):
    cursor=connection.cursor();
    if param==None:
        cursor.execute(sql)
    else:
        cursor.execute(sql,param)
    if type :
        desc = cursor.description 
        result=[dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]
        return result
    else:
        return cursor.fetchall()
#     desc=cursor.description
#     fields = [dict(zip([col[0] for col in desc], row))
#     for row in cursor.fetchall()]
#     for field in fields:
#        for i in field_mapping:
#             field[i[1]]=dict(i[0])[field[i[1]]]
   
def connection_to_db_commit(sql,param=None):
    cursor=connection.cursor();
    if param==None:
        cursor.execute(sql)
    else:
        cursor.execute(sql,param)
    transaction.commit_unless_managed()
  
    

