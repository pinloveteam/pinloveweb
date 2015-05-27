# -*- coding: utf-8 -*-
'''
Created on 2014年4月22日

@author: jin
'''
from apps.recommend_app.models import MatchResult, NotRecommendUser, WeightStar,\
    Grade
import logging
from apps.recommend_app.form import StartForm

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
#     cursor.close()
    from apps.pojo.recommend import RecommendResult
    matchResult=RecommendResult(kwargs=result)
    return matchResult


#============================
#获得匹配结果
#attribute：
#     userId
#     otherId  ：被匹配的人
#============================
def get_matchresult(userId,otherId):
    try:
            matchResult=get_match_score_other(userId,otherId)
            if matchResult is None:
                matchResult=match_score(userId,otherId)
            else:
                from apps.pojo.recommend import MarchResult_to_RecommendResult
                matchResult=MarchResult_to_RecommendResult(matchResult)
            return matchResult
    except Exception as e:
        logging.error('获得匹配结果get_matchresult:出现错误!'+e)
'''
更新不喜欢
myId  用户id
otherId 不喜欢用户id

'''
def update_no_recommend_update_black_list(myId,otherId):  
    if not NotRecommendUser.objects.filter(my_id=myId,other_id=otherId).exists():
        NotRecommendUser(my_id=myId,other_id=otherId).save()
        return 1
    else:
        NotRecommendUser.objects.filter(my_id=myId,other_id=otherId).delete()
        return -1 
    
'''
根据用户名获取不推荐用户列表
@param userId:用户id
@return:  NotRecommendUser[NotRecommendUserList] 不推荐用户列表
   
'''
def get_no_recommend_list(userId):
    return [int(user.other_id) for user in NotRecommendUser.objects.filter(my_id=userId)]


