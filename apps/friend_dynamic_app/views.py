# -*-coding: utf-8 -*-
'''
Created on Nov 5, 2013

@author: jin
'''
from django.shortcuts import render
from apps.friend_dynamic_app.models import FriendDynamic, Picture,\
    FriendDynamicArgee, FriendDynamicComment
from pinloveweb import settings
from PIL import ImageFile 
import time
from apps.user_app.models import UserProfile, Follow
from django.utils import simplejson
from django.http import HttpResponse
import logging

'''
卡片界面动态
'''
def dynamic(request):
    arg={}
    if request.method=="POST":
        flag=True
        content=request.POST.get('content').strip()
        if content.rstrip()=='':
            arg['error']={'error':u'发布内容不能为空！'}
            flag=False
        friendDynamic=FriendDynamic()
        friendDynamic.publishUser=request.user
        friendDynamic.content=content
        if 'images_path' in request.session.keys():
            friendDynamic.data=request.session['images_path']
            friendDynamic.type=2
        else:
            friendDynamic.type=1
        friendDynamic.save()
        if 'images_path' in request.session.keys():
#             pictureList=[]
            photoList=simplejson.loads(request.session['images_path'])
            for photo in photoList:
                picture=Picture()
                picture.user=request.user
                picture.friendDynamic=friendDynamic
                picture.description=content
                from util import util_settings
                picture.picPath='%s%s' % (util_settings.RELATRVE_IMAGE_UPLOAD_PATH_M,photo)
                picture.save()
#                 pictureList.append(picture.picPath)
            del request.session['images_path']
    userProfile=UserProfile.objects.get(user_id=request.user.id)
    from pinloveweb.method import init_person_info_for_card_page
    arg.update(init_person_info_for_card_page(userProfile))
    arg=init_dynamic(request,request.user,arg)
    if request.GET.get('type')=='ajax':
        from apps.pojo.dynamic import MyEncoder
        json=simplejson.dumps( {'friendDynamicList':arg['friendDynamicList'],'next_page_number':arg['next_page_number']},cls=MyEncoder)
        return HttpResponse(json, mimetype='application/json')
    if  'images_path' in request.session:
        del request.session['images_path']
    return render(request, 'dynamic.html',arg )

'''
初始化好友动态
'''
def init_dynamic(request,user,arg):
    #查询关注的人列表
    followList=Follow.objects.filter(my=user)
    #我关注的人id列表
    followIdList=[]
    for follow in followList:
        followIdList.append(follow.follow_id)
    followIdList.append(user.id)
    friendDynamicList=FriendDynamic.objects.select_related('publishUser').filter(publishUser_id__in=followIdList).order_by('-publishTime')
    from util.page import page
    arg.update(page(request,friendDynamicList,page_num=2))
    from apps.pojo.dynamic import friendDynamicList_to_Dynamic
    friendDynamicList=friendDynamicList_to_Dynamic(arg['pages'].object_list, user.id)
    #获取点赞列表
#     friendDynamicArgeeList=FriendDynamicArgee.objects.filter(user=user)
#     argeeList=[]
#     for friendDynamic in friendDynamicList:
#         commentNum=FriendDynamic.objects.get_coment_count(friendDynamic.publishUser.id,user.id,friendDynamic.id)
#         friendDynamic.commentNum=commentNum
#         if friendDynamic.type==2:
#             friendDynamic.data=simplejson.loads(friendDynamic.data)
#         is_agreee=False  
#         for friendDynamicArgee in friendDynamicArgeeList:
#             if friendDynamic.id==friendDynamicArgee.friendDynamic_id:
#                 is_agreee=True 
#         argeeList.append(is_agreee)  
    arg['friendDynamicList']=friendDynamicList
    if arg['pages'].has_next():
        arg['next_page_number']=arg['pages'].next_page_number()
    else:
        arg['next_page_number']=-1
#     arg['argeeList']=argeeList
    return  arg
###############################################
##以上用用于1.0版
########################################
'''
 发布消息
'''
logger = logging.getLogger('django_request_logfile')
def send_dynamic(request):
    arg={}
    if request.user.is_authenticated():
        if request.method=="POST":
            flag=True
            type=request.POST.get('type').strip()
            content=request.POST.get('content').strip()
            #判断失败条件
            if int(type)>=3:
                arg['error']={'error':u'发布失败！'}
                flag=False
            if content.rstrip()=='':
                arg['error']={'error':u'发布内容不能为空！'}
                flag=False
            friendDynamic=FriendDynamic()
            friendDynamic.publishUser=request.user
            friendDynamic.type=type
            friendDynamic.content=content
            if type=='2':
                friendDynamic.data=request.session['images_path']
            friendDynamic.save()
            if type=='2':
                photoList=simplejson.loads(request.session['images_path'])
                for photo in photoList:
                    picture=Picture()
                    picture.user=request.user
                    picture.friendDynamic=friendDynamic
                    picture.description=content
                    from util import util_settings
                    picture.picPath='%s%s' % (util_settings.RELATRVE_IMAGE_UPLOAD_PATH_M,photo)
                    picture.save()
                del request.session['images_path']
            arg=init_dynamic(request.user,arg)
            if flag:
                return render(request, 'send_dynamic.html', arg,)
            else:
                return render(request, 'send_dynamic.html', arg,)
        else:
            arg=init_dynamic(request.user,arg)
            return render(request, 'send_dynamic.html', arg,)      
    else:
        return render(request, 'login.html', arg,)   

'''
 删除消息
'''
def del_dynamic(request):
    arg={}
    if request.user.is_authenticated():
        id=int(request.GET.get('id'))
        type=int(request.GET.get('type'))
        if type==1:
            FriendDynamic.objects.get(id=id).delete()
            arg['type']='success'
        elif type==2:
#             Picture.objects.filter(friendDynamic_id=id).delete()
            FriendDynamic.objects.get(id=id).delete()
            arg['type']='success'
        else:
            arg['type']='error'  
    else:
        arg['type']='login'
    json=simplejson.dumps(arg)
    return HttpResponse(json)

def dynamic_list(request):
    arg={}
    if request.user.is_authenticated():
        friendDynamicList=FriendDynamic.objects.filter(publishUser=request.user)
    else:
        return render(request, 'login.html', arg,) 
'''
上传图片
'''  
def update_photo(request): 
    if request.method == 'POST':
      if request.FILES :
        arg={}
        # uppload image
        f = request.FILES["file"]
        parser = ImageFile.Parser()  
        for chunk in f.chunks():
            parser.feed(chunk)  
        img = parser.close()
        from util import util_settings
        from util.util import random_str
        pictureName='%s%s%s%s%s' % (request.user.id,'_',time.strftime('%Y%m%d',time.localtime(time.time())),random_str(randomlength=10),f.name[f.name.find('.'):])
        if 'images_path' in request.session.keys():
            list=simplejson.loads(request.session['images_path'])
            list.append(pictureName)
            request.session['images_path']=simplejson.dumps(list)
        else:
            request.session['images_path']=simplejson.dumps([pictureName,])
        name = '%s%s' % (util_settings.IMAGE_UPLOAD_PATH_M,pictureName)
        img.save(name) 
#         return HttpResponseRedirect('/dynamic/send/')
        return HttpResponse(pictureName)

'''
删除图片
attribute:图片名称
'''
def delete_photo(request):
        try:
            pictureName=request.GET.get('pictureName')
        except:
            logger.error('获取图片名称pictureName失败')
            logging.exception('Got exception on main handler')
        if 'images_path' in request.session.keys():
            list=simplejson.loads(request.session['images_path'])
            if pictureName in list:
                list.remove(pictureName)
        from util import util_settings
        path = '%s%s' % (util_settings.IMAGE_UPLOAD_PATH_M,pictureName)
        import os
        os.remove(path)
        return HttpResponse('删除成功!')
    
def update_video(request): 
    arg={}
    if request.user.is_authenticated():
        if request.method == 'POST':
            if request.FILES :
                f = request.FILES["file"]
    else:
        return HttpResponse("请先登录")
'''
添加删除点赞
'''
def agree(request):
    arg={}
    if request.user.is_authenticated():
        try:
            id=int(request.GET.get('id'))
        except:
            arg['type']='error' 
            json=simplejson.dumps(arg)
            return json
        argeeNum=FriendDynamic.objects.get(id=id).argeeNum
        if FriendDynamicArgee.objects.filter(friendDynamic_id=id,user=request.user).exists():
            FriendDynamicArgee.objects.get(friendDynamic_id=id).delete()
            argeeNum=argeeNum-1
            FriendDynamic.objects.filter(id=id).update(argeeNum=argeeNum)
            arg['type']='delSuccess'
        else:
            friendDynamicArgee=FriendDynamicArgee()
            friendDynamicArgee.friendDynamic_id=id
            friendDynamicArgee.user=request.user
            friendDynamicArgee.save()
            argeeNum=argeeNum+1
            FriendDynamic.objects.filter(id=id).update(argeeNum=argeeNum)
            arg['type']='addSuccess'  
    else:
        arg['type']='login'
    json=simplejson.dumps(arg)
    return HttpResponse(json)
    
'''
查看评论
'''
def show_comment(request):
    arg={}
    try:
        dynamicId=int(request.GET.get('id'))
        publishUserId=int(request.GET.get('publishUserId'))
    except:
        arg['type']='error' 
        json=simplejson.dumps(arg)
        return json
    if publishUserId==request.user.id:
         commentList=FriendDynamicComment.objects.select_related('reviewer','receiver').filter(friendDynamic_id=dynamicId).order_by('-commentTime')
    else:
        from django.db.models.query_utils import Q
        commentList=FriendDynamicComment.objects.select_related('reviewer','receiver').filter(Q(friendDynamic_id=dynamicId,reviewer_id__in=[request.user.id,publishUserId],receiver_id__in=[request.user.id,publishUserId])|Q(receiver_id__isnull=True)).order_by('-commentTime')
    from apps.pojo.dynamic import FriendDynamicCommentList_to_DynamicCommentList
    dynamicCommentList=FriendDynamicCommentList_to_DynamicCommentList(commentList)
#     arg['commentList']=commentList
#     for comment in incommentList:
#     comentHtml=""
#     for comment in commentList:
#        comentHtml=comentHtml+''' <div id="comment_content_'''+str(comment.id)+'''" class="msgCnt" style="padding-bottom:0; font-size:16px">
#         <a class="fn" target="_self" uid="2"  href="">'''+str(comment.reviewer.username)+'''</a>
#         回复<a class="null" target="_blank" uid="2" rel="face" href="">'''+str(comment.receiver.username)+''''</a>
#          : '''+comment.content.encode("utf-8")+'''<em>('''+comment.commentTime.strftime("%Y-%m-%d:%H")+''')</em>
#       
#         <p class="info"><span class="right">'''
#        if comment.reviewer==request.user:
#             comentHtml=comentHtml+'''<a id="de_comment_'''+str(comment.id)+'''" onclick="del_comment('''+str(comment.id)+''')" href="javascript:void(0)">删除</a>'''
#        comentHtml=comentHtml+'''' <a onclick='reply("'''+str(comment.reviewer.username)+'''",'''+str(dynamicId)+''')' href="javascript:void(0)">回复</a></span>
#                                   </p> </div>
#        '''
#     html='%s%s%s%s%s%s%s%s%s%s%s' % ('''<div class="q_con"><div  class="new_position">
#      <textarea id="comment_''',dynamicId,'''"  class="left text" style="resize: none; overflow: hidden;" rows="1" name="comment_content" wrap="virtual"></textarea>
#     <input class="N_but" type="button" onclick="send_coment(''',dynamicId,''',''',publishUserId,''')" style="*vertical-align:middle;" value="确定">
#     <dl id="comment_list_c_''',dynamicId,'''" class="comment_list">
#     ''',comentHtml,'''</dl></div></div>''')
    from apps.pojo.dynamic import DynamicCommentEncoder
    json=simplejson.dumps(dynamicCommentList,cls=DynamicCommentEncoder)
    return HttpResponse(json)

'''
发布评论
'''
def comment(request):
        arg={}
        try:
            dynamicId=int(request.GET.get('dynamicId'))
            receiverId=request.GET.get('receiverId','')
            content=request.GET.get('content')
        except:
            arg['type']='error' 
            json=simplejson.dumps(arg)
            return HttpResponse(json)
        comment=FriendDynamicComment()
        if len(receiverId)<=0:
            friendDynamic=FriendDynamic.objects.select_related('publishUser').get(id=dynamicId)
            if friendDynamic.publishUser.id!=request.user.id:
                comment.receiver_id=friendDynamic.publishUser.id
        elif int(receiverId)==request.user.id:
            arg['type']='error' 
            arg['msg']='不能自己对自己评论'
            json=simplejson.dumps(arg)
            return HttpResponse(json)
        else:
            comment.receiver_id=receiverId
        if content.startswith(u'回复@'):
            comment.content=content[content.index(':')+1:]
        else:
            comment.content=content
        comment.friendDynamic_id=dynamicId
        comment.reviewer=request.user
        comment.save()
        commentNum=FriendDynamic.objects.get(id=dynamicId).commentNum
        FriendDynamic.objects.filter(id=dynamicId).update(commentNum=commentNum+1)
        from apps.pojo.dynamic import FriendDynamicCommentList_to_DynamicCommentList
        dynamicCommentList=FriendDynamicCommentList_to_DynamicCommentList([comment,])
        arg['type']='success'
        arg['dynamicCommentList']=dynamicCommentList
        from apps.pojo.dynamic import DynamicCommentEncoder
        json=simplejson.dumps(arg,cls=DynamicCommentEncoder)
        return HttpResponse(json)  
#         comentHtml=''' <div id="comment_content_'''+str(comment.id)+'''" class="msgCnt" style="padding-bottom:0; font-size:16px">
#         <a class="fn" target="_self" uid="2"  href="">'''+str(comment.reviewer.username)+'''</a>
#         回复<a class="null" target="_blank" uid="2" rel="face" href="">'''+str(comment.receiver.username)+''''</a>
#          : '''+content.encode("utf-8")+'''<em>('''+comment.commentTime.strftime("%Y-%m-%d:%H")+''')</em>
#         <p class="info"><span class="right">'''
#         if comment.reviewer==request.user:
#             comentHtml=comentHtml+'''<a id="de_comment_'''+str(comment.id)+'''" onclick="del_comment('''+str(comment.id)+''')" href="javascript:void(0)">删除</a>'''
#         comentHtml=comentHtml+'''' <a onclick='reply("'''+str(comment.reviewer.username)+'''",'''+str(dynamicId)+''')' href="javascript:void(0)">回复</a></span>
#                                   </p> </div>
#        '''
#         arg['conent']=comentHtml

'''
删除评论
'''
def del_comment(request):
    arg={}
    commentId=int(request.GET.get('commentId'))
    if FriendDynamicComment.objects.filter(reviewer=request.user,id=commentId).exists():
        FriendDynamicComment.objects.filter(reviewer=request.user,id=commentId).delete()
#         commentNum=FriendDynamic.objects.get(id=friendDynamicComment.friendDynamic_id).commentNum
#         FriendDynamic.objects.filter(id=friendDynamicComment.friendDynamic_id).update(commentNum=commentNum-1)
    else:
        arg['type']='error'
        arg['msg']='数据错误'
    arg['type']='success'
    json=simplejson.dumps(arg)
    return HttpResponse(json)



#用于初始化card页面所需要的信息
def init_card(arg,userProfile):
    if userProfile.avatar_name_status!='3':
        arg['avatar_name']='user_img/image.png'
    else:
        arg['avatar_name']=userProfile.avatar_name
    arg['age']=userProfile.age
    arg['height']=userProfile.height
    arg['income']=userProfile.income
    arg['education']=userProfile.get_education_display()
    arg['jobIndustry']=userProfile.get_jobIndustry_display()
    return arg
   
