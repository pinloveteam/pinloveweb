# -*- coding: utf-8 -*-


from apps.user_app.models import UserProfile
from apps.recommend_app.models import Grade
def task_run():
    userProfileList=UserProfile.objects.all()
    for userProfile in userProfileList:
        cal_income_task(userProfile.user_id,userProfile.income,userProfile.gender)
        cal_education_task(userProfile.user_id,userProfile.gender,userProfile.education,userProfile.educationSchool,userProfile.educationSchool_2)

'''
计算收入
'''      
def cal_income_task(user_id,income,gender):
    if income==None or income==-1:
        return False
    from apps.recommend_app.recommend_util import cal_income
    incomescore=cal_income(income,gender)
    Grade.objects.filter(user_id=user_id).update(incomescore=incomescore)
        
        
'''
计算学历
'''       
def cal_education_task(user_id,gender,education,educationSchool,educationSchool_2):
    if (educationSchool_2==None or educationSchool_2.rstrip() ==u'' )and (educationSchool==None or educationSchool.rstrip() ==u''):
        return False
    from apps.recommend_app.recommend_util import cal_education
    if educationSchool_2==None:
        educationscore=cal_education(education,educationSchool,gender)
    else:
        SchoolScore1=cal_education(education,educationSchool,gender)
        SchoolScore2=0
        if educationSchool_2 != None and educationSchool_2.rstrip() !=u'':
            SchoolScore2=cal_education(education,educationSchool_2,gender)
        if SchoolScore1>SchoolScore2:
            educationscore=SchoolScore1
        else:
            educationscore=SchoolScore2
#             educationscore=cal_education(self.education,self.educationSchool)
        if Grade.objects.filter(user_id=user_id).exists():
            Grade.objects.filter(user_id=user_id).update(educationscore=educationscore)