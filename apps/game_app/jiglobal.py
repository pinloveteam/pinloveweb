#-*- coding: UTF-8 -*- 
import datetime
GAME_TIMES = 10 #游戏可玩次数
ALL_PIECE = set([0,1,2,3,4,5,6,7,8,9])
GIRLS = {} #存放girl数据
BOYS = {}  #存放boy数据
USER_GAME_COUNT = {} #用户游戏次数
TODAY = datetime.date.today()

NO_MATCHING_USER = "0"
DATA_UNAVAILABLE = "1"
GAME_TIMES_REACH_THE_LIMIT = "2"
MATCH_SUCCESS = "3"

print '\xe5\xae\xa1\xe6\xa0\xb8\xe6\x9c\xaa\xe9\x80\x9a\xe8\xbf\x87'.decode('utf-8')