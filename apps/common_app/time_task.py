# -*- coding: utf-8 -*-
'''
Created on Sep 27, 2013

@author: jin
'''
from apps.user_app.models import UserProfile
from apps.recommend_app.recommend_util import cal_income
def time_task():
    userProfileList=UserProfile.objects.all();
    for user in userProfileList:
        incomes=cal_income(user.income)
        from apps.recommend_app.models import Grade
        if Grade.objects.filter(user_id=user.user.id).exists():
               Grade.objects.filter(user_id=user.user.id).update(incomescore=incomes)
        else:
               Grade(user_id=user.user.id,incomescore=incomes).save()