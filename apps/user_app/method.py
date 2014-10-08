# -*- coding: utf-8 -*-
import sys   
from apps.user_app.models import UserProfile, UserTag, Follow,\
    BrowseOherScoreHistory, BlackList, Denounce
from apps.recommend_app.models import  AppearanceVoteRecord
from django.utils import simplejson
reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入   
sys.setdefaultencoding('utf-8')  
'''
Created on Dec 23, 2013

@author: jin
'''
#用户信息未填时返回的值
missing_value=[-1,'N',None,]
def user_info_card(userProfile,userTagBeanList):
    avatar_name=userProfile.get_avatar_image()
    data={
            'avatar_name':avatar_name,
            'username':userProfile.user.username,
            'height':userProfile.height,
            'age':userProfile.age,
            'education':userProfile.get_education_display(),
            'income':userProfile.income,
            'jobIndustry':userProfile.get_jobIndustry_display(),
            'city':userProfile.city,
            'sunSign':userProfile.get_sunSign_display(),
            'gender':userProfile.gender,
            'avatar_name_status':userProfile.avatar_name_status
            }
    #获取标签信息
    tagTupe=()
    for userTag in userTagBeanList:
        tagTupe+=(userTag.tag.content,)
    data['tagTupe']=tagTupe
    #判断信息是否未填
    for  key in data.keys():
        if data[key] in missing_value:
            data[key]='未填'
    return data

'''
信息完成度
'''
def get_profile_finish_percent_and_score(userProfile,oldUserProfile):
    fields = ( 'income','weight','jobIndustry',
        'height', 'education', 'day_of_birth','educationSchool','city')
    updateFields=[]
    num=0
    finishList=None
    if userProfile.finish !=None:
        finishList=simplejson.loads(userProfile.finish)
    else:
        finishList=[]
    for field in fields:
        if  not getattr(userProfile,field) in [-1,'N',None,u'',u'地级市、县',u'国家',u'请选择']:
            if getattr(userProfile,field)!=getattr(oldUserProfile,field):
                if field not in finishList:
                    updateFields.append(field)
            num+=1
    from apps.user_score_app.method import get_score_by_finish_proflie
    profileFinsihPercent=int((num+0.00)/len(fields)*100)
    if profileFinsihPercent>userProfile.profileFinsihPercent:
        get_score_by_finish_proflie(userProfile.user_id,updateFields)
        finishList.extend(updateFields)
        userProfile.finish=simplejson.dumps(finishList)
        userProfile.profileFinsihPercent=profileFinsihPercent
    return userProfile

'''
职员员名单
'''
def get_staff_list():
    from django.contrib.auth.models import User
    return [user.id for user in User.objects.all()if user.is_staff]
'''
根据用户id列表查看聊天权限
myId  我的用户id
oherIdList 另外用户id列表，如果为None则查询所有用户
followIdList 相互关注用户id列表 如果为空则查询
historyIdList 相互购买对方对我的打分用户id列表，如果为空则查询
'''
def get_chat_permission_by_user_ids(myId,oherIdList=None,followIdList=None,historyIdList=None):
    if followIdList is None:
        followIdList=[follow.my_id for follow in Follow.objects.follow_each(myId,oherIdList=oherIdList)]
    if historyIdList is None:
        historyIdList=[history.other_id for history in BrowseOherScoreHistory.objects.browse_score_each_other(myId,oherIdList=oherIdList)]
    for id in historyIdList:
        if not id in followIdList:
            followIdList.append(id)
    return followIdList
    
'''
添加黑名单
myId  拉黑名单的用户id
otherId 被拉黑名单的用户id

'''
def update_black_list(myId,otherId):  
    if not BlackList.objects.filter(my_id=myId,other_id=otherId).exists():
        BlackList(my_id=myId,other_id=otherId).save()
        return 1
    else:
        BlackList.objects.filter(my_id=myId,other_id=otherId).delete()
        return -1 
    
'''
根据用户名获取黑名单列表
@param userId:用户id
@return:  List[BlackList] 黑名单列表
   
'''
def get_black_list(userId):
    return [int(user.other_id) for user in BlackList.objects.filter(my_id=userId)]
'''
 举报用户
'''
def add_denounce(myId,otherId,comeFrom,auid,type,resson=None):
    Denounce(my_id=myId,other_id=otherId,comeFrom=comeFrom,auid=auid,type=type,resson=resson).save()
     
      
'''
根据用户id列表查看是否聊天权限
myId  我的用户id
followIdList 相互关注用户id列表 如果为空则查询
historyIdList 相互购买对方对我的打分用户id列表，如果为空则查询
'''
def is_chat(myId,cardList,followIdList=None,historyIdList=None):
    oherIdList=[card.user_id for card in cardList]
    userIdList=get_chat_permission_by_user_ids(myId,oherIdList=oherIdList,followIdList=followIdList,historyIdList=historyIdList)
    for card in cardList:
        if card.user_id in userIdList:
            card.isChat=True
    return cardList
    
'''
详细信息页面
'''
def get_detail_info(myId,userId,socreForOther):
    userProfile=UserProfile.objects.select_related('user').get(user_id=userId)
    #获取标签信息
    tagList=UserTag.objects.select_related('tag').filter(user_id=userId,type=0)
    tags=[]
    for tag in tagList:
        if tag.tag.id<24:
            tags.append(tag.tag.content)
    isVote=False
    voteScore=-1
    from apps.upload_avatar.app_settings import DEFAULT_IMAGE_NAME
    data={
                        'head' : '%s%s%s'%('/media/', userProfile.avatar_name if userProfile.avatar_name_status=='3' else DEFAULT_IMAGE_NAME,'-100.jpeg'),
                        'tag' : tags,
                        'name' : userProfile.user.username,
                        'userId':userProfile.user_id,
                        'age' : ('%s%s' % (userProfile.age ,'岁')) if userProfile.age!=None  else userProfile.age,
                        'city' :  userProfile.limit_city_length(),
                        'height' :('%s%s' % (userProfile.height,'cm')) if userProfile.height!=-1 else userProfile.height,
                        'education' : userProfile.get_education_display(),
                        'income' : userProfile.get_income_display(),
                        'trade' : userProfile.get_jobIndustry_display(),
                        'constellation' : userProfile.get_sunSign_display(),
                        'isVote':False,
                    }
    if socreForOther['result']=='success':
        if userProfile.avatar_name_status=='3':
            isVote=True
            if AppearanceVoteRecord.objects.filter(user_id=myId,other_id=userId).exists():
                voteScore=int(AppearanceVoteRecord.objects.get(user_id=myId,other_id=userId).score)
            else:
                voteScore=0
        data.update({
                     'score' :int(socreForOther['matchResult']['scoreOther']),
                        'isVote':isVote,
                        'voteScore':voteScore,
                        'scoreMy':int(socreForOther['matchResult'].get('scoreMyself',-3)),
                        'data' : [socreForOther['matchResult']['edcationScore'],socreForOther['matchResult']['characterScore'],socreForOther['matchResult']['incomeScore'],socreForOther['matchResult']['appearanceScore'],socreForOther['matchResult']['heighScore'],]
                     })
    for  key in data.keys():
        if data[key] in missing_value:
            data[key]='未填'
    return data

'''
获取用户头像
'''
def get_avatar_name(myId,userId):
    return UserProfile.objects.get_avatar_name(myId, userId)

def detailed_info_div(myId,userId,compareId=None):
    args={}
    from apps.recommend_app.views import get_socre_for_other
    socreForOther=get_socre_for_other(myId,userId)
    #判断个人信息是否填写完整
    if socreForOther['result']=='error':
        args['result']='error'
        args['error_message']=socreForOther['error_message']
        args['user1']=get_detail_info(myId,userId,socreForOther)
        return args
    #获取页面详细信息
    args['user1']=get_detail_info(myId,userId,socreForOther)
    if not compareId is None:
        compareSocreForOther=get_socre_for_other(myId,compareId)
        args['user2']=get_detail_info(myId,compareId,compareSocreForOther)
    args['result']='success'
    return args
    
'''
判断是否关注
@param myId:关注者的id
@param followId:被关注者的id 
'''
def is_follow(myId,followId):
    return Follow.objects.filter(my_id=myId,follow_id=followId).exists()

'''
判断是否相互关注
@param myId:关注者的id
@param followId:被关注者的id 
'''
def is_follow_each(myId,followId):
    userList=[myId,followId]
    return Follow.objects.filter(my_id__in=[myId,followId],follow_id__in=[myId,followId]).count()>=2

def get_select_info(className,*args,**kwargs):
    from apps.user_app.models import get_models
    classModels=get_models(className)
    if classModels==None:
        return None
    else:
        include=kwargs['include']
        exclude=kwargs['exclude']
        return classModels.filter(**include).exclude(**exclude)
