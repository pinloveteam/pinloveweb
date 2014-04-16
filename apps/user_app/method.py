# coding: utf-8 
'''
Created on Dec 23, 2013

@author: jin
'''
#用户信息未填时返回的值
missing_value=[-1,'N',None,]
def user_info_card(userProfile,userTagBeanList):
    if userProfile.avatar_name_status=='3':
        avatar_name=userProfile.avatar_name
    else:
        avatar_name='user_img/image.png'
    data={
            'avatar_name':avatar_name,
            'username':userProfile.user.username,
            'height':userProfile.height,
            'age':userProfile.age,
            'education':userProfile.get_education_display(),
            'income':userProfile.income,
            'jobIndustry':userProfile.get_jobIndustry_display(),
            'city':userProfile.city,
            'sunSign':userProfile.get_sunSign_display()
            }
    #获取标签信息
    tagTupe=()
    for userTag in userTagBeanList:
        tagTupe+=(userTag.tag.content,)
    data['tagTupe']=tagTupe
    #判断信息是否未填
    for  key in data.keys():
        if data[key] in missing_value:
            data[key]='未填'
    return data

def get_profile_finish_percent(userProfile):
    fields = ( 'gender', 'income','weight','jobIndustry',
        'height', 'education','year_of_birth', 'month_of_birth', 'day_of_birth','educationSchool','city','stateProvince','country')
    num=0
    for field in fields:
        if  not getattr(userProfile,field) in [-1,'N',None]:
            num+=1
    return int((num+0.00)/len(fields)*100)


def get_score_by_profile_finsih_percent(userId,newProfileFinsihPercent,userProfile):
    if newProfileFinsihPercent>userProfile.profileFinsihPercent:
        from apps.user_score_app.method import get_score_by_finish_proflie
        if newProfileFinsihPercent>=100:
            get_score_by_finish_proflie(userId,100)
        elif newProfileFinsihPercent>=60:
            get_score_by_finish_proflie(userId,60)
        elif newProfileFinsihPercent>=30:
            get_score_by_finish_proflie(userId,30)
        userProfile.profileFinsihPercent=newProfileFinsihPercent
    return  userProfile