# -*- coding: utf-8 -*-
'''
Created on 2014年11月20日

@author: jin
'''
'''
我心游戏期望甚高计算
@param gender:用户性别
@param best_height:最佳身高
@return: 得分列表  
'''
def cal_expect_height_in_game(gender,best_heght):
    scoreList=[]
    heightDict={u'M':[155,195],u'F':[160,200]}
    heightList=heightDict[gender]
    for height in range(heightList[0],heightList[1],5):
        scoreList.append(100-abs(best_heght-height)*2)
    return scoreList
   
'''
计算权重
''' 
def cal_weight_in_game(kwargs):
    weightSum=0.0
    for key in kwargs.keys():
        weightSum+=kwargs[key]
    for key in kwargs.keys():
        kwargs[key]=(kwargs[key]/weightSum)
    return kwargs

'''
计算学历
'''
def cal_eduction_in_game(eduction,schoolType,country):
        eductionList=[50,60,70,80,90]
        if eduction>=2:
          if country==0:
            if schoolType<0:
                return eductionList[eduction]
            elif schoolType<=4:
                scroe=eductionList[eduction]+schoolType*5
                scroe=100 if scroe>=100 else scroe
                return scroe
            else:
                raise Exception('学校类型填写错误')
          elif country==1:
                scroe=eductionList[eduction]
                if schoolType<=20:
                    scroe=scroe+(30-schoolType)
                elif schoolType>20 and  schoolType<=100:
                    score=scroe+10
                elif schoolType>100 and schoolType<=200:
                    score=scroe+5
                elif schoolType>200 and schoolType<=300: 
                    score=scroe+2
                scroe=100 if scroe>=100 else scroe
                return scroe
          else:
                raise Exception('国家填写错误')
        else:
            return eductionList[eduction]
        

    
    
'''
判断能不能分享
'''
def has_share_in_game(userId):
    from util.cache import has_recommend,get_has_recommend
    for field in ['grade','userExpect','tag']:
        has_recommend(userId,field)
    if get_has_recommend(userId): 
        return True
    else:
        return False