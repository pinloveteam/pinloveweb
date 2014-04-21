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

'''
信息完成度
'''
def get_profile_finish_percent_and_score(userProfile,oldUserProfile):
    fields = ( 'income','weight','jobIndustry',
        'height', 'education', 'day_of_birth','educationSchool','city')
    updateFields=[]
    num=0
    for field in fields:
        if  not getattr(userProfile,field) in [-1,'N',None,u'',u'地级市、县']:
            if getattr(userProfile,field)!=getattr(oldUserProfile,field):
                updateFields.append(field)
            num+=1
    from apps.user_score_app.method import get_score_by_finish_proflie
    profileFinsihPercent=int((num+0.00)/len(fields)*100)
    if profileFinsihPercent>userProfile.profileFinsihPercent:
        get_score_by_finish_proflie(userProfile.user_id,updateFields)
        userProfile.profileFinsihPercent=profileFinsihPercent
    return userProfile


def get_score_by_profile(userId,newProfileFinsihPercent,userProfile):
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