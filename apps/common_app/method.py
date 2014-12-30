#-*- coding: UTF-8 -*- 
'''
Created on 2014年12月23日

@author: jin
'''
from apps.common_app.models import School
def get_school_list_by_country():
    '''
      获得学校列表根据国家
    '''
    schoolList=School.objects.all().order_by('country')
    CNSchoolList=[]
    AMSchoolList=[]
    for school in schoolList:
        if school.country==1:
            CNSchoolList.append((school.country,school.id,school.name))
        else:
            AMSchoolList.append((school.country,school.id,school.name))
    CNSchoolList.append(AMSchoolList)
    return  CNSchoolList
            
    