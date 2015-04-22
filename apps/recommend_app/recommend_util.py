# -*- coding: utf-8 -*-
'''
Created on Sep 5, 2013

@author: jin
'''
from django.contrib.auth.models import User
from apps.recommend_app.models import Grade, AppearanceVoteRecord
import MySQLdb
from pinloveweb import settings
from apps.common_app.models import School
from apps.user_app.models import UserProfile
from util import detect_device
from django.db.transaction import commit
""""
推荐信息填写情况
attribute：null

return: 填写情况(dict)
   
"""
def recommend_info_status(userId,channel='web'):
    '''
    channel 来源 web(电脑) mobile(手机)
    '''
    args={'result':True,'data':{}}
    #检测设备
    if channel=='mobile':
         dict={
          'userExpect':{'info':'Ta的身高打分','href':'/mobile/grade_height/'},
          'weight':{'info':'权重打分','href':'/mobile/get_weight/'},
          'tag':{'info':'性格标签','href':'/mobile/character_tag/'},
          'info':{'info':'个人信息','href':'/mobile/profile/'},
          'avatar':{'info':'头像','href':'/mobile/account/'}
          }
    else:
        dict={
          'userExpect':{'info':'Ta的身高打分','href':'/user/user_profile/#progress_'},
          'weight':{'info':'权重打分','href':'/user/user_profile/#weight_'},
          'tag':{'info':'性格标签','href':'/user/user_profile/#personality_'},
          'info':{'info':'个人信息','href':'/user/user_profile/#self_info_'},
          'avatar':{'info':'头像','href':'/user/user_profile/#upload_head_'}
          }
       
    from util.cache import get_recommend_status
    recommendStatus=get_recommend_status(userId)
    for key,value in recommendStatus.items():
        if not value: 
            args['data'][key]=dict[key]
    if len(args['data'])==0:
        args['result']=False
    return  args           
    
            

""""
根据用户id，相貌打分计算最终相貌分数
attribute：id ：用户id  int
           voteSocre: 相貌打分分数 int
return:   最终相貌分数
"""
def cal_looks(id,voteSocre):
    try:
        geadeInstance=Grade.objects.get(user_id=id)
    except Grade.DoesNotExist:
        print '根据id:'+id+'没有对应的grade'
        pass
    return (geadeInstance.appearancescore*(geadeInstance.appearancesvote)+voteSocre)/(geadeInstance.appearancesvote+1)
"""
根据用户收入计算用户收入分数
attribute ：
      user_income  用户收入 ：int
returns:
      收入得分
"""
def cal_income(user_income,gender):
    from apps.user_app.models import UserProfile
    overIncomeCount=UserProfile.objects.filter(income__lte=user_income).filter(gender=gender).exclude(income=-1).count()+0.00
    overIncomeCount=overIncomeCount-int((UserProfile.objects.filter(income=user_income).filter(gender=gender).exclude(income=-1).count()+0.00)/2)
    IncomeCount=UserProfile.objects.filter(gender=gender).exclude(income=-1).count()
    #print str(overIncomeCount)+" "+str(IncomeCount)
    return (overIncomeCount/IncomeCount)*100 if IncomeCount>0 else 100
'''
根据学历，学校计算分数
attribute：
      user_education : 学历 int
      school ：学校名字  string
return：
      score：学历分数
'''
def cal_education(user_education,school,gender,type):
        educationMap={'master':5,'doctor':10}
        if not School.objects.filter(name__startswith=school,name__endswith=school,country=type).exists():
            school=School.objects.all().order_by('-ranking')[0]
            return cal_ranking_score(school,gender,type)
        else :
            school=School.objects.get(name__startswith=school,name__endswith=school)
            if user_education==-1:
                return cal_ranking_score(school,gender,type)
            else:
                score=cal_ranking_score(school,gender,type)
                if user_education==3:
                    score+=educationMap.get('master')
                if user_education==4:
                    score+=educationMap.get('doctor')
                if score>100:
                    score=100
                return score

'''
计算排名
'''            
def cal_ranking_score(school,gender,type):
    #前20名为20档（一个名次一档）
    # 21-100名每10名为一档（比如说21-30为并列第21）
    # 100-最后每50名为一档（比如说101-150为并列第100）
    if school.ranking<=20:
        ranking=school.ranking
    elif school.ranking>20 and  school.ranking<=100:
         ranking=((school.ranking-1)/10)*10+1
    elif school.ranking>100:
         ranking=((school.ranking-1)/50)*50+1
         
    if type==1:
        school_sql='u1.educationSchool'
    else:
        school_sql='u1.educationSchool_2'
    sql="""
    SELECT count(*)
from user_profile u1 LEFT JOIN school u2 on """+school_sql+"""=u2.name
where (ranking>=%s and u2.country=%s and gender=%s) 
    """
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute(sql,[ranking,school.country,gender])
    schoolRankingCount=cursor.fetchone()[0]
    
    sql2="""
    SELECT count(*)
from user_profile u1 LEFT JOIN school u2 on """+school_sql+"""=u2.name
where (ranking=%s and u2.country=%s and gender=%s) 
    """
    cursor = connection.cursor()
    cursor.execute(sql2,[ranking,school.country,gender])
    schoolRankingCountCurrent=cursor.fetchone()[0]
    schoolRankingCount=schoolRankingCount-int((schoolRankingCountCurrent+0.00)/2)
    
    sql1="""
    SELECT count(*)
from user_profile u1 LEFT JOIN school u2 on """+school_sql+"""=u2.name
where u2.country=%s and gender=%s
    """
    cursor.execute(sql1,[school.country,gender])
    shcoolCount=cursor.fetchone()[0]
    cursor.close()
    #第一个用户
    if shcoolCount==0:
        return 100
    return int((schoolRankingCount+0.01)/shcoolCount*100)
    
'''
@param scoreId:打分人的用户id
@param param scoredId: 被打分人的用户id 可为空
@param score:用户打分
@param appearancescore:之前的外貌分数
@param appearancesvote: 之前的投票数
@param type:投票类型  
            0 系统打分  1 用户打分
    
相用户貌投票
得分=(原本用户外貌打分*（原本票数+DEFAULT_WEB_VOTE_NUM）+新用户投票分数)/(原本票数+1+DEFAULT_WEB_VOTE_NUM)
[注：DEFAULT_WEB_VOTE_NUM 为网站默认为用打分占的权重]
'''
def cal_user_vote(scoreId,scoredId,score,appearancescore,appearancesvote,type,**kwargs):
    from apps.recommend_app.recommend_settings import DEFAULT_WEB_VOTE_NUM
    #判断是否打过分
    flag=True
    appearanceVoteRecord=None
    scoreTmp=score
    if type==0:
        #前一次系统打分
        preScore=abs((appearancescore*(appearancesvote+DEFAULT_WEB_VOTE_NUM)-kwargs.get('sysappearancescore')*DEFAULT_WEB_VOTE_NUM)/(appearancesvote-DEFAULT_WEB_VOTE_NUM))
        score=(preScore*(appearancesvote)+score*DEFAULT_WEB_VOTE_NUM)/(appearancesvote+DEFAULT_WEB_VOTE_NUM)
            
    elif type==1:
        if AppearanceVoteRecord.objects.filter(user_id=scoreId,other_id=scoredId).exists():
            appearanceVoteRecord=AppearanceVoteRecord.objects.get(user_id=scoreId,other_id=scoredId)
        else:
            flag=False
            appearanceVoteRecord=AppearanceVoteRecord(user_id=scoreId,other_id=scoredId)
        if flag:
            #前一次系统打分
            preScore=(appearancescore*(appearancesvote+DEFAULT_WEB_VOTE_NUM)-appearanceVoteRecord.score)/(appearancesvote+DEFAULT_WEB_VOTE_NUM-1)
            appearanceVoteRecord.score=scoreTmp
            score=(preScore*(appearancesvote+DEFAULT_WEB_VOTE_NUM-1)+score)/(appearancesvote+DEFAULT_WEB_VOTE_NUM)
        else:
            score=(appearancescore*(appearancesvote+DEFAULT_WEB_VOTE_NUM)+score)/(appearancesvote+1+DEFAULT_WEB_VOTE_NUM)
            appearanceVoteRecord.score=scoreTmp
        appearanceVoteRecord.save()
        commit()
    else:
        raise Exception('type 参数错误')    
    return  {'score':score,'flag':flag}
 
def cal_recommend(userId,fields=[]):
    from util.cache import get_has_recommend,has_recommend
    for field in fields:
        has_recommend(userId,field)
    if get_has_recommend(userId): 
        connection = MySQLdb.connect(user=settings.DATABASES['default']['USER'],
                                          db=settings.DATABASES['default']['NAME'], passwd=settings.DATABASES['default']['PASSWORD'], host=settings.DATABASES['default']['HOST'])
        cursor=connection.cursor();
        r=cursor.callproc('recommend',[userId,])
        connection.commit()
        cursor.close()
            
