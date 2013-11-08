# -*- coding: utf-8 -*-
'''
Created on Sep 1, 2013

@author: jin
'''
from pinloveweb import settings
'''分页'''
from apps.recommend_app import recommend_settings
PAGE_NUM=getattr(recommend_settings, 'PAGE_NUM', 8)
BEVOR_RANGE_NUM=getattr(recommend_settings, 'BEVOR_RANGE_NUM', 4)
AFTER_RANGE_NUM=getattr(recommend_settings, 'AFTER_RANGE_NUM,', 4)


'''图片上传路径'''
IMAGE_UPLOAD_PATH_M='%s%s'%(settings.MEDIA_ROOT,'/images/')
'''图片上传路径相对路径'''
RELATRVE_IMAGE_UPLOAD_PATH_M='images/'