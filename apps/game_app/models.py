# -*- coding: utf-8 -*-
from apps.user_app.models import UserProfile
from apps.game_app import jiglobal
import datetime
from django.contrib.auth.models import User

class Yuanfenjigsaw:
    selected_pieces_str = ''
    selected_pieces = set()
    matching_pieces = set()
    current_username = ''
    gender = ''
        
    def __init__(self,request):
        if jiglobal.TODAY != datetime.date.today():
            reset_game()
            
        self.current_username = request.user.username
        self.selected_pieces_str=request.POST.get("selectedPieces",'')
        self.selected_pieces = set([int(i) for i in self.selected_pieces_str.split("-") if i])#用户提交的集合
        self.matching_pieces =  jiglobal.ALL_PIECE - self.selected_pieces#与之互补的集合
        self.gender = UserProfile.objects.get(user=request.user).gender
        
    def data_unavailable(self):
        return  self.selected_pieces - jiglobal.ALL_PIECE != set([]) or self.matching_pieces ==  jiglobal.ALL_PIECE or self.matching_pieces == set([])
    
    def achieve_game_times(self):
        return  jiglobal.USER_GAME_COUNT.get(self.current_username) == 0

    def get_matching_user(self):
        jiglobal.USER_GAME_COUNT[self.current_username] = jiglobal.USER_GAME_COUNT.get(self.current_username) - 1
        if  self.gender == 'M':
            jiglobal.BOYS[str(self.selected_pieces)] = self.current_username#如果位男性，则将其存入JIGSW_BOYS
            matching_username = jiglobal.GIRLS.get(str(self.matching_pieces))#从JIGSW_GIRLS中寻找与之互补的异性
        else :
            jiglobal.GIRLS[str(self.selected_pieces)] = self.current_username#同上
            matching_username =  jiglobal.BOYS.get(str(self.matching_pieces))
            
        if matching_username != None:
            matching_user = UserProfile.objects.get(user=User.objects.get(username=matching_username))  
        else :
            return None
        return matching_user
    
    def get_match_result(self):
        if self.data_unavailable() :
            return {'status_code':jiglobal.DATA_UNAVAILABLE}
        if self.achieve_game_times() :
            return {'status_code':jiglobal.GAME_TIMES_REACH_THE_LIMIT}
        matching_user = self.get_matching_user()
        if matching_user != None :
#             return {'status_code':jiglobal.MATCH_SUCCESS,'matching_user':matching_user,'count':jiglobal.USER_GAME_COUNT.get(self.current_username)}
            return [{'status_code':jiglobal.MATCH_SUCCESS,'username':matching_user.username,'height':matching_user.height,'age':matching_user.age,'avatar_name':matching_user.avatar_name,'count':jiglobal.USER_GAME_COUNT.get(self.current_username)}]
        else :  
            return {'status_code':jiglobal.NO_MATCHING_USER,'count':jiglobal.USER_GAME_COUNT.get(self.current_username)}
        
def get_count(request):
    current_username = request.user.username
    if jiglobal.USER_GAME_COUNT.get(current_username) == None :
        jiglobal.USER_GAME_COUNT[current_username] = jiglobal.GAME_TIMES
    return jiglobal.USER_GAME_COUNT.get(current_username)

def reset_game():
    jiglobal.GIRLS = {}
    jiglobal.BOYS = {} 
    jiglobal.USER_GAME_COUNT = {} 
    jiglobal.TODAY = datetime.date.today()
