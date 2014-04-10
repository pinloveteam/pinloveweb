# -*- coding: utf-8 -*-
'''
Created on 2014年1月9日

@author: jin
'''
#用于初始化用户所需要的信息
from apps.user_app.models import Follow
from django.utils import simplejson
from django.http.response import HttpResponse
def init_person_info_for_card_page(userProfile,**kwargs):
    arg={}
    arg['avatar_name']=userProfile.get_avatar_image()
    arg['age']=userProfile.age
    arg['gender']=userProfile.gender
    arg['height']=userProfile.height
    arg['income']=userProfile.income
    arg['education']=userProfile.get_education_display()
    arg['jobIndustry']=userProfile.get_jobIndustry_display()
    if kwargs.get('myFollowCount')==None:
        myFollowCount=Follow.objects.filter(my=userProfile.user).count()
    else:
        myFollowCount=kwargs.get('follow')
    if kwargs.get('follow')==None:
        fansCount=Follow.objects.filter(follow=userProfile.user).count()
    else:
        fansCount=kwargs.get('followEachCount')
    if kwargs.get('followEachCount')==None:
        followEachList=Follow.objects.follow_each(userProfile.user_id)
        followEachCount=len([followEach.my_id for followEach in followEachList])
    else:
        followEachCount=kwargs.get('followEachCount')   
    #相互关注的人的id
    arg['myFollow']=myFollowCount
    arg['fans']=fansCount
    arg['follow']=followEachCount
    return arg

'''
判断是否是相互关注
attribute：
  CardList :List[Card] Card 类的列表
  focusEachOtherList：list 相互关注用户id
'''
def is_focus_each_other(request,cardList,focusEachOtherList):
    i=0
    focus = Follow.objects.select_related().filter(my=request.user)
    for user in cardList:
        for f in focus:
            if user.user_id == f.follow_id:
                if  user.user_id in focusEachOtherList:
                    cardList[i].followStatus=2
                else:
                    cardList[i].followStatus=1
        i+=1
    return cardList

fansCount=Follow.objects.filter(follow=1).count()
print fansCount


'''
通过ajax加载页面card
'''
def load_cards_by_ajax(request,cardList):
         data={}
         data['has_next']=cardList.has_next()
         if cardList.has_next():
             data['next_page_number']=cardList.next_page_number()
         if cardList.has_previous():
            data['previous_page_number']=cardList.previous_page_number()
         data['has_previous']=cardList.has_previous()
         data['result']='success'
         if request.GET.get('choseCards[]')!=None:
             choseCardslist=request.GET.getlist('choseCards[]')
             cardList.object_list = [card for card in cardList.object_list if str(card.user_id) not in choseCardslist]
             if len(cardList.object_list)<8:
                 data['removeCard']=True
#              for matchResult in cardList.object_list:
#                  if str(matchResult.user_id) in choseCardslist:
#                      cardList.object_list.remove(matchResult) 
#                      data['removeCard']=True
         data['cards']=cardList.object_list
         from apps.pojo.card import MyEncoder
         json=simplejson.dumps(data,cls=MyEncoder)
         return HttpResponse(json)
     
'''
生成邀请码
'''
def create_invite_code(userId):
    import random
    randomInt=random.randint(1001, 9999)
    from util.util import random_str
    randomStr=random_str(randomlength=5)
    return '%s%s%s' % (userId,randomInt,randomStr)