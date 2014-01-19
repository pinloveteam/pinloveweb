# -*- coding: utf-8 -*-
'''
Created on 2014年1月15日

@author: jin
'''
from apps.user_app.models import Tag
class TagBean(object):
    def __init__(self,content,isChoice):
        self.content=content
        self.isChoice=isChoice
        
def tag_to_tagbean(tagList):
    tagBeanList=[]
    tags=[tag.content for tag in tagList]
    from util.util_settings import INIT_TAGS
    tagList=INIT_TAGS
    for tag in tagList:
        if tag in tags:
            tagBean=TagBean(tag,True)
        else:
            tagBean=TagBean(tag,False)
        tagBeanList.append(tagBean)
    return tagBeanList
