# -*- coding: utf-8 -*-
'''
Created on Sep 3, 2013

@author: jin
'''
from apps.user_app.models import UserProfile, Follow, UserTag
from apps.recommend_app.models import MatchResult, Grade, UserExpect
from util.page import page
from django.shortcuts import render
from apps.upload_avatar import app_settings
from apps.pojo.recommend import RecommendResult
from apps.recommend_app.form import WeightForm
from django.utils import simplejson
from django.core.context_processors import csrf
from django.http import HttpResponse
import logging
from django.views.decorators.csrf import csrf_exempt
logger = logging.getLogger(__name__)  
#######################################
#1.0使用版本
#######################################
'''
 更新权重
'''
@csrf_exempt
def update_weight(request):
    args={}
    flag=True
    try:
        height=float(request.POST.get('height',-1))/100
        income=float(request.POST.get('income',-1))/100
        appearance=float(request.POST.get('appearance',-1))/100
        education=float(request.POST.get('education',-1))/100
        character=float(request.POST.get('character',-1))/100
    except Exception as e:
        flag=False
        args['result']='error'
        args['msg']='传输参类型错误！'
        logger.error('传输参类型错误！',e)
    if ( education<0 and education<0 and income<0 and appearance<0 and height<0):
        flag=False
        args['result']='error'
        args['msg']='传输参数错误！'
    if flag:
        Grade.objects.create_update_grade(request.user.id,heightweight=height,\
                                          incomeweight=income,educationweight=education,appearanceweight=appearance,characterweight=character)
        #判断推荐条件是否完善
        from apps.recommend_app.recommend_util import cal_recommend
        cal_recommend(request.user.id,['grade'])
        args['result']='success'
    else:
        args['result']='error'
    json=simplejson.dumps(args)
    return HttpResponse(json)


def grade_for_other(request):
    args={}
    if request.method=="POST":
        flag=True
        try:
            result=request.POST.get('result',False)
            tags=request.REQUEST.get('tagList',False)
        except Exception as e:
            flag=False
            args['result']='error'
            args['msg']='传输参类型错误！'
            logger.error('传输参类型错误！',e)
        if not( result and tags ):
            flag=False
            args['result']='error'
            args['msg']='传输参数错误！'
        if flag:
            tagList=tags.split(',')
            s=result.split(',')
            UserExpect.objects.create_update_by_uid(user_id=request.user.id,heighty1=float(s[1]),heighty2=float(s[3]),heighty3=float(s[5]),heighty4=float(s[7]),heighty5=float(s[9]) ,heighty6=float(s[11]),heighty7=float(s[13]),heighty8=float(s[15]))
            UserTag.objects.filter(user=request.user,type=1).delete()
            UserTag.objects.bulk_insert_user_tag(request.user.id,1,tagList)   
            #判断推荐条件是否完善
            from apps.recommend_app.recommend_util import cal_recommend
            cal_recommend(request.user.id,['userExpect','tag'])     
            args['result']='success'
        json=simplejson.dumps(args)
        return HttpResponse(json)
 
'''
 获取另一半对自己打分
'''   
def socre_my(request):
    args={}
    try:
        otherId=int(request.REQUEST.get('userId',False))
        if otherId:
            member=UserProfile.objects.get(user_id=request.user.id).member
            from apps.user_app.models import BrowseOherScoreHistory
            flag=BrowseOherScoreHistory.objects.filter(my_id=request.user.id,other_id=otherId).exists()
            if member>0 or flag:
                matchResult=get_matchresult(request,otherId)
                args={'result':'success','scoreMyself':int(matchResult.scoreMyself)}
                     
            else:
                from apps.user_score_app.method import use_score_by_other_score
                result=use_score_by_other_score(request.user.id,otherId)
                if result=='success':
                    matchResult=get_matchresult(request,otherId)
                    #保存浏览记录
                    BrowseOherScoreHistory(my_id=request.user.id,other_id=otherId).save()
                    args={'result':'success','scoreMyself':int(matchResult.scoreMyself)}
                elif result=='less':
                        args={'result':'error','error_messge':'请充值!'}
        else:
            args={'result':'error','error_messge':'用户id不存在!'}
        json=simplejson.dumps(args)
        return HttpResponse(json)
    except Exception as e:
        logger.error('%s%s' %('获取另一半对自己打分出错',e))
        args={'result':'error','error_messge':'%s%s' %('获取另一半对自己打分出错',e)}
#         args={'result':'error','error_messge':'系统出错!'}
        json=simplejson.dumps(args)
        return HttpResponse(json)
  
def get_matchresult(request,otherId):  
    from apps.recommend_app.method import get_recommend_result_in_session
    matchResult=get_recommend_result_in_session(request,otherId)
    if matchResult is None:
        from apps.recommend_app.method import get_match_score_other
        matchResult=get_match_score_other(request.user.id,otherId)
        if matchResult is None:
            from apps.recommend_app.method import match_score
            matchResult=match_score(request.user.id,otherId)
        else:
            from apps.pojo.recommend import MarchResult_to_RecommendResult
            matchResult=MarchResult_to_RecommendResult(matchResult)
    return matchResult
                  
     
'''
获得对自己对另一半的打分
'''
def get_socre_for_other(request):    
    args={}
    try:
        otherId=int(request.REQUEST.get('userId',False))
        if otherId:
             from apps.recommend_app.method import get_match_score_other
             matchResult=get_match_score_other(request.user.id,otherId)
             if matchResult==None:
                from apps.recommend_app.method import get_recommend_result_in_session
                matchResult=get_recommend_result_in_session(request,otherId)
                if matchResult is None:
                 #判断是否可用匹配
                 from util.cache import get_has_recommend,get_recommend_status,has_recommend
                 for field in ['userProfile','userExpect','grade','tag']:
                     has_recommend(request.user.id,field)
                 if get_has_recommend(request.user.id):
                     from apps.recommend_app.method import match_score
                     matchResult=match_score(request.user.id,otherId)
                     member=UserProfile.objects.get(user_id=request.user.id).member
                     args={'result':'success','matchResult':matchResult.get_dict(member=member)}
                     from apps.recommend_app.method import set_recommend_result_in_session
                     set_recommend_result_in_session(request,matchResult)
                 else:
                     recommendStatus=get_recommend_status(request.user.id)
                     dict={'userProfile':u'个人信息  ','userExpect':u'身高期望  ','grade':u'权重  ','tag':u'标签  '}
                     errorMessge=''
                     for key in recommendStatus.keys():
                         if not recommendStatus[key]:
                             errorMessge+=dict[key]
                     args={'result':'error','error_messge':'%s%s' %(errorMessge,u'未填写完整!')}
                else:
                    member=UserProfile.objects.get(user_id=request.user.id).member
                    args={'result':'success','matchResult':matchResult.get_dict(member=member)} 
             else:
                 member=UserProfile.objects.get(user_id=request.user.id).member
                 from apps.pojo.recommend import MarchResult_to_RecommendResult
                 matchResult=MarchResult_to_RecommendResult(matchResult)
                 args={'result':'success','matchResult':matchResult.get_dict(member=member)}
        else:
            args={'result':'error','error_messge':'用户id不存在!'}
        json=simplejson.dumps(args)
        return HttpResponse(json)
    except Exception as e:
        logger.error('%s%s' %('获得对自己对另一半的打分，出错原因：',e))
        args={'result':'error','error_messge':'系统出错!'}
        json=simplejson.dumps(args)
        return HttpResponse(json)
##########################################
def recommend(request):
    arg={}
    count=MatchResult.objects.filter(my_id=request.user.id).count()
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
         matchResultList=MatchResult.objects.filter(my_id=request.user.id)
         arg=page(request,matchResultList)
         matchResultList=arg['pages']
         matchResultList.object_list=matchResultList_to_RecommendResultList(matchResultList.object_list)
         friends = Follow.objects.filter(myId=request.user.id)
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
          friends = Follow.objects.filter(my=request.user)
          i=0 
          for user in matchResultList:
           for friend in friends:
               if user.user_id == friend.id:
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
       city=userBaiscProfile.city
       isFriend=0
       if userBaiscProfile.avatar_name_status==3:
           isVote=True
       else:
           isVote=False
       recommendResult=RecommendResult(userId,username,avatar_name,height,age,education,income,jobIndustry,scoreOther,scoreMyself,macthScore,isFriend,isVote,city)
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
       isFriend=0
       city=userProfile.city
       if userProfile.avatar_name_status=='3':
           avatar_name=userProfile.avatar_name
           isVote=True
       else:
           avatar_name='user_img/image.png'
           isVote=False
       recommendResult=RecommendResult(userId,username,avatar_name,height,age,education,income,jobIndustry,scoreOther,scoreMyself,macthScore,isFriend,isVote,city)
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
                                                                      incomeweight=grade.heightweight,educationweight=grade.heightweight,appearanceweight=grade.heightweight,characterweight=grade.heightweight)
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
def grade_for_other_1(request):
    arg={}
    if request.user.is_authenticated():
        count=UserExpect.objects.filter(user=request.user).count()
        if request.method=="POST":
                result=request.POST['result']
                s=result.split(',')
#             gradeForOther=GradeForOther(request.POST)
#             if gradeForOther.is_valid():
#                 grade = gradeForOther.save(commit=False)
                grade=UserExpect(user=request.user,heighty1=float(s[1]),heighty2=float(s[3]),heighty3=float(s[5]),heighty4=float(s[7]),heighty5=float(s[9]) ,heighty6=float(s[11]),heighty7=float(s[13]),heighty8=float(s[15]),)
                if count!=0:
                    grade.id=UserExpect.objects.get(user_id=request.user.id).id
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
       
def test_match(request):
    args={}
    userId=int(request.GET.get('userId'))
    gradeMy=Grade.objects.get(user_id=request.user.id)
    matchResult=MatchResult.objects.get(my_id=request.user.id,other_id=userId)
    grade=Grade.objects.get(user_id=userId)
    args['我的收入得分']=gradeMy.incomescore
    args['我的学历得分']=gradeMy.educationscore
    args['我的外貌得分']=gradeMy.appearancescore
    #对方得分
    args['对方的收入得分']=grade.incomescore
    args['对方的学历得分']=grade.educationscore
    args['对方的外貌得分']=grade.appearancescore
    #相互打分
    args['异性对我的打分和']=matchResult.scoreMyself
    args['我对异性的打分和']=matchResult.scoreMyself
#     args['macthScore']=matchResult.macthScore
    args['我对异性的身高打分（权重）']=matchResult.heighMatchOther
    args['异性对我的身高打分（权重）']=matchResult.heighMatchMy
    args['异性对我的收入打分（权重）']=matchResult.incomeMatchMy
    args['我对异性的收入打分（权重）']=matchResult.incomeMatchOther
    args['我对异性的学历打分（权重）']=matchResult.edcationMatchOther
    args['异性对我的学历打分（权重）']=matchResult.edcationMatchMy
    args['我对异性的外貌打分（权重）']=matchResult.appearanceMatchOther
    args['异性对我的外貌打分（权重）']=matchResult.appearanceMatchMy
    args['异性对我的性格打分（权重）']= matchResult.characterMatchMy
    args['异性对我的性格打分（权重）']=matchResult.characterMatchMy 
    
    args['我匹配标签得分']=matchResult.tagMatchOtherScore
    args['异性对我的匹配标签得分']=matchResult.tagMatchMyScore
    args['我匹配身高得分']=matchResult.heighMatchOtherScore
    args['异性对我的身高标签得分']=matchResult.heighMatchMyScore
    json=simplejson.dumps(args)
    return HttpResponse(json)