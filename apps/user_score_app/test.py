# -*- coding: utf-8 -*-
'''
Created on 2014年4月5日

@author: jin
'''
from django.http.response import HttpResponse
def score_test(request):
    test_reset_count()
    return HttpResponse('success')

def test_reset_count():
    from apps.user_score_app.method import reset_count
    reset_count()
    
    
def score_test1(request):
    from apps.user_app.models import UserProfile
    userProfileList=UserProfile.objects.all()
    for userProfile in userProfileList:
      if userProfile.link=='me':
        from pinloveweb.method import create_invite_code
        userProfile.link=create_invite_code(userProfile.user_id)
        userProfile.save()
#     userScoreList=UserScore.objects.all()
#     from django.contrib.auth.models import User
#     userList=User.objects.all()
#     idList=[]
#     idLists=[]
#     for userScore in userScoreList:
#         idList.append(userScore.user_id)
#     for user in userList:
#         if not user.id in idList:
#             idLists.append(user.id)
#     userScoreList=[]
#     for id in idLists:
#         userScore=UserScore()
#         userScore.user_id=id
#         userScoreList.append(userScore)
#     UserScore.objects.bulk_create(userScoreList)
    return HttpResponse('succes')