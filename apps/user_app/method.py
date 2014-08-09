# -*- coding: utf-8 -*-
import sys   
from apps.user_app.models import UserProfile, UserTag, Follow,\
    BrowseOherScoreHistory, BlackList, Denounce
from apps.recommend_app.models import  AppearanceVoteRecord
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
    for field in fields:
        if  not getattr(userProfile,field) in [-1,'N',None,u'',u'地级市、县',u'国家',u'请选择']:
            if getattr(userProfile,field)!=getattr(oldUserProfile,field):
                updateFields.append(field)
            num+=1
    from apps.user_score_app.method import get_score_by_finish_proflie
    profileFinsihPercent=int((num+0.00)/len(fields)*100)
    if profileFinsihPercent>userProfile.profileFinsihPercent:
        get_score_by_finish_proflie(userProfile.user_id,updateFields)
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
    return BlackList.objects.filter(my_id=userId)
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
        tags.append(tag.tag.content)
    isVote=False
    voteScore=-1
    if userProfile.avatar_name_status=='3':
        isVote=True
        if AppearanceVoteRecord.objects.filter(user_id=myId,other_id=userId).exists():
            voteScore=int(AppearanceVoteRecord.objects.get(user_id=myId,other_id=userId).score)
        else:
            voteScore=0
    data={
                        'head' : '%s%s%s'%('/media/',userProfile.avatar_name,'-110.jpeg'),
                        'tag' : tags,
                        'name' : userProfile.user.username,
                        'userId':userProfile.user_id,
                        'age' : userProfile.age,
                        'city' : userProfile.city,
                        'height' :userProfile.height,
                        'education' : userProfile.get_education_display(),
                        'income' : userProfile.income,
                        'trade' : userProfile.get_jobIndustry_display(),
                        'constellation' : userProfile.get_sunSign_display(),
                        'score' :int(socreForOther['matchResult']['scoreOther']),
                        'isVote':isVote,
                        'voteScore':voteScore,
                        'data' : [socreForOther['matchResult']['edcationScore'],socreForOther['matchResult']['characterScore'],socreForOther['matchResult']['incomeScore'],socreForOther['matchResult']['appearanceScore'],socreForOther['matchResult']['heighScore'],]
                    }
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
    #获取页面详细信息
    args['user1']=get_detail_info(myId,userId,socreForOther)
    if not compareId is None:
        compareSocreForOther=get_socre_for_other(myId,compareId)
        args['user2']=get_detail_info(myId,compareId,compareSocreForOther)
    return args
    