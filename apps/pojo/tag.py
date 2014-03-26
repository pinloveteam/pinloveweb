# -*- coding: utf-8 -*-
'''
Created on 2014年1月15日

@author: jin
'''
COLOR_CLASS=('tag-limeGreen','tag-softPink')
class TagBean(object):
    def __init__(self,id,content,colorClass,isChoice):
        self.id=id
        self.content=content
        if colorClass%2==0:
            self.colorClass=COLOR_CLASS[0]
        elif colorClass%2==1:
            self.colorClass=COLOR_CLASS[1]
        self.isChoice=isChoice
        
def tag_to_tagbean(tagUserList):
    tagTuple=get_tag()
    tagBeanList=[]
    tags=[tagUser.tag.id for tagUser in tagUserList]
    for tag in tagTuple:
        if tag[0] in tags:
            tagBean=TagBean(tag[0],tag[1],tag[2],True)
        else:
            tagBean=TagBean(tag[0],tag[1],tag[2],False)
        tagBeanList.append(tagBean)
    return tagBeanList

'''
从缓存中获取性格标签
'''
def get_tag():
    from django.core.cache import cache
    tagTuple=cache.get("TAG")
    return tagTuple