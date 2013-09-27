# -*- coding: utf-8 -*-
'''
Created on Aug 31, 2013

@author: jin
'''
import MySQLdb
from time import clock as now
from django.contrib import auth
from django.contrib.auth.models import User
from apps.recommend_app.models import Grade, run_procedure,\
     MatchResult, UserExpect
import random
from apps.user_app.models import UserProfile
from apps.recommend_app.recommend_util import cal_income, cal_education
from pinloveweb import settings
from apps.common_app.models import School
connection = MySQLdb.connect(user='root', db='django', passwd='jin521436', host='localhost')
cursor=connection.cursor();
start = now()
arr = [[0]*100001 for row in range(3)]
list=[0.000]*100001
# school=School.objects.all()
# user_basic_profile(user_id=1,gender='M',height=random.randint(155,200),education=random.randint(0,4),
#                        educationSchool=school[random.randint(1,600)].name,income=random.randint(5,100),).save()
# User_Expect(user_id=1,heighty1=random.randint(1,100),heighty2=random.randint(1,100),heighty3=random.randint(1,100),heighty4=random.randint(1,100),heighty5=random.randint(1,100),
#                 heighty6=random.randint(1,100),heighty7=random.randint(1,100),heighty8=random.randint(1,100),).save()
# g=grade(user_id=1,heightweight=random.uniform(0,1),incomescore=random.uniform(0,1),incomeweight=random.uniform(0,1),
#             edcationscore=random.uniform(0,1),edcationweight=random.uniform(0,1),appearancescore=random.uniform(0,1),appearanceweight=random.uniform(0,1)).save()
# for i in range(3,50):
#     user1=User(username=str(i),)
#     user1.set_password('112233')
#     user1.save()
#     user_basic_profile(user_id=i,gender='M',height=random.randint(155,200),education=random.randint(0,4),
#                        educationSchool=school[random.randint(1,600)].name,income=random.randint(5,100),).save()
#     User_Expect(user_id=i,heighty1=random.randint(1,100),heighty2=random.randint(1,100),heighty3=random.randint(1,100),heighty4=random.randint(1,100),heighty5=random.randint(1,100),
#                 heighty6=random.randint(1,100),heighty7=random.randint(1,100),heighty8=random.randint(1,100),).save()
#     g=grade(user_id=i,heightweight=random.uniform(0,1),incomescore=random.uniform(0,1),incomeweight=random.uniform(0,1),
#             edcationscore=random.uniform(0,1),edcationweight=random.uniform(0,1),appearancescore=random.uniform(0,1),appearanceweight=random.uniform(0,1)).save()
# for i in range(55,100):
#     user1=User(username=str(i),)
#     user1.set_password('112233')
#     user1.save()
#      user_basic_profile(user_id=i,gender='F',height=random.randint(155,200),education=random.randint(0,4),
#                          educationSchool=school[random.randint(1,500)].name,income=random.randint(5,100),).save()
#                        educationSchool=school[random.randint(1,600)].name,income=random.randint(5,100),).save()
#     User_Expect(user_id=i,heighty1=random.randint(1,100),heighty2=random.randint(1,100),heighty3=random.randint(1,100),heighty4=random.randint(1,100),heighty5=random.randint(1,100),
#                 heighty6=random.randint(1,100),heighty7=random.randint(1,100),heighty8=random.randint(1,100),).save()
#     g=grade(user_id=i,heightweight=random.uniform(0,1),incomescore=random.uniform(0,1),incomeweight=random.uniform(0,1),
#             edcationscore=random.uniform(0,1),edcationweight=random.uniform(0,1),appearancescore=random.uniform(0,1),appearanceweight=random.uniform(0,1)).save()
# gradelist=grade.objects.filter()
# jin=grade.objects.get(user_id=1)
# j=0
# for i in gradelist:
#     score1=(jin.heightweight*i.incomescore+jin.incomescore*i.incomeweight+jin.edcationscore*i.edcationweight+jin.appearancescore*i.appearanceweight)*100;
#     if score1>200:
#         score2=(i.heightweight*jin.incomescore+i.incomescore*jin.incomeweight+i.edcationscore*jin.edcationweight+i.appearancescore*jin.appearanceweight)*100;
#         print str(score2)+" "+str(score1)
#         if score2>200:
#              arr[3][j]=i.user_id
#              arr[0][j]=score1
#              arr[1][j]=score2
#     j+=1
# j=0
# for i in range(len(arr[0])):    
#     if abs(arr[0][i]-arr[1][i]) <40:
#         list[j]=arr[0][i]+arr[1][i]
#         j+=1
# print gradelist[0]

######掉用procedure
# r=cursor.callproc('recommend',(8,))
# result=cursor.fetchall()
#   
# connection.commit()
# cursor.close()
# matchResult.objects.filter(id=10).delete()
# run_procedure(10)
# print r,result
# macth=matchResult.objects.filter(my_id=10)
# for i in macth:
#     print i.get_user_basic_profile().get_income_display()
# tupe=(r'北京大学',r'清华大学',r'复旦大学',r'浙江大学',r'上海交通大学',r'南京大学',r'中山大学',r'吉林大学',r'武汉大学',r'中国科技大学',r'华中科技大学',r'中国人民大学',r'四川大学',r'南开大学',r'山东大学',r'北京师范大学',r'哈尔滨工业大学',r'西安交通大学',r'中南大学',r'厦门大学',r'东南大学',r'同济大学',r'天津大学',r'北京航空航天大学',r'大连理工大学',r'华东师范大学',r'华南理工大学',r'中国农业大学',r'湖南大学',r'兰州大学',r'重庆大学',r'西北工业大学',r'东北大学',r'北京理工大学',r'华东理工大学',r'北京协和医学院',r'东北师范大学',r'北京科技大学',r'中国地质大学',r'武汉理工大学',r'华中师范大学',r'西北大学',r'中国矿业大学',r'华中农业大学',r'电子科技大学',r'长安大学',r'东华大学',r'西南大学',r'中国海洋大学',r'南京航空航天大学',r'南京理工大学',r'西南交通大学',r'北京交通大学',r'苏州大学',r'中国石油大学',r'云南大学',r'北京化工大学',r'西安电子科技大学',r'南京农业大学',r'西北农林科技大学',r'南京师范大学',r'上海大学',r'郑州大学',r'河海大学',r'北京邮电大学',r'哈尔滨工程大学',r'合肥工业大学',r'湖南师范大学',r'暨南大学',r'福州大学',r'南昌大学',r'北京林业大学',r'北京工业大学',r'华南师范大学',r'陕西师范大学',r'江南大学',r'华南农业大学',r'首都医科大学',r'中国政法大学',r'新疆大学',r'广西大学',r'内蒙古大学',r'华北电力大学',r'上海财经大学',r'中央民族大学',r'南京医科大学',r'山西大学',r'河南大学',r'太原理工大学',r'中南财经政法大学',r'安徽大学',r'南方医科大学',r'湘潭大学',r'贵州大学',r'哈尔滨医科大学',r'南京工业大学',r'燕山大学',r'浙江工业大学',r'东北林业大学',r'辽宁大学',\
# '昆明理工大学','扬州大学','中国医科大学','中央财经大学','海南大学','江苏大学','西南财经大学','首都师范大学','宁夏大学','对外经济贸易大学','天津医科大学','北京中医药大学','福建师范大学','黑龙江大学','山东师范大学','上海师范大学','深圳大学','山东农业大学','西南政法大学','四川农业大学','重庆医科大学','西北师范大学','中国药科大学','河北大学','北京外国语大学','东北农业大学','河北工业大学','安徽师范大学','石河子大学','延边大学','东北财经大学','天津师范大学','大连海事大学','浙江师范大学','青岛科技大学','上海理工大学','西安建筑科技大学','湖南农业大学','内蒙古农业大学','宁波大学','广州中医药大学','青岛大学','湖北大学','福建农林大学','山东科技大学','西安理工大学','上海外国语大学','武汉科技大学','沈阳农业大学','上海中医药大学','河南师范大学','汕头大学','青海大学','西藏大学','江西师范大学','长沙理工大学','成都理工大学','河北师范大学','广西师范大学','云南师范大学','安徽医科大学','天津工业大学','兰州交通大学','兰州理工大学','南京林业大学','华侨大学','江西农业大学','浙江理工大学','长春理工大学','辽宁师范大学','河南理工大学','中北大学','东北石油大学','哈尔滨理工大学','河北农业大学','河北医科大学','江西财经大学','温州医学院','广东工业大学','天津中医药大学','云南农业大学','沈阳工业大学','沈阳药科大学','辽宁工程技术大学','安徽农业大学','哈尔滨师范大学','南京信息工程大学','西南石油大学','广州大学','南京邮电大学','首都经济贸易大学','成都中医药大学','新疆医科大学','河南农业大学','南京中医药大学','杭州师范大学','四川师范大学','浙江工商大学','曲阜师范大学','广西医科大学','辽宁大学',\
# '西南科技大学','广州医学院','江苏师范大学','华东政法大学','天津财经大学','中南林业科技大学','桂林理工大学','杭州电子科技大学','吉林农业大学','湖南科技大学','山西师范大学','济南大学','内蒙古师范大学','南华大学','重庆交通大学','福建医科大学','山西医科大学','上海海事大学','江西理工大学','山西农业大学','新疆农业大学','安徽理工大学','大连医科大学','河南科技大学','甘肃农业大学','广东外语外贸大学','景德镇陶瓷学院','温州大学','西安科技大学','北京语言大学','贵州师范大学','华东交通大学','天津科技大学','东华理工大学','河南工业大学','青岛理工大学','长江大学','陕西科技大学','北京工商大学','山东理工大学','天津理工大学','南通大学','三峡大学','山东中医药大学','中南民族大学','重庆师范大学','上海海洋大学','中国计量学院','河北科技大学','黑龙江中医药大学','内蒙古科技大学','宁夏医科大学','烟台大学','安徽工业大学','桂林电子科技大学','湖南中医药大学','石家庄铁道大学','常州大学','浙江农林大学','聊城大学','南昌航空大学','新疆师范大学','重庆邮电大学','内蒙古工业大学','青海师范大学','太原科技大学','武汉纺织大学','武汉工程大学','沈阳师范大学','东北电力大学','河北联合大学','昆明医科大学','西南民族大学','中国民航大学','重庆工商大学','重庆理工大学','浙江中医药大学','贵阳医学院','青岛农业大学','云南民族大学','国际关系学院','黑龙江八一农垦大学','西安石油大学','湖北中医药大学','集美大学','西北民族大学','西华师范大学','北京建筑工程学院','吉林师范大学','西北政法大学','云南财经大学','大连交通大学','广西民族大学','海南师范大学','江西中医学院','大连工业大学','福建中医药大学','辽宁科技大学','塔里木大学','外交学院',\
# '西华大学','浙江财经学院','安徽财经大学','大连大学','湖北工业大学','湖南工业大学','辽宁中医药大学','山东建筑大学','山西财经大学','沈阳航空航天大学','沈阳建筑大学','西安工业大学','长春工业大学','河南财经政法大学','佳木斯大学','江苏科技大学','渤海大学','哈尔滨商业大学','吉首大学','鲁东大学','南京财经大学','青海民族大学','山东财经大学','山东轻工业学院','西安工程大学','郑州轻工业学院','安徽中医学院','河北经贸大学','上海工程技术大学','西南林业大学','广东医学院','华北水利水电学院','武汉工业学院','遵义医学院','北方工业大学','广西中医药大学','齐齐哈尔大学','河南中医学院','泸州医学院','内蒙古民族大学','天津商业大学','北华大学','广东商学院','绍兴文理学院','徐州医学院','延安大学','北京第二外国语学院','长春中医药大学','大连民族学院','广东药学院','内蒙古医科大学','四川外语学院','西藏民族学院','浙江海洋学院','甘肃中医学院','贵州财经大学','贵州民族大学','沈阳大学','中国人民公安大学','安徽建筑工业学院','沈阳化工大学','天津城市建设学院','中原工学院','北方民族大学','广西师范学院','湖南商学院','淮北师范大学','辽宁医学院','苏州科技学院','中国青年政治学院','北京联合大学','赣南师范学院','广西工学院','辽宁石油化工大学','潍坊医学院','新乡医学院','安徽工程大学','北京信息科技大学','湖州师范学院','吉林财经大学','吉林化工学院','洛阳师范学院','山东工商学院','上海电力学院','上海对外贸易学院','沈阳理工大学','信阳师范学院','大理学院','大连外国语学院','广东海洋大学','贵阳中医学院','桂林医学院','黑龙江科技学院','南京审计学院','泰山医学院','西安邮电大学','西藏藏医学院','新疆财经大学','安庆师范学院','蚌埠医学院',\
# '重庆科技学院','重庆三峡学院','安阳师范学院','常熟理工学院','合肥师范学院','湖北师范学院','九江学院','南京工程学院','山西中医学院','上海金融学院','邵阳学院','皖西学院','五邑大学','盐城师范学院','伊犁师范学院','浙江科技学院','东莞理工学院','福建工程学院','赣南医学院','广东金融学院','湖南科技学院','金陵科技学院','南阳师范学院','陕西理工学院','上海第二工业大学','四川理工学院','天津农学院','天水师范学院','厦门理工学院','湘南学院','浙江万里学院','宝鸡文理学院','北京电子科技学院','北京石油化工学院','长江师范学院','长沙学院','广东技术师范学院','贵阳学院','河西学院','红河学院','湖南城市学院','湖南工程学院','湖南人文科技学院','怀化学院','惠州学院','济宁医学院','喀什师范学院','兰州城市学院','绵阳师范学院','重庆科技学院','重庆三峡学院','安阳师范学院','常熟理工学院','合肥师范学院','湖北师范学院','九江学院','南京工程学院','山西中医学院','上海金融学院','邵阳学院','皖西学院','五邑大学','盐城师范学院','伊犁师范学院','浙江科技学院','东莞理工学院','福建工程学院','赣南医学院','广东金融学院','湖南科技学院','金陵科技学院','南阳师范学院','陕西理工学院','上海第二工业大学','四川理工学院','天津农学院','天水师范学院','厦门理工学院','湘南学院','浙江万里学院','宝鸡文理学院','北京电子科技学院','北京石油化工学院','长江师范学院','长沙学院','广东技术师范学院','贵阳学院','河西学院','红河学院','湖南城市学院','湖南工程学院','湖南人文科技学院','怀化学院','惠州学院','济宁医学院','喀什师范学院','兰州城市学院','绵阳师范学院',\
# '南昌工程学院','曲靖师范学院','山西大同大学','上海立信会计学院','韶关学院','沈阳医学院','台州学院','右江民族医学院','湛江师范学院','中国劳动关系学院','安康学院','北华航天工业学院','北京物资学院','长春工程学院','成都医学院','赤峰学院','德州学院','佛山科学技术学院','甘肃民族师范学院','贵州师范学院','合肥学院','湖北科技学院','湖北文理学院','淮海工学院','淮阴工学院','黄冈师范学院','吉林医药学院','闽江学院','南京晓庄学院','山东交通学院','上海电机学院','上海政法学院','石家庄学院','太原师范学院','铜陵学院','潍坊学院','渭南师范学院','西昌学院','盐城工学院','宜宾学院','玉林师范学院','运城学院','中国民用航空飞行学院','中国刑事警察学院','中华女子学院','安徽科技学院','安顺学院','百色学院','毕节学院','滨州学院','长春大学','长治医学院','成都学院','承德医学院','大庆师范学院','韩山师范学院','河北北方学院','河北科技师范学院','河池学院','湖北理工学院','湖北汽车工业学院','湖南第一师范学院','淮南师范学院','吉林农业科技学院','集宁师范学院','晋中学院','凯里学院','廊坊师范学院','陇东学院','牡丹江医学院','齐齐哈尔医学院','黔南民族师范学院','泉州师范学院','上海海关学院','上饶师范学院','沈阳工程学院','四川文理学院','宿州学院','通化师范学院','西安文理学院','西安医学院','徐州工程学院','许昌学院','宜春学院','玉溪师范学院','云南警官学院','肇庆学院','中国人民武装警察部队学院','遵义师范学院','安阳工学院','鞍山师范学院','白城师范学院','保山学院','北京警察学院','昌吉学院','长治学院','巢湖学院','成都工业学院','池州学院','滁州学院',)
#独立学院
# tupe=('华中科技大学武昌分校','华中科技大学文华学院','吉林大学珠海学院','浙江大学城市学院','四川大学锦江学院','云南师范大学商学院','燕山大学里仁学院','武汉科技大学城市学院','北京师范大学珠海分校','河南理工大学万方科技学院','浙江大学宁波理工学院','西南财经大学天府学院','南京大学金陵学院','电子科技大学成都学院','厦门大学嘉庚学院','四川大学锦城学院','河北大学工商学院','电子科技大学中山学院','华南理工大学广州学院','中山大学南方学院','山西大学商务学院','长春理工大学光电信息学院','北京理工大学珠海学院','西安交通大学城市学院','中国传媒大学南广学院','大连理工大学城市学院','天津大学仁爱学院','武汉理工大学华夏学院','南开大学滨海学院','东南大学成贤学院','云南大学滇池学院','武汉大学珞珈学院','西南大学育才学院','河北工业大学城市学院','中南财经政法大学武汉学院','东北师范大学人文学院','成都理工大学广播影视学院','中北大学信息商务学院','北京化工大学北方学院','华中师范大学武汉传媒学院','重庆邮电大学移通学院','湖南商学院北津学院','广州大学华软软件学院','中国地质大学江城学院','河南大学民生学院','复旦大学上海视觉艺术学院','四川师范大学文理学院','广东工业大学华立学院','长沙理工大学城南学院','南京航空航天大学金城学院','北京科技大学天津学院','重庆大学城市科技学院','成都理工大学工程技术学院','云南大学旅游文化学院','西北工业大学明德学院','集美大学诚毅学院','广州大学松田学院','浙江师范大学行知学院','湖北大学知行学院','西北大学现代学院','北京工业大学耿丹学院','同济大学浙江学院','中国矿业大学徐海学院','湖南农业大学东方科技学院','华东交通大学理工学院','华南师范大学增城学院','南京理工大学泰州科技学院','四川外语学院重庆南方翻译学院','湘潭大学兴湘学院','南京邮电大学通达学院','重庆师范大学涉外商贸学院','北京交通大学海滨学院','上海师范大学天华学院','南昌大学科学技术学院','江西师范大学科学技术学院','浙江工业大学之江学院','长江大学文理学院','兰州商学院陇桥学院','浙江工商大学杭州商学院','三峡大学科技学院','四川外语学院成都学院','西北师范大学知行学院','北京邮电大学世纪学院','中山大学新华学院','宁波大学科学技术学院','南京师范大学泰州学院','湖北工业大学商贸学院','广西师范大学漓江学院','湖南师范大学树达学院','南京财经大学红山学院','苏州大学文正学院','中国石油大学胜利学院','湖南科技大学潇湘学院','长江大学工程技术学院','南京理工大学紫金学院','北京航空航天大学北海学院','福建农林大学东方学院','河海大学文天学院','江西农业大学南昌商学院','温州大学城市学院',)
# 民办
# tupe=('北京城市学院','湖南涉外经济学院','山东英才学院','西安欧亚学院','三亚学院','仰恩大学','黄河科技学院','西京学院','南昌理工学院','浙江树人学院','江西科技学院','武昌理工学院','吉林华桥外国语学院','汉口学院','西安外事学院','武汉东湖学院','西安翻译学院','上海杉达学院','三江学院','海口经济学院','安徽三联学院','西安培华学院','黑龙江东方学院','武汉生物工程学院','哈尔滨德强商务学院','河北传媒学院','潍坊科技学院','长沙医学院','天津天狮学院','大连艺术学院','安徽新华学院','上海建桥学院','青岛滨海学院','大连东软信息学院','吉林动画学院','辽宁财贸学院','郑州科技学院','宁波大红鹰学院','辽宁对外经贸学院','陕西国际商贸学院','山东万杰医学院','广东培正学院','西安思源学院','烟台南山学院','无锡太湖学院','浙江越秀外国语学院','武汉长江工商学院','广东白云学院','宁夏理工学院','闽南理工学院','郑州华信学院','武昌工学院','江西服装学院','哈尔滨华德学院','北京吉利大学','齐齐哈尔工程学院','黑龙江外国语学院','郑州升达经贸管理学院','青岛工学院','成都东软学院','长春建筑学院','云南工商学院','哈尔滨剑桥学院','青岛黄海学院','郑州成功财经学院','哈尔滨石油学院','哈尔滨广厦学院','南昌工学院','长江职业学院','商丘学院','哈尔滨远东理工学院','河北科技学院','大连科技学院','河北外国语学院','哈尔滨华夏计算机职业技术学院','辽宁何氏医学院','广东科技学院','河北美术学院','银川能源学院','商丘工学院','安徽外国语学院','安徽文达信息工程学院','福州外语外贸学院','山西工商学院','广西外国语学院','武汉商贸职业学院','北京科技职业学院','陕西服装工程学院','山东协和学院','广东岭南职业技术学院','青岛飞洋职业技术学院','青岛恒星职业技术学院','重庆正大软件职业技术学院','江西渝州科技职业学院','上海新侨职业技术学院','正德职业技术学院','浙江东方职业技术学院','北京经贸职业学院','云南科技信息职业技术学院','上海工商外国语职业学院',)
# tupe=('哈佛大学','普林斯顿大学','耶鲁大学','哥伦比亚大学','斯坦福大学','宾夕法尼亚大学','加利福尼亚科技学院','麻省理工学院','达特茅斯学院','杜克大学','芝加哥大学','西北大学','约翰霍普金斯大学','美国圣路易斯华盛顿大学','布朗大学','康奈尔大学','莱斯大学','范德堡大学','圣母大学','埃默里大学','乔治敦大学','美国加州大学-伯克利分校','卡内基梅隆大学','美国南加州大学','美国加州大学-洛杉矶分校','弗吉尼亚大学','威克森林大学','塔夫茨大学','密歇根大学-安娜堡分校','北卡罗来纳大学教堂山分校','波士顿大学','威廉和玛丽学院','纽约大学','布兰代斯大学','佐治亚理工学院','美国加州大学-圣地亚哥分校','利哈伊大学','罗彻斯特大学','加州大学戴维斯分校','美国加州大学-圣巴巴拉分校','凯斯西储大学','伦斯勒理工学院','加州大学欧文分校','华盛顿大学','德克萨斯大学奥斯汀分校','威斯康辛大学麦迪逊分校','美国宾州州立大学商学院','伊利诺伊大学厄巴纳-香槟分校','迈阿密大学','叶史瓦大学','乔治华盛顿大学','杜兰大学','佩珀代因大学','福罗里达州大学','雪城大学','波士顿大学','福特汉姆大学','俄亥俄州立大学哥伦比亚分校','美国普渡大学西拉法叶校区','南卫理公会大学','佐治亚大学','马里兰大学帕克分校','德州农工大学','克莱姆森大学','罗格斯大学新伯朗士威校区','明尼苏达大学双城分校','美国匹兹堡大学','伍斯特理工学院','东北大学','康涅狄格大学','弗吉尼亚科技大学','科罗拉多矿业大学',' 加州大学圣克鲁兹分校','爱荷华大学','美利坚大学','贝勒大学','迈阿密大学-牛津分校','密歇根州立大学','美国纽约州立大学环境科学与林业科学学院','阿拉巴马大学','奥本大学','纽约州立大学宾汉姆顿大学','克拉克大学','德雷塞尔大学','斯蒂文斯理工学院','圣路易斯大学','科罗拉多大学波尔得分校','丹佛大学','塔尔萨大学','爱荷华州立大学','加州大学河滨分校','密苏里大学','圣迭戈大学','佛蒙特大学','纽约州立大学石溪分校','德克萨斯基督教大学','戴顿大学','马萨诸塞大学安默斯特校区','太平洋大学','佛罗里达州立大学','霍华德大学','山佛大学','美国堪萨斯大学','内布拉斯加大学，林肯分校','新罕布什尔大学','田纳西大学','美国伊利诺伊理工大学','北卡罗来纳州立大学','美国俄克拉荷马大学','俄勒冈大学','南卡罗来纳大学哥伦比亚分校','华盛顿州立大学','芝加哥洛约拉大学','密歇根理工大学','旧金山大学','美国天主教大学','杜肯大学','纽约州立大学水牛城分校','美国亚利桑那大学','克拉克森大学','科罗拉多州立大学','路易斯安那州立大学','俄亥俄大学','圣托马斯大学','密苏里大学理工学院','肯塔基大学','犹他大学','堪萨斯州立大学','俄克拉何马州立大学','天普大学','阿肯色大学','德宝大学','薛顿贺尔大学','美国拉文大学','霍夫斯特拉大学','新泽西理工学院','新学院大学','美国俄勒冈州立大学','亚利桑那州立大学','乔治梅森大学','罗格斯-新泽西州立大学','圣约翰大学','纽约州立大学奥尔巴尼分校','伊利诺大学芝加哥校区','美国密西西比大学','德克萨斯大学达拉斯分校','密西西比州立大学','美国阿拉巴马大学伯明翰分校','纽约大学理工学院','爱达荷大学','怀俄明大学','伊利诺伊州立大学','夏威夷太平洋大学','辛辛那提大学','美国艾德菲大学','佛罗里达科技大学','德州理工大学','夏威夷马诺大学','缅因大学','马里兰大学巴尔的摩县分校','北达科他大学','威得恩大学','阿兹塞太平洋大学','罗德岛大学','弗吉尼亚联邦大学','拜欧拉大学','鲍灵格林大学','乔治福克斯大学','佩斯大学','美国南卡罗来纳州犹他州立大学','依马库雷塔大学','路易斯维尔大学','西弗吉尼亚大学','波尔州立大学','阿拉巴马汉茨维尔大学','中佛罗里达大学','西密歇根大学','肯特州立大学','蒙大拿州立大学','美国圣地亚哥州立大学','南伊利诺伊卡本代尔大学','明尼苏达圣玛利大学','哈特福大学','马萨诸塞大学卢维尔分校','南佛罗里达大学',' 圣安德鲁斯大学','北达科他州立大学','科罗拉多大学-丹佛分校','蒙大拿大学','内华达里诺大学','北卡罗来纳夏洛特大学','北卡罗来纳州立大学格林波若分校',)
# 
# j=1
# for i in tupe:
#     print i
#     shcool=School()
#     shcool.ranking=j
#     shcool.name=i
#     shcool.type=1
#     shcool.save()
#     j+=1
# School.objects.filter(ranking__lte=160).filter(ranking__gte=35).update(type=2)
# School.objects.filter(ranking__gte=600).update(type=4)
# print settings.DATABASES['default']
# finish=now()
# print start
# print finish
# print  '话费时间:'+str(finish-start)

# print School.objects.filter(name='哈佛大学').count()
if  not (UserProfile.objects.filter(user_id=2).filter(height=-1).exists() )and not (UserExpect.objects.filter(user_id=userId).filter(heighty1=0.00).filter(heighty2=0.00).filter(heighty3=0.00).exclude(heighty4=0.00).filter(heighty5=0.00).filter(heighty6=0.00).filter(heighty7=0.00).filter(heighty8=0.00).exists()):
     print 1
if Grade.objects.filter(user_id=101).exclude(heightweight__isnull=True).exclude(incomescore__isnull=True).exclude(incomeweight__isnull=True).exclude(edcationscore__isnull=True).exclude(edcationweight__isnull=True).exclude(appearancescore__isnull=True).exclude(appearanceweight__isnull=True).exists():
      print 2
      
      
      