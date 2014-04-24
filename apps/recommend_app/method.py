# -*- coding: utf-8 -*-
'''
Created on 2014年4月22日

@author: jin
'''
from apps.recommend_app.models import MatchResult
'''
获取另一半对你打分的结果
'''
def get_score_my(userId,otherUserId):
    try:
        matchResult=MatchResult.objects.get(my_id=userId,other_id=otherUserId)
        return matchResult.scoreMyself
    except Exception as e:
        raise Exception('%s%s' %('获取另一半对你打分的结果出错,出错原因:',e))
 

'''
获取你对另一半的打分，如果没有返回None
attridute:
    my_id=userId  查询人id
    other_id=otherUserId  被查询人id
'''
def get_match_score_other(userId,otherUserId):   
    try:
        if MatchResult.objects.filter(my_id=userId,other_id=otherUserId).exists():
            return MatchResult.objects.get(my_id=userId,other_id=otherUserId)
        else:
            return None
    except Exception as e:
        raise Exception('%s%s' %('获取你对另一半的打分,出错原因:',e))
    
    
def match_score(userId,otherUserId):
#     from django.conf import settings
#     connection = MySQLdb.connect(user=settings.DATABASES['default']['USER'],
#                                           db=settings.DATABASES['default']['NAME'], passwd=settings.DATABASES['default']['PASSWORD'], host=settings.DATABASES['default']['HOST'])
    from django.db import connection
    cursor=connection.cursor();
#     cursor.callproc('recommend_for_one',[userId,otherUserId])
    cursor.execute("call recommend_for_one(%s,%s)",[userId,otherUserId]) 
#     cursor.execute("SELECT @_recommend_for_one")
#     connection.commit()
    desc = cursor.description 
    result=[dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()][0]
    cursor.close()
    from apps.pojo.recommend import RecommendResult
    matchResult=RecommendResult(kwargs=result)
    return matchResult

def set_recommend_result_in_session(request,matchResult):
    if not 'matchResultDict' in request.session.keys():
        request.session['matchResultDict']={}
    else:
        matchResultDict=request.session['matchResultDict']
        if not matchResult.userId in matchResultDict.keys():
            matchResultDict[matchResult.userId]=matchResult
        request.session['matchResultDict']=matchResultDict
        
def get_recommend_result_in_session(request,userId):
    if not 'matchResultDict' in request.session.keys():
        return None
    else:
        matchResultDict=request.session['matchResultDict']
        return matchResultDict.get(userId,None)