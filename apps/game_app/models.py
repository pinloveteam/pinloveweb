# -*- coding: utf-8 -*-
import datetime

from django.core.cache import cache
from apps.third_party_login_app.models import FacebookUser, FacebookPhoto
import simplejson

class Yuanfenjigsaw:
#     selected_pieces_str = ''
    pieces = set()
    matching_pieces = set()
    uid = ''
    gender = ''
    def __init__(self,request):
        if cache.get('TODAY') != datetime.date.today():
            reset_game()
            get_count(request)
        self.uid = request.GET.get('uid')
        facebookUser=FacebookUser.objects.get(uid=self.uid)
        
#         self.pieces = set([int(i) for i in self.selected_pieces_str.split("-") if i])#用户提交的集合
        self.pieces = self.generate_pieces()
        self.matching_pieces = self.pieces#与之互补的集合
        self.gender = facebookUser.gender
        self.recommendList=simplejson.loads(facebookUser.recommendList)
        
#     def data_unavailable(self):
#         return  self.pieces - cache.get('ALL_PIECE') != set([]) or self.matching_pieces ==  cache.get('ALL_PIECE') or self.matching_pieces == set([])
    
    def achieve_game_times(self):
        return  get_count(self.uid) + get_game_count_forever(self.uid)== 0
    
    def match_uid(self,gender,match_gender):
        matching_uid=None
        persons = cache.get(gender)
        if not  str(self.pieces) in persons.keys():
            persons[str(self.pieces)]=[self.uid,]
        else:
            if not self.uid in  persons[str(self.pieces)]:
                persons[str(self.pieces)].append(self.uid)
        cache.set(gender,persons)
        if cache.get(match_gender).get(str(self.matching_pieces))==None:
            return None
        matching_uid_list=cache.get(match_gender).get(str(self.matching_pieces))
        for uid in matching_uid_list:
            if not uid in self.recommendList: 
                matching_uid=uid
#                 self.recommendList.append(uid)
#                 FacebookUser.objects.filter(uid=self.uid).update(recommendList=simplejson.dumps(self.recommendList))
        return matching_uid
    
    def get_matching_user(self):
        
#         if  self.gender == 'M':
#             boys = cache.get('BOYS')
#             boys[str(self.pieces)] = self.uid#如果位男性，则将其存入JIGSW_BOYS
#             matching_uid = cache.get('GIRLS').get(str(self.matching_pieces))#从JIGSW_GIRLS中寻找与之互补的异性
#             cache.set('BOYS',boys)
#         else :
#             girls = cache.get('GIRLS')
#             girls[str(self.pieces)] = self.uid
#             matching_uid =  cache.get('BOYS').get(str(self.matching_pieces))
#             cache.set('GIRLS',girls)
            
        if  self.gender == 'M':
            matching_uid=self.match_uid('BOYS','GIRLS')
        else : 
           matching_uid=self.match_uid('GIRLS','BOYS')
           
        user_game_count = cache.get('USER_GAME_COUNT')
        if user_game_count.get(self.uid)==None:
            user_game_count[self.uid] =9
        else:
            if matching_uid != None:
                if  user_game_count.get(self.uid)==0:
                    set_game_count_forever(self.uid,get_game_count_forever(self.uid)-1)
                else:
                    user_game_count[self.uid] = user_game_count.get(self.uid) - 1
        cache.set('USER_GAME_COUNT',user_game_count)
        if matching_uid != None:
            matching_user =FacebookUser.objects.get(uid=matching_uid)
        else :
            return None
        return matching_user
    
    
    def get_match_result(self):
#         if self.data_unavailable() :
#             return {'status_code':cache.get('DATA_UNAVAILABLE')}
        if self.achieve_game_times() :
            return [cache.get('GAME_TIMES_REACH_THE_LIMIT')]
        matching_user = self.get_matching_user()
        pieces = [i for i in self.pieces]
        if matching_user != None :
            username = matching_user.username
            uid=matching_user.uid
            city = matching_user.location
            age = matching_user.age
            avatar = matching_user.avatar
            #获得照片
            from django.core import serializers
            facebookPhotoList = serializers.serialize("json", FacebookPhoto.objects.filter(user_id=uid)[:12])
            
            return [cache.get('MATCH_SUCCESS'),pieces,{'username':username,'city':city,'age':age,'uid':uid,'facebookPhotoList':facebookPhotoList,
                                                       'avatar':avatar,'game_count':cache.get('USER_GAME_COUNT').get(self.uid)+get_game_count_forever(self.uid)}]
        else :  
            return [cache.get('NO_MATCHING_USER'),pieces,{'game_count':cache.get('USER_GAME_COUNT').get(self.uid)+get_game_count_forever(self.uid)}]
        
    def generate_pieces(self):
        import random
        number = random.randint(1,100)
        number=3
        year = int(str(datetime.date.today()).split("-")[0])
        month = int(str(datetime.date.today()).split("-")[1])
        day = int(str(datetime.date.today()).split("-")[2])
        size = day*number%7
        if size == 0:
            size = 6
        base = str(year*year*month*day*number)
        temp = set()
        for i in range(0,size):
            temp.add(int(base[i])%7)
        return  temp

def get_count(uid):
    user_game_count = cache.get('USER_GAME_COUNT')
    if user_game_count.get(uid) == None :
        user_game_count[uid] = cache.get('GAME_TIMES')
        cache.set('USER_GAME_COUNT',user_game_count)
    return cache.get('USER_GAME_COUNT').get(uid)

def set_count(uid,gameCount):
    user_game_count = cache.get('USER_GAME_COUNT')
    user_game_count[uid] = gameCount+user_game_count[uid] 
    cache.set('USER_GAME_COUNT',user_game_count)

def reset_game():
    cache.set('TODAY',datetime.date.today())
    cache.set('GIRLS',{})
    cache.set('BOYS',{})
    cache.set('USER_GAME_COUNT',{})

'''
判断是否被邀请过
''' 
def has_invited(uid,username):
    inviteConfirm= cache.get('CONFIRM_INVITE')
    if inviteConfirm.get(uid) == None :
        return False
    inviteFriends=inviteConfirm.get(uid)
    if username in inviteFriends:
        return True
    else:
        return False
'''
接受索要命的好友
'''
def add_invite_confirm(uid,username):
    inviteConfirm= cache.get('CONFIRM_INVITE')
    if inviteConfirm.get(uid) == None :
        inviteConfirm[uid]=[username,]
    else:
        inviteConfirmFriends=inviteConfirm.get(uid)
        inviteConfirmFriends.append(username)
        inviteConfirm[uid]=inviteConfirmFriends
    cache.set('CONFIRM_INVITE',inviteConfirm)
'''
清空接受索要命的好友列表
'''        
def clear_invite_confirm(uid):
    inviteConfirm= cache.get('CONFIRM_INVITE')
    inviteConfirm[uid]=[]
    cache.set('CONFIRM_INVITE',inviteConfirm)
'''
获取接受索要命的好友列表
'''
def get_invite_confirm_list(uid):
    inviteConfirm= cache.get('CONFIRM_INVITE')
    if not uid in inviteConfirm.keys():
        return []
    else:
        return inviteConfirm.get(uid)
#############facebook###########
def get_invite_count(uid):
    invite_count = cache.get('INVITE_COUNT')
    if invite_count.get(uid) == None :
        invite_count[uid] = 0
        cache.set('INVITE_COUNT',invite_count)
    return cache.get('INVITE_COUNT').get(uid)
def set_invite_count(uid,count):
    invite_count = cache.get('INVITE_COUNT')
    invite_count[uid]=count
    cache.set('INVITE_COUNT',invite_count)
    
def get_game_count_forever(uid):
    user_game_count_forever = cache.get('USER_GAME_COUNT_FOREVE')
    if user_game_count_forever.get(uid) == None :
        user_game_count_forever[uid] = 0
        cache.set('USER_GAME_COUNT_FOREVE',user_game_count_forever)
    return cache.get('USER_GAME_COUNT_FOREVE').get(uid)
def set_game_count_forever(uid,count):
    game_count_forever=cache.get('USER_GAME_COUNT_FOREVE')
    game_count_forever[uid]=count
    cache.set('USER_GAME_COUNT_FOREVE',game_count_forever)

