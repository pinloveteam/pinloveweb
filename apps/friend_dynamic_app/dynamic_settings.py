# -*-coding: utf-8 -*-
'''
Created on 2014年6月9日

@author: jin
'''
from pinloveweb import settings
thumbnails=140, 140
IMAGE_SAVE_FORMAT='jpg'
#上传格式
UPLOAD_PHOTO_FORMAT = getattr(settings, 'UPLOAD_PHOTO_FORMAT',['jpg','jpeg','gif','png','bmp'])
UPLOAD_PHOTO_TEXT={
                   'UPLOAD_FORMAT_ERROR':u'上传格式出错!',
                   'EORROR':'上传动态图片出错!'
                   }