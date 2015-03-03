# -*- coding: utf-8 -*-
'''
Created on 2014年1月15日

@author: jin
'''
COLOR_CLASS=('tag-limeGreen','tag-softPink')
class TagBean(object):
    def __init__(self,id,content,isChoice):
        self.id=id
        self.content=content
        self.isChoice=isChoice
        
def tag_to_tagbean(tagUserList):
    tagLists=get_tag()
    tagBeanLists=[]
    tagBeanList=[]
    tags=[tagUser.tag.id for tagUser in tagUserList]
    for tagList in tagLists:
      for tag in tagList:
        if tag[0] in tags:
            tagBean=TagBean(tag[0],tag[1],True)
        else:
            tagBean=TagBean(tag[0],tag[1],False)
        tagBeanList.append(tagBean)
      tagBeanLists.append(tagBeanList)
      tagBeanList=[]
    return tagBeanLists

'''
从缓存中获取性格标签
'''
def get_tag():
    from django.core.cache import cache
    tagTuple=cache.get("TAG")
    return tagTuple