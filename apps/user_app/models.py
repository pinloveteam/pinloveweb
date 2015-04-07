# -*- coding: utf-8 -*-
'''
Created on 2013-6-27

@author: jin
'''
from django.db import models, transaction
from django.contrib.auth.models import User
import time
import string
from apps.upload_avatar.models import UploadAvatarMixIn
from apps.upload_avatar.signals import avatar_crop_done
import os
# import MySQLdb
from apps.recommend_app.models import  MatchResult, Grade
# from apps.recommend_app.recommend_util import cal_recommend
from pinloveweb.settings import UPLOAD_AVATAR_UPLOAD_ROOT, ADMIN_ID
# from util.singal import cal_recommend_user
from apps.common_app.models import Tag
import datetime
from django.utils import simplejson

'''
获得Model
'''
def get_models(className):
    classModels=globals().get(className,False)
    if classModels==False:
        return classModels
    else:
        return None
    
class UserProfileManager(models.Manager):
    '''
    根据用户id获取用户详细信息
    '''    
    def get_user_info(self,userId):
        try:
            return UserProfile.objects.get(user_id=userId)  
        except Exception as e:
            print e 
    '''
    根据id获取在推荐得分
    '''
    def get_march_result(self,my_id,other_id):
        return MatchResult.objects.filter(my_id=my_id,other_id=other_id)[:1]
    
    '''
    获取用户头像，如果头像本人，则没有通过审核也可显示
    '''
    def get_avatar_name(self,myId,userId):
        userProfile=UserProfile.objects.get(user_id=userId)
        if myId==userId or userId==ADMIN_ID:
            return userProfile.avatar_name
        elif userProfile.avatar_name_status=='3':
            return userProfile.avatar_name
        else:
            from apps.upload_avatar.app_settings import DEFAULT_IMAGE_NAME
            return DEFAULT_IMAGE_NAME
        
    def get_email_recommed_list(self,userId,limit=8):
        '''
        获取邮件推荐的用户列表
        paramters:
          limit :推荐人数默认8
        '''
        sql1='''
        select * from recommend_match_result u3 ,user_profile u1 ,auth_user u2
where u3.my_id=u2.id and u1.user_id =u3.other_id and u2.id=%s and u3.other_id not in 
(SELECT u4.recommender_id from email_recommend_history u4 where u4.user_id=%s)
and  u3.other_id not in (SELECT u5.other_id from black_list u5 where u5.my_id=%s)
and u3.other_id not in (SELECT u6.follow_id from follow u6 where u6.my_id=%s)
LIMIT %s
        '''
        sql2='''
        select * from user_profile u1 ,auth_user u2
where u1.user_id =u2.id and avatar_name_status=3 and u1.user_id not in 
(SELECT u4.recommender_id from email_recommend_history u4 where u4.user_id=%s)
and  u1.user_id not in (SELECT u5.other_id from black_list u5 where u5.my_id=%s)
and u1.user_id not in (SELECT u6.follow_id from follow u6 where u6.my_id=%s)
and u1.user_id not in (SELECT u7.other_id from recommend_match_result u7 where u7.my_id=%s)
and u1.user_id !=%s
ORDER BY u2.date_joined DESC
LIMIT %s
        '''
        userProfileSql=UserProfile.objects.raw(sql1%(userId,userId,userId,userId,limit))
        userProfileList=list(userProfileSql)
        num=limit-len(userProfileList)
        if num!=0:
            userProfileList+=list(UserProfile.objects.raw(sql2%(userId,userId,userId,userId,userId,num)))
        if len(userProfileList)==limit:
            return userProfileList
        else:
            return 'less'
        
        
class UserProfile(models.Model, UploadAvatarMixIn):
    
    user = models.ForeignKey(User)
####user_basic_profile###
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = ( (MALE, r'男'), (FEMALE, r'女'), )
    gender = models.CharField(verbose_name=r"性别", max_length=1, choices=GENDER_CHOICES, default=MALE,null=True,blank=True,) 
    
    YEAR_OF_BIRTH_CHOICES = ((-1,r'未填'),)
    for year in range(1900,2013):  
        YEAR_OF_BIRTH_CHOICES += ((year, str(year)),)
    year_of_birth = models.SmallIntegerField(verbose_name=r"出生年份", choices=YEAR_OF_BIRTH_CHOICES, default=-1,null=True,blank=True,) 

    MONTH_OF_BIRTH_CHOICES = ((-1,r'未填'),)
    for month in range(1,13):  
        MONTH_OF_BIRTH_CHOICES += ((month, str(month)),)
    month_of_birth = models.SmallIntegerField(verbose_name=r"出生月份", choices=MONTH_OF_BIRTH_CHOICES, default=-1,null=True,blank=True,)  
    
    DAY_OF_BIRTH_CHOICES = ((-1,r'未填'),)
    for day in range(1,32):  
        DAY_OF_BIRTH_CHOICES += ((day, str(day)),)
    day_of_birth = models.SmallIntegerField(verbose_name=r"出生日期", choices=DAY_OF_BIRTH_CHOICES, default=-1,null=True,blank=True,)
   
    age = models.IntegerField(verbose_name=r"年龄",max_length=11,null=True,blank=True,)
    #calculate  age
    def cal_age(self):
        if self.year_of_birth !=-1:
            current_year = time.strftime('%Y', time.localtime(time.time()))
            self.age = string.atoi(current_year) - self.year_of_birth
    
    SUN_SIGN_CHOOSICE=((-1,r'未填'),(1,r'水瓶座'),(2,r'双鱼座'),(3,r'白羊座'),(4,r'金牛座'),(5,r'双子座'),(6,r'巨蟹座'),(7,r'狮子座'),(8,r'处女座'),(9,r'天秤座'),(10,r'天蝎座'),(11,r'射手座'),(12,r'摩羯座'),)
    sunSign=models.SmallIntegerField(verbose_name=r"星座",choices=SUN_SIGN_CHOOSICE,null=True,blank=True,default=-1)
    #calculate  sunSign
    def cal_sunSign(self):
#         if self.year_of_birth !=-1 and self.month_of_birth !=-1 and self.year_of_birth !=year_of_birth and self.month_of_birth !=month_of_birth :
         n = (12,1,2,3,4,5,6,7,8,9,10,11)  
         d = ((1,20),(2,19),(3,21),(4,21),(5,21),(6,22),(7,23),(8,23),(9,23),(10,23),(11,23),(12,23))  
         self.sunSign= n[len(filter(lambda y:y<=(self.month_of_birth,self.day_of_birth), d))%12]  
    
    ZODIAC_CHOOSICE=((-1,r'未填'),(0,r'鼠'),(1,r'牛'),(2,r'虎'),(3,r'兔'),(4,r'龙'),(5,r'蛇'),(6,r'马'),(7,r'羊'),(8,r'猴'),(9,r'鸡'),(10,r'狗'),(11,r'猪'),)
    zodiac=models.SmallIntegerField(verbose_name=r"生肖",choices=ZODIAC_CHOOSICE,null=True,blank=True,default=-1)
    #calculate  zodiac
    def cal_zodiac(self):
        self.zodiac=(self.year_of_birth-1900)%12
    
    ETHNICGROUP_CHOOSICE=((-1,r'未填'),(1,r'汉族'),(2,r'蒙古族'),(3,r'满族'),(4,r'朝鲜族'),(5,r'赫哲族'),(6,r'达斡尔族'),(7,r'鄂温克族'),(8,r'鄂伦春族'),(9,r'回族'),(10,r'东乡族'),(11,r'土族'),(12,r'撒拉族'),(13,r'保安族'),(14,r'裕固族'),(15,r'维吾尔族'),(16,r'哈萨克族'),(17,r'柯尔克孜族'),(18,r'锡伯族'),(19,r'塔吉克族'),(20,r'乌孜别克族'),(21,r'俄罗斯族'),(22,r'塔塔尔族'),(23,r'藏族'),(24,r'门巴族'),(25,r'珞巴族'),(26,r'羌族'),(27,r'彝族'),(28,r'白族'),(29,r'哈尼族'),(30,r'傣族'),(31,r'僳僳族'),(32,r'佤族'),(33,r'拉祜族'),(34,r'纳西族'),(35,r'景颇族'),(36,r'布朗族'),(37,r'阿昌族'),(38,r'普米族'),(39,r'怒族'),(40,r'德昂族'),(41,r'独龙族'),(42,r'基诺族'),(43,r'苗族'),(44,r'布依族'),(45,r'侗族'),(46,r'水族'),(47,r'仡佬族'),(48,r'壮族'),(49,r'瑶族'),(50,r'仫佬族'),(51,r'毛南族'),(52,r'京族'),(53,r'土家族'),(54,r'黎族'),(55,r'畲族'),(56,r'高山族'),)
    ethnicGroup=models.SmallIntegerField(verbose_name=r"民族",choices=ETHNICGROUP_CHOOSICE,null=True,blank=True,default=-1)
    
    BLOODTYPE_CHOOSICE=(('N',r'未填'),('A',r'A型'),('B',r'B型'),('AB',r'AB血型'),('O',r'O型'),('0',r'其他血型'),)
    bloodType=models.CharField(verbose_name=r'血型',choices=BLOODTYPE_CHOOSICE,max_length=2,null=True,blank=True,default='N')
    
    HEIGHT_CHOICES = ((-1,r'未填'),)
    for height in range(130,226):  
        HEIGHT_CHOICES += ((height, str(height)),)
    height = models.IntegerField(verbose_name=r"身高（厘米）", choices=HEIGHT_CHOICES, default=-1,null=True,blank=True,)  # height=models.IntegerField(max_length=8) 
    
    SINGLE = 'S'
    MARRIED = 'M'
    DIVORCED = 'D'
    WIDOWED = 'W'
    SEPARATED = 'P'
    MARITAL_STATUS_CHOICES = ( ('N', r'未填'),(SINGLE, r'单身'), (MARRIED, r'已婚'), (DIVORCED, r'离婚'), (SEPARATED, r'分居'), (WIDOWED, r'丧偶'))
    maritalStatus = models.CharField(verbose_name=r"婚姻状态", max_length=1, choices=MARITAL_STATUS_CHOICES, default='N',null=True,blank=True,)  
    
    hasChild=models.NullBooleanField(verbose_name=r"是否有孩子",choices=((True,r'有'),(False,r'无')),null=True,blank=True,)
    
    # education experience 
    choice=-1 #未填
    secondary=0 #大专以下
    junior=1  # 大专
    Bachelor =2# 本科
    master=3 #硕士
    doctor=4 # 博士 
    EDUCATION_DEGREE_CHOICES=((choice,r'未填'),(secondary,r'大专以下'),(junior,r'大专'),(Bachelor,r'本科'),(master,r'硕士 '),(doctor,r'博士 '),)
    education = models.IntegerField(verbose_name=r"学位",choices=EDUCATION_DEGREE_CHOICES, default=-1,null=True,blank=True,) # educate = models.CharField(max_length=50)
    #school
    educationSchool = models.CharField(verbose_name=r"最高学位毕业学校", max_length=100,null=True,blank=True,) 
    educationSchool_2 = models.CharField(verbose_name=r"毕业学校2", max_length=100,null=True,blank=True,) 
    # personal web and links 
    link=models.CharField(verbose_name=r"共享链接",max_length=128,default='me',null=True,blank=True,)  

    
    # location
    country = models.CharField(verbose_name=r"所在国家", max_length=50,null=True,blank=True,)
    stateProvince = models.CharField(verbose_name=r"所在省", max_length=50,null=True,blank=True,) 
    
    city = models.CharField(verbose_name=r"所在城市", max_length=50,null=True,blank=True,) 
    '''
    限制城市长度
    '''
    def limit_city_length(self,limit_length=12):
        if  isinstance(self.city,basestring) and len(self.city.encode('gbk'))>limit_length:
            if self.city.find(u' ')!=-1:
                return self.city[:self.city.find(u' ')]
        else:
            return self.city
    streetAddress = models.CharField(verbose_name=r"街道地址", max_length=255,null=True,blank=True,)
    INCOME_CHOICES = ((-1,"未填"),(1,"5万以下"))
    for income in range(5,100,1):  
        INCOME_CHOICES += ((income, '%s%s'%(str(income),u'万')),)
    INCOME_CHOICES += ((100000, "100万以上"),)
    income = models.IntegerField(verbose_name=r"年薪（万元）", choices=INCOME_CHOICES, default=-1,null=True,blank=True,) # payRang=models.CharField(max_length=50)
   
    position=models.CharField(verbose_name=r'定位',max_length=10,null=True,blank=True,)
    
    # photo
     
    language=models.CharField(verbose_name='语言能力',max_length=20,null=True,blank=True,)
    
    avatar_name = models.CharField(verbose_name=r"头像路径",max_length=128,default='user_img/image',null=True,blank=True,)
    """
           1:未上传  
           2.正在审核
           3.审核通过
           4.审核未通过
    """
    AVAYAR_STATUS_CHOICES = (('1',"未上传"),('2',"正在审核"),('3',"审核通过"),('4',"审核未通过"),)
    avatar_name_status= models.CharField(verbose_name=r"头像状态",max_length=2, choices=AVAYAR_STATUS_CHOICES,default='1',null=True,blank=True,)
 
    def get_uid(self):
        return self.user.id
 
    def get_avatar_name(self, size):
        return UploadAvatarMixIn.build_avatar_name(self, self.avatar_name, size)
    def get_image_path(self):
        from apps.upload_avatar.app_settings import UPLOAD_AVATAR_DEFAULT_SIZE
        path = os.path.join(UPLOAD_AVATAR_UPLOAD_ROOT, self.get_avatar_name(UPLOAD_AVATAR_DEFAULT_SIZE))
        if not os.path.exists(path):
            return None
        return path
    
    '''
    检查出生年月日是否填写
    '''
    def check_birth(self):
        if (self.day_of_birth!=-1 and self.month_of_birth!=-1 and self.year_of_birth!=-1):
            return True
        else:
            return False
    
####user_appearance###
    self_evaluation=models.FloatField(verbose_name=r"自我评价",choices=((0.0,r'未填'),(0.35,r'普通'),(0.70,r'不错'),(1.00,r'很好')),null=True,blank=True,default=0.0)
    CHOICE_WEIGHT=((-1,r'未填'),)
    for i in range(40,300,1):
        CHOICE_WEIGHT+=((i,str(i)),)
    weight=models.SmallIntegerField(verbose_name=r"体重(kg)",choices=CHOICE_WEIGHT,null=True,blank=True,default=-1)
    
    HAIR_STYLE_CHOICE=(('N',r'未填'),('0',r'顺直长发'),('1',r'卷曲长发'),('2',r'中等长度'),('3',r'短发'),('4',r'平头'),('5',r'光头'),('6',r'其他'),)
    hairStyle=models.CharField(verbose_name=r"发型",choices=HAIR_STYLE_CHOICE,max_length=2,null=True,blank=True,default='N')
    
    HAIR_COLOR_CHOICE=(('N',r'未填'),('0',r'黑色'),('1',r'金色'),('2',r'褐色'),('3',r'栗色'),('4',r'灰色'),('5',r'红色'),('6',r'白色'),('7',r'挑染'),('8',r'光头'),('9',r'其他'),)
    hairColor=models.CharField(verbose_name=r"发型",choices=HAIR_COLOR_CHOICE,max_length=2,null=True,blank=True,default='N')
    
    FACE_CHOICE=(('N',r'未填'),('0',r'圆脸型'),('1',r'方脸型'),('2',r'长脸型'),('3',r'瓜子脸型'),('4',r'国字脸型'),('5',r'三角脸型'),('6',r'菱形脸型'),('7',r'其他'),)
    face=models.CharField(verbose_name=r"发型",choices=HAIR_STYLE_CHOICE,max_length=2,null=True,blank=True,default='N')
    
    EYE_COLOR_CHOICE=(('N',r'未填'),('0',r'黑色'),('1',r'蓝色'),('2',r'浅褐色'),('3',r'棕色'),('4',r'灰色'),('5',r'绿色'),('6',r'其它'),)
    eyeColor=models.CharField(verbose_name=r"发型",choices=HAIR_STYLE_CHOICE,max_length=2,null=True,blank=True,default='N')
    
    BODY_SHAPE_CHOICE=(('N',r'未填'),('0',r'苗条'),('1',r'匀称'),('2',r'高挑'),('3',r'丰满'),('4',r'健壮'),('5',r'魁梧'),('6',r'其他'),)
    bodyShape=models.CharField(verbose_name=r"发型",choices=HAIR_STYLE_CHOICE,max_length=2,null=True,blank=True,default='N')
    
#####user_study_work
    JOB_INDUSRY_CHOICE=((-1,r'未填'),(0,r'IT|互联网'),(1,r'金融业'),(2,r'房地产|建筑业'),(3,r'商业服务'),(4,r'贸易|租赁'),(5,r'教育'),
                        (6,r'加工|制造'),(8,r'交通|物流'),(9,r'服务业'),(10,r'文化|传媒'),(11,r'能源|矿产'),
                        (12,r'政府|事业单位'),(13,r'农业'),(14,r'学生'),(15,r'通信|电子'),(16,r'批发|零售'),(17,r'科研'),
                        (18,r'体育'),(19,r'环保'),(20,r'非营利组织'),(21,r'农业'),(22,r'生物|制药'),(23,r'医疗|护理'),(24,r'其它'))
    jobIndustry = models.IntegerField(verbose_name=r"职业领域",max_length=125,null=True,blank=True,choices=JOB_INDUSRY_CHOICE) 
    
    jOB_TITLE=((-1,r'未填'),(0,r'普通职员'),(1,r'中层管理者'),(2,r'高层管理者'),(3,r'企业主'),)
    jobTitle = models.IntegerField(verbose_name=r"目前职位",choices=jOB_TITLE, max_length=50,null=True,blank=True,default=-1) 
    
    COMPANY_TYPE_CHOICE=(('N',r'未填'),('0',r'政府机关'),('1',r'事业单位'),('2',r'外企企业'),('3',r'上市公司'),('4',r'国有企业'),('5',r'私营企业'),('6',r'自有公司'),)
    companyType=models.CharField(verbose_name=r"公司性质", choices=COMPANY_TYPE_CHOICE,max_length=2,null=True,blank=True,default='N') 
    
    WORK_STATUS_CHOICE=(('N',r'未填'),('0',r'轻松稳定'),('1',r'朝九晚五'),('2',r'偶尔加班'),('3',r'经常加班'),('4',r'偶尔出差'),('5',r'经常出差'),('6',r'经常有应酬'),('7',r'工作时间自由'),('8',r'其他'),)
    workStatus=models.CharField(verbose_name=r"工作状态", choices=WORK_STATUS_CHOICE,max_length=2,null=True,blank=True,default='N') 
    
    companyName=models.CharField(verbose_name=r"公司名字", max_length=50,null=True,blank=True,) 
  
    educationCountry = models.CharField(verbose_name=r"最高学位毕业国家", max_length=50,null=True,blank=True,) 
    
####user_personal_habit
    BELIEF_CHOICE=(('N',r'未填'),('0',r'无宗教信仰'),('1',r'佛教'),('2',r'基督教'),('3',r'犹太教'),('4',r'伊斯兰教'),('5',r'印度教'),('6',r'神道教'),('7',r'其他'),)
    belief=models.CharField(verbose_name=r"信仰",choices=BELIEF_CHOICE, max_length=2,null=True,blank=True,default='N') 
   
    SMOKE_CHOICE=(('N',r'未填'),('0',r'不吸烟'),('1',r'社交时偶尔吸'),('2',r'每周吸几次'),('3',r'每天都吸'),)
    isSmoke=models.CharField(verbose_name=r"吸烟",choices=SMOKE_CHOICE, max_length=2,null=True,blank=True,default='N') 
    
    DRINK_CHOICE=(('N',r'未填'),('0',r'不喝'),('1',r'社交时喝酒'),('2',r'有兴致时喝'),('3',r'每天都离不开酒)'),)
    isDrink=models.CharField(verbose_name=r"喝酒",choices=DRINK_CHOICE, max_length=2,null=True,blank=True,default='N') 
    
    BEDDING_TIME_CHOICE=(('N',r'未填'),('0',r'早睡早起很规律'),('1',r'经常夜猫子'),('2',r'总是早起鸟'),('3',r'偶尔懒散一下'),('4',r'总是早起鸟'),('5',r'没有规律'),)
    beddingTime=models.CharField(verbose_name=r"作息习惯",choices=BEDDING_TIME_CHOICE, max_length=2,null=True,blank=True,default='N') 
    pet=models.CharField(verbose_name=r"宠物",max_length=30,null=True,blank=True,) 
    character=models.CharField(verbose_name=r"个性", max_length=50,null=True,blank=True,) 
    
###user_family_information
    MONTHLY_EXPENSE_CHOICE=((-1,r'未填'),(1,r'1000元以下'),)
    for i in range(1,20,1):
        temp=str(i*1000)+'-'+str((i+1)*1000)+'元'
        MONTHLY_EXPENSE_CHOICE+=((i*100+5,temp),)
    MONTHLY_EXPENSE_CHOICE+=((90000,r'2万以上'),)
    monthlyExpense=models.IntegerField(verbose_name=r'月消费',choices=MONTHLY_EXPENSE_CHOICE,default=-1,null=True,blank=True,)
    isOnlyChild=models.NullBooleanField(verbose_name=r'是否是独生子女',choices=((True,r'是'),(False,r'否'),),null=True,blank=True,)
    hasCar=models.NullBooleanField(verbose_name=r'是否购车',choices=((True,r'是'),(False,r'否'),),null=True,blank=True,)
    hasHouse=models.NullBooleanField(verbose_name=r'是否是购房',choices=((True,r'是'),(False,r'否'),),null=True,blank=True,)
    financialCondition=models.CharField(verbose_name=r'家庭经济条件',choices=(('N',r'未填'),('0',r'富裕'),('1',r'小康'),('2',r'温饱'),),max_length=1,null=True,blank=True,default='N')
    parentEducation=models.CharField(verbose_name=r'父母受教育水平',choices=(('N',r'未填'),('0',r'高级知识分子'),('1',r'普通知识分子'),),max_length=1,null=True,blank=True,default='N')
###user_family_life    
    liveWithParent=models.CharField(verbose_name=r'愿与Ta父母同住',choices=(('N',r'未填'),('0',r'愿意'),('1',r'不愿意'),('2',r'视情况而定'),),max_length=1,null=True,blank=True,)
    likeChild=models.CharField(verbose_name=r'是否喜欢有孩子',choices=(('N',r'未填'),('0',r'愿意'),('1',r'不愿意'),('2',r'视情况而定'),),max_length=1,null=True,blank=True,)
    lastLoginAddress=models.CharField(verbose_name=r'最后登录地点',max_length=100,null=True,blank=True,)
    profileFinsihPercent=models.SmallIntegerField(verbose_name=r'资料完成度',default=0,null=True,blank=True,)
    member=models.SmallIntegerField(verbose_name=r'资料完成度',default=0,choices=((0,u'普通用户'),(1,u'会员'),),null=True,blank=True,)
    guide=models.CharField(verbose_name=r'引导',max_length=255,null=True,blank=True,)
    finish=models.CharField(verbose_name=r'个人信息完成字段',max_length=255,null=True,blank=True,)
    #定制管理器
    objects = UserProfileManager()
    
    #获取头像
    def get_avatar_image(self):
        if self.avatar_name_status!='3':
            return 'user_img/image'
        else:
            return self.avatar_name
        
    '''
    计算收入
    '''
    def _cal_income(self,oldUserProfile):
        if self.income!=None and self.income!=oldUserProfile.income:
            from apps.recommend_app.recommend_util import cal_income
            incomes=cal_income(self.income,self.gender)
            if Grade.objects.filter(user=self.user).exists():
                Grade.objects.filter(user=self.user).update(incomescore=incomes)
            else:
                Grade(user=self.user,incomescore=incomes).save()

    '''
    计算学历
    '''        
    def _cal_education(self,oldUserProfile):
        if self.education!=-1 and (not self.educationSchool in [None,u'']) and (self.education != oldUserProfile.education or  self.educationSchool!=oldUserProfile.educationSchool or self.educationSchool_2!=oldUserProfile.educationSchool_2):
            from apps.recommend_app.recommend_util import cal_education
            if self.educationSchool_2==None:
                educationscore=cal_education(self.education,self.educationSchool,self.gender,1)
            else:
                SchoolScore1=cal_education(self.education,self.educationSchool,self.gender,1)
                SchoolScore2=0
                if self.educationSchool_2 != None and self.educationSchool_2.rstrip() !=u'':
                    SchoolScore2=cal_education(self.education,self.educationSchool_2,self.gender,2)
                if SchoolScore1>SchoolScore2:
                    educationscore=SchoolScore1
                else:
                    educationscore=SchoolScore2
#             educationscore=cal_education(self.education,self.educationSchool)
            if Grade.objects.filter(user=self.user).exists():
                Grade.objects.filter(user=self.user).update(educationscore=educationscore)
            else:
                Grade(user=self.user,educationscore=educationscore).save()
                
    @transaction.commit_on_success
    def save(self, *args, **kwargs):
       oldUserProfile=kwargs.pop('oldUserProfile',None)
       if oldUserProfile:
           self._cal_income(oldUserProfile)
           self._cal_education(oldUserProfile)
           if not oldUserProfile.check_birth():
               self.cal_age()
               self.cal_sunSign()
       super(UserProfile, self).save(*args, **kwargs)
       
    class Meta:
        verbose_name=u'用户基本信息'
        verbose_name_plural = u'用户基本信息'
        db_table='user_profile'

class UserContactLink(models.Model):
    user=models.ForeignKey(User)
    
    trueName = models.CharField(verbose_name=r"真实姓名", max_length=50,null=True,blank=True,)
    
    # phone number 
    mobileNumber = models.CharField(verbose_name=r"手机号码", max_length=20,null=True,blank=True,)
    
    ID_CARD_CHIOSE=((-1,'请选择'),(0,'身份证'),(1,'护照'))
    IDCardChoice=models.IntegerField(verbose_name=r"证件类型",choices=ID_CARD_CHIOSE,null=True,blank=True,default=-1)
    IDCardNumber=models.CharField(verbose_name=r"证件号码", max_length=50,null=True,blank=True,)
    
    QQ=models.CharField(verbose_name=r"QQ", max_length=20,null=True,blank=True,)
    
    MSN=models.CharField(verbose_name=r"MSN", max_length=20,null=True,blank=True,)
    
    CountryHome=models.CharField(verbose_name=r"户口所在地国家", max_length=50,null=True,blank=True,)
    stateProvinceHome=models.CharField(verbose_name=r"户口所在地省", max_length=50,null=True,blank=True,)
    cityHome=models.CharField(verbose_name=r"户口所在地市", max_length=50,null=True,blank=True,)
    class Meta:
        verbose_name=u'用户身份信息'
        verbose_name_plural = u'用户身份信息'
        db_table = "user_contact_link" 

    
class UserVerification(models.Model):
    user=models.ForeignKey(User)
    """
           1:未认证  
           2.正在审核
           3.认证通过
           4.认证未通过
    """
    STATUS_CHOICES = (('1',"未认证"),('2',"正在审核"),('3',"已认证"),('4',"认证未通过"),)
    IDCardValid=models.CharField(verbose_name=r"身份证（护照）验证",max_length=2,choices=STATUS_CHOICES,default='1',)
    IDCardPicture=models.ImageField(verbose_name=r"证件照片",max_length=128,upload_to='verfication_img/IDCard',null=True)
    MOBILE_EMAIL_STATUS_CHOICES = (('1',"未认证"),('2',"已认证"),)
    mobileNumberValid=models.CharField(verbose_name=r"手机号码验证",max_length=2,choices=MOBILE_EMAIL_STATUS_CHOICES,default='1',)
    emailValid=models.CharField(verbose_name=r"邮箱验证",max_length=2,choices=MOBILE_EMAIL_STATUS_CHOICES,default='1',)
#     jobValid=models.NullBooleanField(verbose_name=r"工作验证",choices=STATUS_CHOICES,default='1',)
    incomeValid=models.CharField(verbose_name=r"收入验证",max_length=2,choices=STATUS_CHOICES,default='1',)
    incomePicture=models.ImageField(verbose_name=r"收入证明",max_length=128,upload_to='verfication_img/income',null=True)
    educationValid=models.CharField(verbose_name=r"学历验证",max_length=2,choices=STATUS_CHOICES,default='1',)
    educationPicture=models.ImageField(verbose_name=r"学历证明",max_length=128,upload_to='verfication_img/education',null=True)
    educationPicture2=models.ImageField(verbose_name=r"学历证明",max_length=128,upload_to='verfication_img/education',null=True)
    class Meta:
        verbose_name=u'用户信息验证'
        verbose_name_plural = u'用户信息验证'
        db_table = "user_verification" 

class BrowseOherScoreHistoryManage(models.Manager):
    '''
     相互查看过分数的用户列表
     myId  我的用户id
oherIdList 另外用户id列表，如果为None则查询所有用户
    '''
    def browse_score_each_other(self,myId,oherIdList=None):
        sql='''
        select * from 
browse_oher_score_history where my_id= %s and 
other_id in (SELECT my_id from browse_oher_score_history where other_id=%s) 
'''
        if oherIdList is None:
            BrowseOherScoreHistoryList=BrowseOherScoreHistory.objects.raw(sql,[myId,myId])
        else:
            count=len(oherIdList)
            sql=sql+'and other_id in(%s)'%(('%s,'*count)[:-1])
            list=[myId,myId]
            list.extend(oherIdList)
            BrowseOherScoreHistoryList=BrowseOherScoreHistory.objects.raw(sql,list)
        return BrowseOherScoreHistoryList
'''
浏览另一半分数表
'''
class BrowseOherScoreHistory(models.Model):
    my=models.ForeignKey(User,verbose_name=u"用户",related_name=u'browse_oher_score_history_my')
    other=models.ForeignKey(User,verbose_name=u"另一半用户",related_name=u'browse_oher_score_history_other')
    objects=BrowseOherScoreHistoryManage()
    class Meta:
        verbose_name=u'浏览另一半得分记录表'
        verbose_name_plural = u'浏览另一半得分记录表'
        db_table = "browse_oher_score_history" 
    
class UserHobbyInterest(models.Model):
    user=models.ForeignKey(User)
    sport=models.CharField(verbose_name=r"爱好什么体育运动", max_length=50,null=True) 
    food=models.CharField(verbose_name=r"爱好什么食物", max_length=50,null=True) 
    book=models.CharField(verbose_name=r"爱好什么书籍", max_length=50,null=True) 
    movice=models.CharField(verbose_name=r"爱好什么电影", max_length=50,null=True) 
    TVShow=models.CharField(verbose_name=r"爱好什么关注节目", max_length=50,null=True) 
    recreation=models.CharField(verbose_name=r"爱好什么娱乐休闲", max_length=50,null=True) 
    travel=models.CharField(verbose_name=r"爱好什么旅游去处", max_length=50,null=True) 
    class Meta:
        verbose_name=u'用户兴趣爱好'
        verbose_name_plural = u'用户兴趣爱好'
        db_table = "user_hobby_interest" 
'''
关注表
'''
class FollwManager(models.Manager):
    #==================================
    #获取相互关注的人数
    #attribute：follow_id关注者的id
    #=================================
    def follow_each_count(self,follow_id):
        try:
            sql='''
            select count(*) from follow where follow_id= %s and my_id in (SELECT follow_id from follow where my_id=%s)
            '''
            from django.db import connection
            cursor=connection.cursor()
            cursor.execute(sql,(follow_id,follow_id))
            count=cursor.fetchone()[0]
            cursor.close()
            return count
        except Exception as e:
            print e
     
    #==================================
    #获取相互关注的列表
    #attribute：follow_id关注者的id
    #=================================       
    def follow_each(self,follow_id,**kwargs):
        follow_id=str(follow_id)
        if kwargs.get('userIdList',False):
            userIdList=kwargs.get('userIdList')
            count=len(userIdList)
            
            sql='''
            select * from 
follow where follow_id= %s and 
my_id in (SELECT follow_id from follow where my_id=%s) 
and my_id in('''+('%s,'*count)[:-1]+''')
            '''
            params=[follow_id,follow_id]
            params.extend(userIdList)
            followEachList=Follow.objects.raw(sql,params)
        else:
            followEachList=Follow.objects.raw("select * from follow where follow_id= %s and my_id in (SELECT follow_id from follow where my_id=%s) ",(follow_id,follow_id))
        return followEachList
class Follow(models.Model):
    my=models.ForeignKey(User,related_name='user_my',verbose_name=r'自己',)
    follow=models.ForeignKey(User,related_name='user_follow',verbose_name=r'关注的人',)
    objects=FollwManager()
    class Meta:
        verbose_name = u'关注表' 
        verbose_name_plural = u'关注表'
        db_table = "follow" 

        
'''
用户标签表
'''
class TagManage(models.Manager):
    '''
    根据类型获得标签集合
    attribute：
        type 
            0：自己的个人标签
            1.自己对另一半的期望标签
        user_id    用户id
    return
       UserTag
    '''
    def get_tags_by_type(self,user_id=None,type=0,*args, **kwargs):   
        return UserTag.objects.filter(user_id=user_id,type=type,*args, **kwargs) 
    
    '''
    批量插入用户标签表
    '''   
    @transaction.commit_on_success 
    def bulk_insert_user_tag(self,user_id,type,tagIdList):
        tagTupe=Tag.objects.all()
        count=len(tagTupe)/3
        if len(tagIdList)!=count:
            if type==0:
                raise Exception('我的性格标签必须全部选择') 
            elif type==1:
                raise Exception('Ta的性格标签必须全部选择') 
        tagIds=[]
        for tag in tagTupe:
            tagIds.append(tag.id)
        #保存tag信息
        tags=[]
        for tag in tagIdList:
            try:
                tag=int(tag)
            except Exception as e:
                print e
            if not tag in tagIds:
                pass
            else:
                tags.append(UserTag(user_id=user_id,tag_id=tag,type=type))
        UserTag.objects.filter(user_id=user_id,type=type).delete()
        UserTag.objects.bulk_create(tags)
class UserTag(models.Model):
    user=models.ForeignKey(User,related_name='tab_user',verbose_name=u'用户')
    tag=models.ForeignKey(Tag,related_name=u'tag',verbose_name=u'标签')
    TYPE_CHOICES=((0,u'自己的标签'),(1,u'对另一半的标签'))
    type=models.SmallIntegerField(verbose_name='类型',choices=TYPE_CHOICES)
    objects=TagManage()
    class Meta:
        verbose_name = u'用户标签表' 
        verbose_name_plural = u'用户标签表'
        db_table = "user_tag" 
        

class Dictionary(models.Model):

    key=models.CharField(max_length=128)
    name=models.CharField(max_length=255,default='')
    value=models.CharField(max_length=255)

class Verification(models.Model):
        
    username = models.CharField(max_length=30)
    verification_code = models.CharField(max_length=50)
    class Meta:
        verbose_name=u'临时验证码'
        verbose_name_plural = u'临时验证码'
        db_table='verification'
    
'''
黑名单
'''   
class BlackList(models.Model):
    my=models.ForeignKey(User,related_name='black_list_user',verbose_name=u'拉黑用户')
    other=models.ForeignKey(User,related_name='black_list_other',verbose_name=u'被拉黑的用户')
    createTime=models.DateTimeField(verbose_name=u'创建时间',)
    
    def save(self,*args,**kwargs):
        self.createTime=datetime.datetime.now()
        super(BlackList,self).save(*args,**kwargs)
    class Meta:
        verbose_name=u'黑名单'
        verbose_name_plural = u'黑名单'
        db_table='black_list'

'''
举报
'''
class Denounce(models.Model):
    my=models.ForeignKey(User,related_name='denounce_user',verbose_name=u'举报用户')
    FROM_CHOICES=((0,u'私信'),)
    comeFrom=models.SmallIntegerField(verbose_name='举报内容来自哪里',null=True)
    auid=models.IntegerField(verbose_name='举报内容id',null=True)
    other=models.ForeignKey(User,related_name='denounce_other',verbose_name=u'被举报的用户')
    STATUTS_CHOICES=((0,u'未处理'),(1,u'无效'),(2,u'有效'),)
    status=models.SmallIntegerField(verbose_name=u'处理状态',default=0,choices=STATUTS_CHOICES)
    TYPE_CHOICES=((0,u'色情交易'),(1,u'头像、资料虚假或冒用'),(2,u'婚托、饭托、酒托'),
                  (3,u' 骚扰广告'),(4,u' 诈骗钱财、虚假中奖信息'),(5,u' 其他理由'),)
    type=models.SmallIntegerField(verbose_name=u'举报类型',choices=TYPE_CHOICES)
    reason=models.CharField(verbose_name=u'理由',max_length=128,null=True)
    createTime=models.DateTimeField(verbose_name=u'创建时间')
    def save(self,*args,**kwargs):
        self.createTime=datetime.datetime.now()
        super(Denounce,self).save(*args,**kwargs)
    class Meta:
        verbose_name=u'举报'
        verbose_name_plural = u'举报'
        db_table='denounce'

def save_avatar_in_db(sender, uid, avatar_name, **kwargs):
    if UserProfile.objects.filter(user_id=uid).exists():
        UserProfile.objects.filter(user_id=uid).update(avatar_name=avatar_name,avatar_name_status='2')
    else:
        UserProfile.objects.create(user_id=uid, avatar_name=avatar_name,avatar_name_status='2')
        
  
avatar_crop_done.connect(save_avatar_in_db)
 
def _delete_crop_avatar_on_disk(sender, instance, *args, **kwargs):
    path = instance.get_image_path()
    if path:
        try:
            os.unlink(path)
        except OSError:
            pass
avatar_crop_done.connect(_delete_crop_avatar_on_disk,sender=UserProfile)

# @transaction.autocommit
# def basic_profile_callback(sender, userProfile,height,education,educationSchool,income,**kwargs):
#    profile=userProfile
#    if profile!=None :
#         flag=False
#         if profile.income!=-1 and userProfile.income!=income:
#             from apps.recommend_app.recommend_util import cal_income
#             incomes=cal_income(profile.income)
#             from apps.recommend_app.models import Grade
#             if Grade.objects.filter(user_id=profile.user.id).exists():
#                Grade.objects.filter(user_id=profile.user.id).update(incomescore=incomes)
#             else:
#                Grade(user_id=profile.user.id,incomescore=incomes).save()
#             flag=True
#         if (userProfile.education!=education or userProfile.educationSchool!=educationSchool):
#             from apps.recommend_app.recommend_util import cal_education
#             score=cal_education(profile.education,profile.educationSchool)
#             from apps.recommend_app.models import Grade
#             if Grade.objects.filter(user_id=profile.user.id).exists():
#                Grade.objects.filter(user_id=profile.user.id).update(edcationscore=score)
#             else:
#                Grade(user_id=profile.user.id,edcationscore=score).save()
#             flag=True
#         if height!=userProfile.height:
#              flag=True
#         #如果收入，学历，发生改变重新计算推荐
#         if flag:
#           cal_recommend(profile.user.id)
# 
# """
# signals 用于监听，触发事件
# """
# # signals.post_save.connect(basic_profile_callbacke, sender=user_basic_profile)  
# cal_recommend_user.connect(basic_profile_callback, sender=None)