# -*- coding: utf-8 -*-
from apps.user_app.models import UserProfile
import datetime

from django.contrib.auth.models import User
from django.core.cache import cache

class Yuanfenjigsaw:
    selected_pieces_str = ''
    selected_pieces = set()
    matching_pieces = set()
    current_username = ''
    gender = ''
       
    def __init__(self,request):
        if cache.get('TODAY') != datetime.date.today():
            reset_game()
            
        self.current_username = request.user.username
        self.selected_pieces_str=request.GET.get("selectedPieces",'')
        self.selected_pieces = set([int(i) for i in self.selected_pieces_str.split("-") if i])#用户提交的集合
        self.matching_pieces =  cache.get('ALL_PIECE') - self.selected_pieces#与之互补的集合
        self.gender = UserProfile.objects.get(user=request.user).gender
        
    def data_unavailable(self):
        return  self.selected_pieces - cache.get('ALL_PIECE') != set([]) or self.matching_pieces ==  cache.get('ALL_PIECE') or self.matching_pieces == set([])
    
    def achieve_game_times(self):
        return  cache.get('USER_GAME_COUNT').get(self.current_username) == 0
    
    def get_matching_user(self):
        user_game_count = cache.get('USER_GAME_COUNT')
        user_game_count[self.current_username] = user_game_count.get(self.current_username) - 1
        cache.set('USER_GAME_COUNT',user_game_count)
        if  self.gender == 'M':
            boys = cache.get('BOYS')
            boys[str(self.selected_pieces)] = self.current_username#如果位男性，则将其存入JIGSW_BOYS
            matching_username = cache.get('GIRLS').get(str(self.matching_pieces))#从JIGSW_GIRLS中寻找与之互补的异性
            cache.set('BOYS',boys)
        else :
            girls = cache.get('GIRLS')
            girls[str(self.selected_pieces)] = self.current_username
            matching_username =  cache.get('BOYS').get(str(self.matching_pieces))
            cache.set('GIRLS',girls)
            
        if matching_username != None:
            matching_user = UserProfile.objects.get(user=User.objects.get(username=matching_username))  
        else :
            return None
        return matching_user
    
    def get_match_result(self):
        if self.data_unavailable() :
            return {'status_code':cache.get('DATA_UNAVAILABLE')}
        if self.achieve_game_times() :
            return {'status_code':cache.get('GAME_TIMES_REACH_THE_LIMIT'),'count':0}
        matching_user = self.get_matching_user()
        if matching_user != None :
#             return {'status_code':jiglobal.MATCH_SUCCESS,'username':matching_user.user.username,'count':jiglobal.USER_GAME_COUNT.get(self.current_username)}
            return {'status_code':cache.get('MATCH_SUCCESS'),'username':matching_user.user.username,'city':matching_user.city,'age':matching_user.age,'avatar_name':matching_user.avatar_name,'count':cache.get('USER_GAME_COUNT').get(self.current_username)}
        else :  
            return {'status_code':cache.get('NO_MATCHING_USER'),'count':cache.get('USER_GAME_COUNT').get(self.current_username)}
        
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
