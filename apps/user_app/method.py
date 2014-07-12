# -*- coding: utf-8 -*-
import sys   
import time
from apps.user_app.models import UserProfile, UserTag, Follow,\
    BrowseOherScoreHistory
import logging
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
            'jobIndustry':userProfile.jobIndustry,
            'city':userProfile.city,
            'sunSign':userProfile.get_sunSign_display(),
            'gender':userProfile.gender,
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
def get_detail_info(userId):
    userProfile=UserProfile.objects.get_user_info(userId)
    tagList=UserTag.objects.select_related('tag').filter(user_id=userId,type=0)
    return user_info_card(userProfile,tagList)

'''
获取用户头像
'''
def get_avatar_name(myId,userId):
    return UserProfile.objects.get_avatar_name(myId, userId)

def detailed_info_div(myId,userId,compareId=None):
    args={}
    flag=False
    detailDict=get_detail_info(userId)
    from apps.recommend_app.views import get_socre_for_other
    args['socreForOther']=get_socre_for_other(myId,userId)
    head_color = 'head_girl' if detailDict['gender']=='F' else 'head_boy'
#     keys=''
#     for key in args['socreForOther'].keys():
#         keys+=key+'====='
#     logging.error('======='+keys)
    if not compareId is None:
        flag=True
        data=get_detail_info(compareId)
        compareTags=''
        for tag in data['tagTupe']:
            compareTags+='%s%s%s'%('<span class="label label-info">',tag,'</span>\r')
            
        args['compareSocreForOther']=get_socre_for_other(myId,compareId)
    tags=''
    for tag in detailDict['tagTupe']:
        tags+='%s%s%s'%('<span class="label label-info">',tag,'</span>\r')
    if flag:
        compareTag='取消对比'
        left=8
        width=''
    else:
        compareTag='对比'
        left=25
        width='width:780px'
    detail='''<div id="detail_info_div" class="container poplayer" style="top:10%%;left: %s%%;padding: 0;%s">
<div class="row">
<div class="col-xs-4" style="border-right: solid 2px #00CCCC;">

<div class="main">
<div class="head %s">
<img src="/media/%s-110.jpeg" alt="当前头像">
</div>
<div style="display: inline-block;width: 260px;position: relative;top:-40px;">
<span><strong>%s</strong></span>
<br>
<span>%s</span>
</div>
<br>
<button id="compare-button" class="btn btn-info compare-btn">
%s
</button>
<input id="vote" name="vote" >
<button id="vote-button" class="btn btn-info">
打分
</button>
</div>

<div>
   %s
</div>
<table class="table">
<tbody>
<tr>
<td><i class="icon icon-height"></i>&nbsp;&nbsp;身高：%s</td>
<td><i class="icon icon-education"></i>&nbsp;&nbsp;学历：%s</td>
</tr>
<tr>
<td><i class="icon icon-age"></i>&nbsp;&nbsp;年龄：%s</td>
<td><i class="icon icon-income"></i>&nbsp;&nbsp;收入：%s</td>
</tr>
<tr>
<td><i class="icon icon-trade"></i>&nbsp;&nbsp;行业：%s</td>
<td><i class="icon icon-constellation"></i>&nbsp;&nbsp;星座:%s</td>
</tr>
</tbody>
</table>
</div>
'''%(left,width,head_color,detailDict['avatar_name'],detailDict['username'],detailDict['city'],compareTag,tags,detailDict['height'],detailDict['education'],detailDict['age'],detailDict['income'],detailDict['jobIndustry'],detailDict['sunSign'],)

    if flag:
        head_color = 'head_girl' if data['gender']=='F' else 'head_boy'
        canvasDiv=canvas_div(args['socreForOther'],flag,args['compareSocreForOther'])
        detail+=canvasDiv
        compare='''
        <div class="col-xs-4" style="border-left: solid 2px #00CCCC;">

<div class="main">
<div class="head %s">
<img src="/media/%s-110.jpeg" alt="当前头像">
</div>
<div style="display: inline-block;width: 260px;position: relative;top:-40px;">
<span><strong>%s</strong></span>
<br>
<span>%s</span>
</div>
<br>
<button class="btn btn-info compare-btn_1">
%s
</button>
</div>

<div>
   %s
</div>
<table class="table">
<tbody>
<tr>
<td><i class="icon icon-height"></i>&nbsp;&nbsp;身高：%s</td>
<td><i class="icon icon-education"></i>&nbsp;&nbsp;学历：%s</td>
</tr>
<tr>
<td><i class="icon icon-age"></i>&nbsp;&nbsp;年龄：%s</td>
<td><i class="icon icon-income"></i>&nbsp;&nbsp;收入：%s</td>
</tr>
<tr>
<td><i class="icon icon-trade"></i>&nbsp;&nbsp;行业：%s</td>
<td><i class="icon icon-constellation"></i>&nbsp;&nbsp;星座:%s</td>
</tr>
</tbody>
</table>
</div>
</div>
</div>'''%(head_color,data['avatar_name'],data['username'],data['city'],compareTag,compareTags,data['height'],data['education'],data['age'],data['income'],data['jobIndustry'],data['sunSign'],)
        detail+=compare
        
    else:
         canvasDiv=canvas_div(args['socreForOther'],flag)
         detail+=canvasDiv
#          print detail
    args['detail']=detail.replace('\n', '')
    if args['socreForOther']['result']=='success':
         from util.util import is_guide
         guide=UserProfile.objects.get_user_info(myId).guide
         if not is_guide(myId,guide,'compareButton'):
             args['compare_button']=True
    return args  

'''
获得雷达图的div
scoreMatch 我对对方打分的
compareFlag  是否有对比用户
compareScoreMatch 对比用户我对对方打分的

'''
def canvas_div(scoreMatch,compareFlag,compareScoreMatch=None):
    canvasDiv='''<div class="col-xs-4" id="radar" >
<div class="">
<div class="score">
<span>%s</span>
<a onclick="buy_score_for_other(%s)"><i title="让对方看见" class="icon icon-eye"></i></a>
</div>
<div class="score score_other">
%s
<span>%s</span>
</div>
</div>

<canvas class="radar" height="370px" width="370px"></canvas>
<div class="">
<div class="score">
<span>%s</span>
</div>
<div class="score score_other">
<span>%s</span>
</div>
</div>
</div>'''
    if scoreMatch['result']=='success':
        compareScoreOther=''
        compareScoreMyself=''
        compareEye=''
        if compareFlag:
            compareScoreOther=int(compareScoreMatch['matchResult']['scoreOther'])
            if compareScoreMatch['matchResult'].get('scoreMyself',None)!=None:
                compareScoreMyself=int(compareScoreMatch['matchResult'].get('scoreMyself'))
            else:
                compareScoreMyself='<button value="%s">查<button>'%(compareScoreMatch['matchResult']['userId'])
        if scoreMatch['matchResult'].get('scoreMyself',None)!=None:
            scoreMyself= int(scoreMatch['matchResult'].get('scoreMyself'))
            compareEye='<a onclick="buy_score_for_other(%s)"><i class="icon icon-eye" ></i></a>'%(scoreMatch['matchResult']['userId'])
        else:
            scoreMyself='<button value="%s" >查<button>'%(scoreMatch['matchResult']['userId'])
        canvasDiv=canvasDiv%(int(scoreMatch['matchResult']['scoreOther']),scoreMatch['matchResult']['userId'],compareEye,compareScoreOther,scoreMyself,compareScoreMyself)
    else:
        canvasDiv='<div class="col-xs-4" id="radar" >为了显示雷达图，请您首先填写完整的个人信息</div>'
#         canvasDiv='<div class="col-xs-4" id="radar" >'+scoreMatch['error_messge']+'</div>'

    return canvasDiv
        
    
    