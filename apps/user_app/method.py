# coding: utf-8 
'''
Created on Dec 23, 2013

@author: jin
'''
#用户信息未填时返回的值
missing_value=[-1,'N',None,]
def user_info_card(userProfile):
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
    #判断信息是否未填
    for  key in data.keys():
        if data[key] in missing_value:
            data[key]='未填'
    return data