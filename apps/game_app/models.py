# -*- coding: utf-8 -*-
import datetime

from django.core.cache import cache
from apps.third_party_login_app.models import FacebookUser, FacebookPhoto,\
    FacebookUserInfo
import simplejson
import logging
from apps.user_app.models import UserProfile
from apps.friend_dynamic_app.models import Picture
from django.core import serializers



class Yuanfenjigsaw:
#     selected_pieces_str = ''
    pieces = set()
    matching_pieces = set()
    uid = ''
    gender = ''
    def __init__(self,request):
        if cache.get('TODAY') != datetime.date.today():
            reset_game()
            get_count(request.user.id)
        self.uid = request.REQUEST.get('uid')
        facebookUser=FacebookUser.objects.get(uid=self.uid)
        
#         self.pieces = set([int(i) for i in self.selected_pieces_str.split("-") if i])#用户提交的集合
        self.pieces = self.generate_pieces()
        self.matching_pieces = self.pieces#与之互补的集合
        self.gender = facebookUser.gender
        self.age=facebookUser.age
        self.location=facebookUser.location
        self.noRecommendList=simplejson.loads(facebookUser.noRecommendList)
        self.recommendList=simplejson.loads(facebookUser.recommendList)
        self.filter=request.REQUEST.get('filter')
        #根据学校，学历，地点，匹配结果
        self.filter_match=None
        
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
        matching_uid=self.get_match_user_uid(matching_uid_list)
        return matching_uid
      
        
    '''
    根据cache 中的信息匹配用户数据
    '''
    def get_match_user_uid(self,matching_uid_list):
        matching_uid=None
        filter=False
       
        if self.filter!=None :
          uids=self.noRecommendList
          uids.append(self.uid)
          uidsstr="','".join(uids)
          matching_uid_str="','".join(matching_uid_list)
          if self.filter=='age' or self.filter=='location':
              if self.filter=='age':
                facebookUser=FacebookUser.objects.filter(age=getattr(self,self.filter),uid__in=matching_uid_list).exclude(uid__in=uids)
              if self.filter=='location':
                 facebookUser=FacebookUser.objects.filter(location=getattr(self,self.filter),uid__in=matching_uid_list).exclude(uid__in=uids)
              if len(facebookUser)<=0:
                  filter=matching_uid
              else:
                  self.update_norecommend_list(facebookUser[0].uid)
                  self.filter_match=facebookUser[0].location
                  return facebookUser[0].uid
          elif self.filter=='work' or self.filter=='school':
              #获取学历和工作，并将分别存储的数组中
              facebookUserInfoList=FacebookUserInfo.objects.filter(user_id=self.uid)
              shoolList=[]
              employerList=[]
              for facebookUserInfo in facebookUserInfoList:
                  if facebookUserInfo.type=='school':
                      shoolList.append(facebookUserInfo.name)
                  if  facebookUserInfo.type=='employer':
                      employerList.append(facebookUserInfo.name)
              sql2='''
                      SELECT DISTINCT name from facebook_user_info where user_id=%s
                      '''    
              if self.filter=='work':
                  employerStr=''
                  for employer in employerList:
                      employerStr+=u" name = '"+employer+u"' or"
                  if len(shoolList)>0:
                      employerStr=  '%s%s%s' % (u'and (',employerStr[:len(employerStr)-2],u')')
                      sql='''
          SELECT  distinct u1.user_id as shool_user_id  from facebook_user_info u1 where type=%s '''+employerStr+''' and u1.user_id in( '''+"'"+matching_uid_str+"'"+''' ) and u1.user_id not in ('''+"'"+uidsstr+"'"+''')
group by u1.user_id
ORDER BY  count(u1.user_id) DESC
LIMIT 0,1
'''      
                      sql2+=employerStr
                      from util.connection_db import connection_to_db
                      user_id=connection_to_db(sql,('employer',))
                      if len(user_id)>0:
                          self.update_norecommend_list(user_id[0][0])
                          employers=[employer[0]for employer in connection_to_db(sql2,(user_id[0][0]))]
                          self.filter_match=employers
                          return user_id[0][0]
                      else:
                          return matching_uid
                  else:
                      return matching_uid
              if self.filter=='school':
                  shoolStr=''
                  for shool in shoolList:
                      shoolStr+=u" name ='"+shool+u"' or"
                  if len(shoolList)>0:
                      shoolStr= '%s%s%s' % (u'and (',shoolStr[:len(shoolStr)-2],u')')
                      sql='''
          SELECT  distinct u1.user_id as shool_user_id  from facebook_user_info u1 where type=%s '''+shoolStr+''' and u1.user_id in( '''+"'"+matching_uid_str+"'"+''' ) and u1.user_id not in ('''+"'"+uidsstr+"'"+''')
group by u1.user_id
ORDER BY  count(u1.user_id) DESC
LIMIT 0,1
'''                    
                      sql2+=shoolStr
                      from util.connection_db import connection_to_db
                      user_id=connection_to_db(sql,('school'))
                      if len(user_id)>0:
                          self.update_norecommend_list(user_id[0][0])
                          shools=[shool[0] for shool in connection_to_db(sql2,(user_id[0][0]))]
                          self.filter_match=shools
                          return user_id[0][0]
                      else:
                           return matching_uid
                  else:
                      return matching_uid
                      
        if not filter:
            for uid in matching_uid_list:
                if not uid in self.noRecommendList: 
                    matching_uid=uid
                    self.update_norecommend_list(uid)
                    break;
            return matching_uid
  
    def update_norecommend_list(self,uid):
        self.recommendList.append(uid)
        self.noRecommendList.append(uid)
        FacebookUser.objects.filter(uid=self.uid).update(noRecommendList=simplejson.dumps(self.noRecommendList),recommendList=simplejson.dumps(self.recommendList))
        
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
        #判断筛选条件是否存在
        if self.filter=='age' and self.age==None:
                return [4,'age']
        if self.filter=='location' and self.age==None:
                return [4,'location']
        if self.filter=='school' and (not FacebookUserInfo.objects.filter(user_id=self.uid,type='school').exists()):
                return [4,'education']
        if self.filter=='work' and  (not FacebookUserInfo.objects.filter(user_id=self.uid,type='employer').exists()) :
                return [4,'work']
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
            smallAvatar=matching_user.smallAvatar
            #获得照片
            from django.core import serializers
            facebookPhotoList = serializers.serialize("json", FacebookPhoto.objects.filter(user_id=uid))
            filter_pic='';
            if self.filter=='location' and self.filter_match!=None:
                filter_pic='/static/img/facebook_location.png'
            if self.filter=='school' and self.filter_match!=None:
                filter_pic='/static/img/facebook_school.png'
            if self.filter=='work' and self.filter_match!=None:
                filter_pic='/static/img/facebook_work.png'
            return [cache.get('MATCH_SUCCESS'),pieces,{'username':username,'city':city,'age':age,'uid':uid,'facebookPhotoList':facebookPhotoList,
                                                       'avatar':avatar,'smallAvatar':smallAvatar,'game_count':cache.get('USER_GAME_COUNT').get(self.uid)+get_game_count_forever(self.uid),
                                                       'filter_pic':filter_pic,'filter_match':self.filter_match}]
        else :  
            return [cache.get('NO_MATCHING_USER'),pieces,{'game_count':cache.get('USER_GAME_COUNT').get(self.uid)+get_game_count_forever(self.uid),'filter':self.filter}]
        
    def generate_pieces(self):
        import random
        number = random.randint(1,3)
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


'''
缘分拼图网页版
'''
class YuanfenjigsawWeb:
    pieces = set()
    matching_pieces = set()
    uid = ''
    gender = ''
    def __init__(self,user,**kwargs):
        self.uid =user.id
        userProfile=UserProfile.objects.get(user=user)
        self.pieces = self.generate_pieces()
        self.matching_pieces = self.pieces#与之互补的集合
        self.gender = userProfile.gender
        self.age=userProfile.age
        self.location=userProfile.city
        self.educationSchool=userProfile.educationSchool
        self.educationSchool_2=userProfile.educationSchool_2
        self.recommendList=get_pintu_web_recommendList(self.uid)
        self.jobIndustry=userProfile.jobIndustry
        self.filter=kwargs.pop('filter',None)
        self.type=kwargs.pop('type',None)
        #根据学校，学历，地点，匹配结果
        self.filter_match=None
        
    def generate_pieces(self):
        import random
#         number = random.randint(1,3)
        number = 1
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
    

    def get_match_user_uid(self,matching_uid_list):
        matching_uid=None
        filter=False
       
        if self.filter!=None and self.filter!='all':
          uids=self.recommendList
          uids.append(self.uid)
          if self.filter=='age':
            facebookUser=UserProfile.objects.filter(age=getattr(self,self.filter),user_id__in=matching_uid_list).exclude(user_id__in=uids)
          elif self.filter=='location':
            facebookUser=UserProfile.objects.filter(city=getattr(self,self.filter),user_id__in=matching_uid_list).exclude(user_id__in=uids)
          elif self.filter=='work':
              facebookUser=UserProfile.objects.filter(jobIndustry=getattr(self,self.filter),user_id__in=matching_uid_list).exclude(user_id__in=uids)
          elif self.filter=='school':
              facebookUser=UserProfile.objects.filter(educationSchool=getattr(self,'educationSchool'),user_id__in=matching_uid_list).exclude(user_id__in=uids)
          if len(facebookUser)<=0:
            filter=matching_uid
          else:
             set_pintu_web_recommendList(facebookUser[0].uid)
             self.filter_match=facebookUser[0].city
             return facebookUser[0].user_id
    
                      
        if not filter:
            for uid in matching_uid_list:
               if not uid in self.recommendList: 
                    matching_uid=uid
                    set_pintu_web_recommendList(self.uid,uid)
                    break;
            return matching_uid
        
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
        matching_uid=self.get_match_user_uid(matching_uid_list)
        return matching_uid
    
    def get_matching_user(self):
        if  self.gender == 'M':
            matching_uid=self.match_uid('WEB_BOYS','WEB_GIRLS')
        else : 
           matching_uid=self.match_uid('WEB_GIRLS','WEB_BOYS')
        if matching_uid != None:
            matching_user =UserProfile.objects.select_related('user').get(user_id=matching_uid)
        else :
            return None
        return matching_user
    
    def score_and_PLprice_for_pintu(self):
        self.type ='score'
        if self.type =='score':
            from apps.user_score_app.method import use_score_by_pintu
            return use_score_by_pintu(self.uid)
        elif self.type =='charge':
            from apps.pay_app.method import use_charge_by_pintu
            return use_charge_by_pintu(self.uid)
        else:
            return 'error'
    def get_match_result(self):
         
#         if self.data_unavailable() :
#             return {'status_code':cache.get('DATA_UNAVAILABLE')}
        #判断筛选条件是否存在
        if self.filter=='age' and self.age==None:
                return [4,'age']
        if self.filter=='location' and self.age==None:
                return [4,'location']
        if self.filter=='school' and (self.educationSchool==None ):
                return [4,'education']
        if self.filter=='work' and self.jobIndustry==None :
                return [4,'work']
        matching_user = self.get_matching_user()
        pieces = [i for i in self.pieces]
        if matching_user != None :
            buy=self.score_and_PLprice_for_pintu()
            if buy=='less':
                return 'less'
            elif buy=='error':
                return 'error'
            username = matching_user.user.username
            uid=matching_user.user.id
            city = matching_user.city
            age = matching_user.age
            avatar = matching_user.get_avatar_image()
            filter_pic='';
            if self.filter=='location' and self.filter_match!=None:
                filter_pic='/static/img/facebook_location.png'
            if self.filter=='school' and self.filter_match!=None:
                filter_pic='/static/img/facebook_school.png'
            if self.filter=='work' and self.filter_match!=None:
                filter_pic='/static/img/facebook_work.png'
            
            from apps.pay_app.method import get_charge_amount
            game_count=get_charge_amount(self.uid)
            from apps.pojo.card import userProfileList_to_CardList
            card=userProfileList_to_CardList(self.uid,[matching_user,])[0]
            from apps.pojo.card import MyEncoder
            card=simplejson.dumps(card,cls=MyEncoder)
            return [cache.get('MATCH_SUCCESS'),pieces,{'username':username,'city':city,'age':age,'uid':uid,'game_count':game_count,
                                                       'avatar':avatar,'filter_pic':filter_pic,'filter_match':self.filter_match,"card":card}]
        else :  
            return [cache.get('NO_MATCHING_USER'),pieces,{'filter':self.filter}]


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
#     cache.set('GIRLS',{})
#     cache.set('BOYS',{})
    cache.set('USER_GAME_COUNT',{})
    cache.set('INVITE_IN_DAY',{})

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
uid  
confirmUid 给你送心的好友Uid
'''
def add_invite_confirm(uid,confirmUid):
    inviteConfirm= cache.get('CONFIRM_INVITE')
    if inviteConfirm.get(uid) == None :
        inviteConfirm[uid]=[confirmUid,]
    else:
        inviteConfirmFriends=inviteConfirm.get(uid)
        inviteConfirmFriends.append(confirmUid)
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
        inviteConfirmList=inviteConfirm.get(uid)
        facebookUserList=FacebookUser.objects.filter(uid__in=inviteConfirmList)
        from util.util import model_to_dict
        return model_to_dict(facebookUserList,fields=['uid','username','avatar','gender','location','age'])
'''
一天之内受过邀请的好友uid
'''   
def get_invite_in_day(uid):
    inviteInDay=cache.get('INVITE_IN_DAY')
    if not uid in inviteInDay.keys():
        return []
    else:
        inviteInDayList=inviteInDay.get(uid)
        return inviteInDayList

def add_invite_in_day(uid,inviteUid):         
    inviteInDay= cache.get('INVITE_IN_DAY')
    if inviteInDay.get(uid) == None :
        inviteInDay[uid]=[inviteUid,]
    else:
        inviteInDays=inviteInDay.get(uid)
        inviteInDays.append(inviteUid)
        inviteInDay[uid]=inviteInDays
    cache.set('INVITE_IN_DAY',inviteInDay)
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

'''
获取历史记录返回字典列表
'''
def get_recommend_history(uid):
    recommendHistoryList=simplejson.loads(FacebookUser.objects.get(uid=uid).recommendList)
    facebookUserList=FacebookUser.objects.filter(uid__in=recommendHistoryList)
    from util.util import model_to_dict
    facebookUserListTemp=model_to_dict(facebookUserList, fields=['uid','username','smallAvatar','location','age','link'])
    facebookUserListDcit=[]
    for recommendUid in reversed(recommendHistoryList):
        for user in facebookUserListTemp:
            if user.get('uid')==recommendUid:
                facebookUserListDcit.append(user)
    return facebookUserListDcit



'''
获取历史记录返回字典列表web版
'''
def get_recommend_history_web(uid):
    recommendHistoryList=get_pintu_web_recommendList(uid)
    userProfileList=UserProfile.objects.select_related('user').filter(user_id__in=recommendHistoryList)
    from util.util import model_to_dict
    facebookUserListTemp=model_to_dict(userProfileList, fields=['user_id','user.username','avatar_name','city','age','avatar_name_status'])
    return facebookUserListTemp


'''

获得拼图微博版的已经推荐过的列表
    attridute:
          uid 用户id
'''
def get_pintu_web_recommendList(uid):
    recommendDict=cache.get('PINTU_WEB_RECOMMEND',False)
    if recommendDict:
        return recommendDict.get(uid,[])
    else:
        return []
        
'''
插入拼图微博版的已经推荐过的列表
attridute:
        uid 用户id
'''
def set_pintu_web_recommendList(uid,ouid):
    recommendDict=cache.get('PINTU_WEB_RECOMMEND',False)
    if recommendDict:
        if recommendDict.get(uid,None) is None:
             recommendDict[uid]=[ouid]
        else:
            recommendDict[uid].append(ouid)
    else:
        recommendDict={}
        recommendDict[uid]=[ouid]
    cache.set('PINTU_WEB_RECOMMEND',recommendDict)