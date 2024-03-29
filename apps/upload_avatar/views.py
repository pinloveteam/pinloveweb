# -*- coding: utf-8 -*-

import os
import hashlib
import time
from functools import wraps
import logging
from PIL import Image

from django.http import HttpResponse
from django.utils.crypto import get_random_string

from .app_settings import (
    UPLOAD_AVATAR_TEST_FUNC as test_func,
    UPLOAD_AVATAR_GET_UID_FUNC as get_uid,
    UPLOAD_AVATAR_MAX_SIZE,
    UPLOAD_AVATAR_UPLOAD_ROOT,
    UPLOAD_AVATAR_AVATAR_ROOT,
    UPLOAD_AVATAR_URL_PREFIX_ORIGINAL,
    UPLOAD_AVATAR_RESIZE_SIZE,
    UPLOAD_AVATAR_SAVE_FORMAT,
    UPLOAD_AVATAR_SAVE_QUALITY,
    UPLOAD_AVATAR_DELETE_ORIGINAL_AFTER_CROP,
    
    UPLOAD_AVATAR_WEB_LAYOUT,
    UPLOAD_AVATAR_TEXT,
)




from .signals import avatar_crop_done
from .models import UploadedImage
from apps.upload_avatar.models import _delete_avatar_on_disk
from apps.user_app.models import _delete_crop_avatar_on_disk, UserProfile
from pinloveweb.settings import MEDIA_URL
from apps.upload_avatar.app_settings import UPLOAD_AVATAR_MIX_SIZE,\
    UPLOAD_AVATAR_FORMAT
from django.http.response import HttpResponseServerError
from django.shortcuts import render
import simplejson
from PIL import ExifTags
logger=logging.getLogger(__name__)


border_size = UPLOAD_AVATAR_WEB_LAYOUT['crop_image_area_size']


class UploadAvatarError(Exception):
    pass


'''
检查相机设备导致的旋转
选择返回image否则返回空
'''
def detect_image_rotate(image,is_save=False):
    has_rotate=False
    for orientation in ExifTags.TAGS.keys() : 
        if ExifTags.TAGS[orientation]=='Orientation' : break 
    if (not hasattr(image, '_getexif')) or (image._getexif() is None):
        return image
    exif=dict(image._getexif().items())
    if   exif.get(orientation) == 3 : 
        image=image.rotate(180, expand=True)
        has_rotate=True
    elif exif.get(orientation) == 6 : 
        image=image.rotate(270, expand=True)
        has_rotate=True
    elif exif.get(orientation) == 8 : 
        image=image.rotate(90, expand=True)
        has_rotate=True
    if is_save and has_rotate:
        image.save()
    return image 
    
        
        
def protected(func):
    @wraps(func)
    def deco(request, *args, **kwargs):
        if not test_func(request):
            return HttpResponse(
                "<script>window.parent.upload_avatar_error('%s')</script>" % UPLOAD_AVATAR_TEXT['TEST_FUNC_NOT_PASSED']
            )
        try:
            return func(request, *args, **kwargs)
        except UploadAvatarError as e:
            return HttpResponse(
                "<script>window.parent.upload_avatar_error('%s')</script>" % e
            )
    return deco

@protected
def upload_avatar(request):
    try:
        uploaded_file = request.FILES['uploadavatarfile']
    except KeyError:
        raise UploadAvatarError(UPLOAD_AVATAR_TEXT['INVALID_IMAGE'])
    imageName=uploaded_file.name
    if uploaded_file.size > UPLOAD_AVATAR_MAX_SIZE:
        raise UploadAvatarError(UPLOAD_AVATAR_TEXT['TOO_LARGE'])
    elif uploaded_file.size < UPLOAD_AVATAR_MIX_SIZE:
        raise UploadAvatarError(UPLOAD_AVATAR_TEXT['TOO_SMALL'])
    elif not imageName[imageName.rindex('.')+1:].lower()   in UPLOAD_AVATAR_FORMAT:
        raise UploadAvatarError(UPLOAD_AVATAR_TEXT['UPLOAD_FORMAT_ERROR'])
    
    
    name, ext = os.path.splitext(uploaded_file.name)
    new_name = hashlib.md5(
        '%s%f' % (get_random_string(), time.time())
    ).hexdigest()
    new_name = '%s%s' % (new_name, ext.lower())
    
    fpath = os.path.join(UPLOAD_AVATAR_UPLOAD_ROOT, new_name)
    
    with open(fpath, 'wb') as f:
        for c in uploaded_file.chunks(10240):
            f.write(c)
            
    try:
        image=Image.open(fpath)
    except IOError:
        try:
            os.unlink(fpath)
        except:
            pass
        raise UploadAvatarError(UPLOAD_AVATAR_TEXT['INVALID_IMAGE'])
        
    #检测手机设备导致的选择
    detect_image_rotate(image,True)
    # uploaed image has been saved on disk, now save it's name in db
    if UploadedImage.objects.filter(uid=get_uid(request)).exists():
        uid=UploadedImage.objects.get(uid=get_uid(request))
        _delete_avatar_on_disk(None, uid,None,None)
        UploadedImage.objects.filter(uid=get_uid(request)).update(image=new_name)
    else:
        UploadedImage.objects.create(uid=get_uid(request), image=new_name)
        
    return HttpResponse(
        "<script>window.parent.upload_avatar_success('%s')</script>" % \
        (UPLOAD_AVATAR_URL_PREFIX_ORIGINAL + new_name)
    )


@protected
def crop_avatar(request):
    try:
        upim = UploadedImage.objects.get(uid=get_uid(request))
    except UploadedImage.DoesNotExist:
        raise UploadAvatarError(UPLOAD_AVATAR_TEXT['NO_IMAGE'])
    
    image_orig = upim.get_image_path()
    if not image_orig:
        raise UploadAvatarError(UPLOAD_AVATAR_TEXT['NO_IMAGE'])
    
    try:
        x1 = int(float(request.POST['x1']))
        y1 = int(float(request.POST['y1']))
        x2 = int(float(request.POST['x2']))
        y2 = int(float(request.POST['y2']))
    except:
        raise UploadAvatarError(UPLOAD_AVATAR_TEXT['ERROR'])
    
    
    try:
        orig = Image.open(image_orig)
    except IOError:
        raise UploadAvatarError(UPLOAD_AVATAR_TEXT['NO_IMAGE'])
    orig_w, orig_h = orig.size
    global  border_size 
    if request.POST.get('border_size',False):
        border_size=int(request.POST.get('border_size',False))
    if orig_w <= border_size and orig_h <= border_size:
        ratio = 1
    else:
        if orig_w > orig_h:
            ratio = float(orig_w) / border_size
        else:
            ratio = float(orig_h) / border_size
         
    #logger.exception('------------------------'+simplejson.dumps(request.POST))
    box = [int(x * ratio) for x in [x1, y1, x2, y2]]
    rotate=int(float(request.POST.get('rotate',0)))
    if rotate!=0:
        orig=orig.rotate(rotate)
    avatar = orig.crop(box)
    avatar_name, _ = os.path.splitext(upim.image)
    count = UserProfile.objects.filter(user_id=get_uid(request)).count()
    
    def _resize(size):
        res = avatar.resize((size[0], size[1]), Image.ANTIALIAS)
        res_name = '%s-%d.%s' % (avatar_name, size[0], UPLOAD_AVATAR_SAVE_FORMAT)
        res_path = os.path.join(UPLOAD_AVATAR_AVATAR_ROOT, res_name)
        
        res.save(res_path, UPLOAD_AVATAR_SAVE_FORMAT, quality=UPLOAD_AVATAR_SAVE_QUALITY)
        
    for size in UPLOAD_AVATAR_RESIZE_SIZE:
        _resize(size)
    if count >0:
        user=UserProfile.objects.get(user_id=get_uid(request))
        _delete_crop_avatar_on_disk(None, user,None,None)
    #save 图片到user_profile
    from apps.upload_avatar.app_settings import UPLOAD_AVATAR_DEFAULT_SIZE
    avatar_name=u'%s%s' %('user_img/',avatar_name)
    avatar_crop_done.send(sender=None, uid=get_uid(request), avatar_name=avatar_name)
    if UPLOAD_AVATAR_DELETE_ORIGINAL_AFTER_CROP:
        upim.delete()
    #判断推荐条件是否完善
    from apps.recommend_app.recommend_util import cal_recommend
    cal_recommend(request.user.id,['avatar'])    
    return HttpResponse(
        u"<script>window.parent.crop_avatar_success('%s','%s%s')</script>"  % (UPLOAD_AVATAR_TEXT['SUCCESS'],MEDIA_URL,avatar_name)
    )
