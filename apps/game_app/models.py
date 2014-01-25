# -*- coding: utf-8 -*-
from apps.user_app.models import UserProfile
import datetime

from django.contrib.auth.models import User
from django.core.cache import cache
from apps.third_party_login_app.models import FacebookUser

class Yuanfenjigsaw:
#     selected_pieces_str = ''
    pieces = set()
    matching_pieces = set()
    current_username = ''
    gender = ''
    number = 0; 
    def __init__(self,request):
        if cache.get('TODAY') != datetime.date.today():
            reset_game()
            get_count(request)
        uid=request.GET.get('uid')
        facebookUser=FacebookUser.objects.get(uid=uid)
        self.current_username = facebookUser.username
        self.number=int(request.GET.get("number",''))
#         self.pieces = set([int(i) for i in self.selected_pieces_str.split("-") if i])#用户提交的集合
        self.pieces = self.generate_pieces()
        self.matching_pieces = self.pieces#与之互补的集合
        self.gender = facebookUser.gender
        
#     def data_unavailable(self):
#         return  self.pieces - cache.get('ALL_PIECE') != set([]) or self.matching_pieces ==  cache.get('ALL_PIECE') or self.matching_pieces == set([])
    
    def achieve_game_times(self):
        return  cache.get('USER_GAME_COUNT').get(self.current_username) == 0
    
    def get_matching_user(self):
        user_game_count = cache.get('USER_GAME_COUNT')
        if user_game_count.get(self.current_username)==None:
            user_game_count[self.current_username] =9
        else:
            user_game_count[self.current_username] = user_game_count.get(self.current_username) - 1
        cache.set('USER_GAME_COUNT',user_game_count)
        if  self.gender == 'M':
            boys = cache.get('BOYS')
            boys[str(self.pieces)] = self.current_username#如果位男性，则将其存入JIGSW_BOYS
            matching_username = cache.get('GIRLS').get(str(self.matching_pieces))#从JIGSW_GIRLS中寻找与之互补的异性
            cache.set('BOYS',boys)
        else :
            girls = cache.get('GIRLS')
            girls[str(self.pieces)] = self.current_username
            matching_username =  cache.get('BOYS').get(str(self.matching_pieces))
            cache.set('GIRLS',girls)
            
        if matching_username != None:
            matching_user =FacebookUser.objects.filter(username=matching_username)
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
#             city = matching_user.city
#             age = matching_user.age
#             avatar_name = matching_user.avatar_name
            city = 'ttt'
            age = '22'
            avatar_name = 'matching_user.avatar_name'
#             return {'status_code':jiglobal.MATCH_SUCCESS,'username':matching_user.user.username,'count':jiglobal.USER_GAME_COUNT.get(self.current_username)}
            return [cache.get('MATCH_SUCCESS'),pieces,username,city,age,avatar_name,cache.get('USER_GAME_COUNT').get(self.current_username)]
        else :  
            return [cache.get('NO_MATCHING_USER'),pieces,cache.get('USER_GAME_COUNT').get(self.current_username)]
        
    def generate_pieces(self):
        year = int(str(datetime.date.today()).split("-")[0])
        month = int(str(datetime.date.today()).split("-")[1])
        day = int(str(datetime.date.today()).split("-")[2])
        size = day*self.number%7
        if size == 0:
            size = 6
        base = str(year*year*month*day*self.number)
        temp = set()
        for i in range(0,size):
            temp.add(int(base[i])%7)
        return  temp

def get_count(request):
    current_username = request.user.username
    user_game_count = cache.get('USER_GAME_COUNT')
    if user_game_count.get(current_username) == None :
        user_game_count[current_username] = cache.get('GAME_TIMES')
        cache.set('USER_GAME_COUNT',user_game_count)
    return cache.get('USER_GAME_COUNT').get(current_username)

def reset_game():
    cache.set('TODAY',datetime.date.today())
    cache.set('GIRLS',{})
    cache.set('BOYS',{})
    cache.set('USER_GAME_COUNT',{})
    

