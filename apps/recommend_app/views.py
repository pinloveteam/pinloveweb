# -*- coding: utf-8 -*-
'''
Created on Sep 3, 2013

@author: jin
'''
from apps.user_app.models import UserProfile, Friend
from apps.recommend_app.models import matchResult, Grade, UserExpect
from util.page import page
from django.shortcuts import render
from util.connection_db import connection_to_db
from apps.upload_avatar import app_settings
from apps.pojo.recommend import RecommendResult
from apps.recommend_app.form import WeightForm, GradeForOther
from django.utils import simplejson
from django.http.response import HttpResponse
from django.core.context_processors import csrf

def recommend(request):
    arg={}
    count=matchResult.objects.filter(my_id=request.user.id).count()
    if request.user.is_authenticated():
#     if request.method=='POST':
#        minAge = request.POST['minAge']
#        maxAge = request.POST['maxAge']
#        if request.POST.get('image')!= None:
#            image = ' and c4.avatar_name is not null'
#        else:
#            image=''
#        user_basic=user_basic_profile.objects.get(user_id=request.user.id)
#        if count>0:
#            sql='''select c1.id as id,c1.username as username,c2.age as age,c2.gender as gender,
#           c2.education as education,c2.height,c2.income as income,c3.jobIndustry,c4.avatar_name
#           from recommend_app_matchresult c5 
#           LEFT JOIN user_app_user_basic_profile c2 on c5.my_id=c2.user_id
#           LEFT JOIN auth_user c1 on c1.id=c2.user_id 
#           LEFT JOIN user_app_user_study_work c3 on c1.id=c3.user_id  
#           LEFT JOIN user_app_user c4 on c1.id=c4.user_id 
#           where c1.id!='''+str(request.user.id)+' and c2.age>='+minAge+' and c2.age<='+maxAge+image+\
#           ' and c2.gender!='+"'"+user_basic.gender+"'"+' limit 0,1000'
#        else:
#            sql='''select c1.id as id,c1.username as username,c2.age as age,c2.gender as gender,
#           c2.education as education,c2.height,c2.income as income,c3.jobIndustry,c4.avatar_name
#           from user_app_user_basic_profile c2 
#           LEFT JOIN auth_user c1 on c1.id=c2.user_id 
#           LEFT JOIN user_app_user_study_work c3 on c1.id=c3.user_id  
#           LEFT JOIN user_app_user c4 on c1.id=c4.user_id  
#           where c1.id!='''+str(request.user.id)+' and c2.age>='+\
#           minAge+' and c2.age<='+maxAge+image+' and c2.gender!='+"'"+user_basic.gender+"'"++' limit 0,1000'
#        request.session['search_sql']=sql   
#         # 需要映射到field choices 的字段
#        searchRsultList=connection_to_db(sql)
#        arg=page(request,searchRsultList)  
#        searchRsultList=search_result_mapping_field(arg.get('pages'))
#        friends = Friend.objects.filter(myId=request.user.id)
#        i=0 
#        for user in searchRsultList:
#            searchRsultList[i].setdefault('isFriend',False)
#            for friend in friends:
#                if user['id'] == friend.friendId.id:
#                    searchRsultList[i]['isFriend']=True
#            i+=1
#        arg['pages'] = searchRsultList    
#     else:  
      if count>0:
         matchResultList=matchResult.objects.filter(my_id=request.user.id)
         arg=page(request,matchResultList)
         matchResultList=arg['pages']
         matchResultList.object_list=matchResultList_to_RecommendResultList(matchResultList.object_list)
         friends = Friend.objects.filter(myId=request.user.id)
         i=0 
         for user in matchResultList:
           for friend in friends:
               if user.user_id == friend.friendId.id:
                   matchResultList[i].isFriend=True
           i+=1
         arg['pages']=matchResultList
#          for i in arg.get('pages'):
#             print i.macthScore
         
      else:
          try:
              userProfile=UserProfile.objects.get(user=request.user)
          except:
              print'推荐获模块,用户信息失败'
              pass
          userProfileList=UserProfile.objects.exclude(user=request.user).exclude(gender=userProfile).order_by("?")
          # 需要映射到field choices 的字段
#           searchRsultList=connection_to_db(sql)
          arg=page(request,userProfileList)   
          matchResultList=arg['pages']
          matchResultList.object_list=userProfileList_to_RecommendResultList(matchResultList.object_list)
          friends = Friend.objects.filter(myId=request.user.id)
          i=0 
          for user in matchResultList:
           for friend in friends:
               if user.user_id == friend.friendId.id:
                   matchResultList[i].isFriend=True
           i+=1
          arg['pages']=matchResultList
      return render(request,'recommend.html',arg)
    else :
        return render(request, 'login.html', arg,) 
     
#映射到django 对象
def recommend_result_mapping_field(searchRsultList):
    for i in searchRsultList:
        if i['jobIndustry']!=None:
            i['jobIndustry']=dict(UserProfile.JOB_INDUSRY_CHOICE)[i['jobIndustry']]
        else :
            i['jobIndustry']='未填'
        i['income']=dict(UserProfile.INCOME_CHOICES)[i['income']]
        i['education']=dict(UserProfile.EDUCATION_DEGREE_CHOICES)[i['education']]
        if i['avatar_name']!=None:
             i['avatar_name']='user_img/'+ i['avatar_name']+'-'+str(app_settings.UPLOAD_AVATAR_DEFAULT_SIZE)+'.jpeg'
        else :
            i['avatar_name']='user_img/image.png'
#     print searchRsultList 
    return searchRsultList
'''
 推荐结果querySet转换RecommendResultList
'''
def matchResultList_to_RecommendResultList(matchResultList):
    recommendResultList=[]
    for matchResult in matchResultList:
       scoreOther=matchResult.scoreOther
       scoreMyself=matchResult.scoreMyself
       macthScore=matchResult.macthScore
       userBaiscProfile=matchResult.get_user_basic_profile()
       userId=matchResult.other_id
       username=matchResult.other.username
       height=userBaiscProfile.height
       age=userBaiscProfile.age
       education=userBaiscProfile.get_education_display()
       income=userBaiscProfile.income
       jobIndustry=userBaiscProfile.get_jobIndustry_display()
       avatar_name=userBaiscProfile.avatar_name
       isFriend=False
       if userBaiscProfile.avatar_name_status==3:
           isVote=True
       else:
           isVote=False
       recommendResult=RecommendResult(userId,username,avatar_name,height,age,education,income,jobIndustry,scoreOther,scoreMyself,macthScore,isFriend,isVote)
       recommendResultList.append(recommendResult)
    return recommendResultList

def userProfileList_to_RecommendResultList(userProfileList):
     recommendResultList=[]
     for userProfile in userProfileList:
       scoreOther=u'需完善个人信息'
       scoreMyself=u'需完善个人信息'
       macthScore=u'需完善个人信息'
       userId=userProfile.user_id
       username=userProfile.user.username
       height=userProfile.height
       age=userProfile.age
       education=userProfile.get_education_display()
       income=userProfile.income
       jobIndustry=userProfile.get_jobIndustry_display()
       avatar_name=userProfile.avatar_name
       isFriend=False
       if userProfile.avatar_name_status==3:
           isVote=True
       else:
           isVote=False
       recommendResult=RecommendResult(userId,username,avatar_name,height,age,education,income,jobIndustry,scoreOther,scoreMyself,macthScore,isFriend,isVote)
       recommendResultList.append(recommendResult)
     return recommendResultList
'''
用户权重选择
'''
def weight(request):
    arg={}
    if request.user.is_authenticated():
        count=Grade.objects.filter(user=request.user).count()
        if request.method=="POST":
            weightForm=WeightForm(request.POST)
            if weightForm.is_valid():
                grade = weightForm.save(commit=False)
                if count!=0:
                    Grade.objects.filter(user_id=request.user.id).update(heightweight=grade.heightweight,
                                                                      incomeweight=grade.heightweight,edcationweight=grade.heightweight,appearanceweight=grade.heightweight,characterweight=grade.heightweight)
                else:                                                    
                   grade.user=request.user
                   grade.save()
                from apps.recommend_app.recommend_util import cal_recommend
                cal_recommend(request.user.id)
                return render(request,'member/update_profile_success.html',arg,)
        else:
             weightForm=WeightForm()
             if count!=0:
                  grade=Grade.objects.get(user_id=request.user.id)
                  weightForm=WeightForm(instance=grade)
             arg['weight_form']=weightForm
             return render(request,'weight.html',arg)
    else:
        return render(request,'login.html',arg)
    
'''
用户对另一半的打分
'''
def grade_for_other(request):
    arg={}
    if request.user.is_authenticated():
        count=UserExpect.objects.filter(user=request.user).count()
        if request.method=="POST":
                result=request.POST['result']
                s=result.split(',')
#             gradeForOther=GradeForOther(request.POST)
#             if gradeForOther.is_valid():
#                 grade = gradeForOther.save(commit=False)
                grade=UserExpect(user=request.user,heighty1=float(s[1])/100,heighty2=float(s[3])/100,heighty3=float(s[5])/100,heighty4=float(s[7])/100,heighty5=float(s[9])/100 ,heighty6=float(s[11])/100,heighty7=float(s[13])/100,heighty8=float(s[15])/100,)
                if count!=0:
                    grade.id=UserExpect.objects.get(user_id=request.user.id).id
         
#                     grade.heighty1=float(s[1])/100
#                     grade.heighty2=float(s[3])/100
#                     grade.heighty3=float(s[5])/100
#                     grade.heighty4=float(s[7])/100
#                     grade.heighty5=float(s[9])/100
#                     grade.heighty6=float(s[11])/100
#                     grade.heighty7=float(s[13])/100
#                     grade.heighty8=float(s[15])/100
                grade.save()
                return render(request,'member/update_profile_success.html',arg,)
        else:
             grade=False
             if count!=0:
                  grade=UserExpect.objects.get(user_id=request.user.id)
#                   gradeForOther=GradeForOther(instance=grade)
             arg['grade_for_other']=grade
             return render(request,'grade_for_other.html',arg)
    else:
        return render(request,'login.html',arg)
'''
  用户投票
'''    
def user_vote(request):
     if request.user.is_authenticated() :
         score = request.GET.get('score')
         if score.strip()=='':
              result = '不能为空!'
              json = simplejson.dumps(result)
              return HttpResponse(json)
         try:
            geadeInstance=Grade.objects.get(user=request.user)
         except Grade.DoesNotExist:
             print '相用户貌投票出错，没有找到对应的用户'
             pass
         from apps.recommend_app.recommend_util import cal_user_vote
         score=cal_user_vote(float(score),geadeInstance)
         Grade.objects.filter(user=request.user).update(appearancescore=score,appearancesvote=geadeInstance.appearancesvote+1)
         result = '评价成功!'
         json = simplejson.dumps(result)
         return HttpResponse(json)
     else:
           args = {}
           args.update(csrf(request))
           return render(request, 'login.html', args) 