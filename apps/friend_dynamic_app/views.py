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
from django.http.response import HttpResponseRedirect, HttpResponse
import time
import simplejson
from apps.user_app.models import UserProfile, Friend
from django.db import connection
'''
 发布消息
'''
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
初始化好友动态
'''
def init_dynamic(user,arg):
    #查询关注的人列表
    followList=Friend.objects.filter(my=user)
    #我关注的人id列表
    followIdList=[]
    for friend in followList:
        followIdList.append(friend.friend_id)
    followIdList.append(user.id)
    friendDynamicList=FriendDynamic.objects.filter(publishUser_id__in=followIdList).order_by('-publishTime')[0:8]
    #获取点赞列表
    friendDynamicArgeeList=FriendDynamicArgee.objects.filter(user=user)
    argeeList=[]
    for friendDynamic in friendDynamicList:
        if friendDynamic.type==2:
            friendDynamic.data=simplejson.loads(friendDynamic.data)
        is_agreee=False  
        for friendDynamicArgee in friendDynamicArgeeList:
            if friendDynamic.id==friendDynamicArgee.friendDynamic_id:
                is_agreee=True 
        argeeList.append(is_agreee)  
    arg['friendDynamicList']=friendDynamicList
    arg['argeeList']=argeeList
    return  arg

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
        # uppload image
        f = request.FILES["file"]
        parser = ImageFile.Parser()  
        for chunk in f.chunks():
            parser.feed(chunk)  
        img = parser.close()
        from util.common_util import random_str
        from util import util_settings
        pictureName='%s%s%s%s%s' % (request.user.id,'_',time.strftime('%Y%m%d',time.localtime(time.time())),random_str(randomlength=10),f.name[f.name.find('.'):])
        if 'images_path' in request.session.keys():
            list=simplejson.loads(request.session['images_path'])
            list.append(pictureName)
            request.session['images_path']=simplejson.dumps(list)
        else:
            request.session['images_path']=simplejson.dumps([pictureName,])
        name = '%s%s' % (util_settings.IMAGE_UPLOAD_PATH_M,pictureName)
        img.save(name) 
        return HttpResponseRedirect('/dynamic/send/')
#     return render(request, 'test111.html',)   
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
            agreeStatus=request.GET.get('agreeStatus')
        except:
            arg['type']='error' 
            json=simplejson.dumps(arg)
            return json
        argeeNum=FriendDynamic.objects.get(id=id).argeeNum
        if agreeStatus=="True":
            FriendDynamicArgee.objects.get(friendDynamic_id=id).delete()
            argeeNum=argeeNum-1
            FriendDynamic.objects.filter(id=id).update(argeeNum=argeeNum)
            arg['type']='delSuccess'
        else:
            if FriendDynamicArgee.objects.filter(friendDynamic_id=id,user=request.user).exists():
               arg['type']='error' 
               json=simplejson.dumps(arg)
               return json 
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
         commentList=FriendDynamicComment.objects.select_related().filter(friendDynamic_id=dynamicId).order_by('-commentTime')
    else:
        commentList=FriendDynamicComment.objects.select_related().filter(friendDynamic_id=dynamicId,reviewer_id__in=[request.user.id,publishUserId],receiver_id__in=[request.user.id,publishUserId]).order_by('-commentTime')
    arg['commentList']=commentList;
    comentHtml=""
    for comment in commentList:
       comentHtml=comentHtml+''' <div id="comment_content_'''+str(comment.id)+'''" class="msgCnt" style="padding-bottom:0; font-size:16px">
        <a class="fn" target="_self" uid="2"  href="">'''+str(comment.reviewer.username)+'''</a>
        回复<a class="null" target="_blank" uid="2" rel="face" href="">'''+str(comment.receiver.username)+''''</a>
         : '''+comment.content.encode("utf-8")+'''<em>('''+comment.commentTime.strftime("%Y-%m-%d:%H")+''')</em>
      
        <p class="info"><span class="right">'''
       if comment.reviewer==request.user:
            comentHtml=comentHtml+'''<a id="de_comment_'''+str(comment.id)+'''" onclick="del_comment('''+str(comment.id)+''')" href="javascript:void(0)">删除</a>'''
       comentHtml=comentHtml+'''' <a onclick='reply("'''+str(comment.reviewer.username)+'''",'''+str(dynamicId)+''')' href="javascript:void(0)">回复</a></span>
                                  </p> </div>
       '''
    html='%s%s%s%s%s%s%s%s%s%s%s' % ('''<div class="q_con"><div  class="new_position">
     <textarea id="comment_''',dynamicId,'''"  class="left text" style="resize: none; overflow: hidden;" rows="1" name="comment_content" wrap="virtual"></textarea>
    <input class="N_but" type="button" onclick="send_coment(''',dynamicId,''',''',publishUserId,''')" style="*vertical-align:middle;" value="确定">
    <dl id="comment_list_c_''',dynamicId,'''" class="comment_list">
    ''',comentHtml,'''</dl></div></div>''')
    json=simplejson.dumps(html)
    return HttpResponse(json)

'''
发布评论
'''
def comment(request):
    arg={}
    if request.user.is_authenticated():
        try:
            dynamicId=int(request.GET.get('dynamicId'))
            publishUserId=int(request.GET.get('publishUserId'))
            content=request.GET.get('content')
        except:
            arg['type']='error' 
            json=simplejson.dumps(arg)
            return json
        comment=FriendDynamicComment()
        if content.startswith(u'回复@'):
            end = content.find(u':')
            username=content[3:end]
            from django.contrib.auth.models import User
            user=User.objects.get(username=username)
            comment.receiver_id=user.id 
        else:
          comment.receiver_id=publishUserId  
        comment.friendDynamic_id=dynamicId
        comment.reviewer=request.user
        comment.content=content
        comment.save()
        commentNum=FriendDynamic.objects.get(id=dynamicId).commentNum
        FriendDynamic.objects.filter(id=dynamicId).update(commentNum=commentNum+1)
        arg['type']='success'
        comentHtml=''' <div id="comment_content_'''+str(comment.id)+'''" class="msgCnt" style="padding-bottom:0; font-size:16px">
        <a class="fn" target="_self" uid="2"  href="">'''+str(comment.reviewer.username)+'''</a>
        回复<a class="null" target="_blank" uid="2" rel="face" href="">'''+str(comment.receiver.username)+''''</a>
         : '''+content.encode("utf-8")+'''<em>('''+comment.commentTime.strftime("%Y-%m-%d:%H")+''')</em>
        <p class="info"><span class="right">'''
        if comment.reviewer==request.user:
            comentHtml=comentHtml+'''<a id="de_comment_'''+str(comment.id)+'''" onclick="del_comment('''+str(comment.id)+''')" href="javascript:void(0)">删除</a>'''
        comentHtml=comentHtml+'''' <a onclick='reply("'''+str(comment.reviewer.username)+'''",'''+str(dynamicId)+''')' href="javascript:void(0)">回复</a></span>
                                  </p> </div>
       '''
        arg['conent']=comentHtml
    else:
        arg['type']='login'
    json=simplejson.dumps(arg)
    return HttpResponse(json)   

'''
删除评论
'''
def del_comment(request):
    arg={}
    commentId=int(request.GET.get('commentId'))
    friendDynamicComment=FriendDynamicComment.objects.get(id=commentId)
    friendDynamicComment.delete()
    commentNum=FriendDynamic.objects.get(id=friendDynamicComment.friendDynamic_id).commentNum
    FriendDynamic.objects.filter(id=friendDynamicComment.friendDynamic_id).update(commentNum=commentNum-1)
    arg['type']='success'
    json=simplejson.dumps(arg)
    return HttpResponse(json)


'''
卡片界面动态
'''
def dynamic(request):
    arg={}
    if request.user.is_authenticated():
        userProfile=UserProfile.objects.get(user_id=request.user.id)
        #关注
        myFollow=Friend.objects.filter(my=request.user).count()
        fans=Friend.objects.filter(friend=request.user).count()
        sql="select my_id from user_app_friend where friend_id="+str(request.user.id)+" and my_id in (SELECT friend_id from user_app_friend where my_id="+str(request.user.id)+") "
        cursor=connection.cursor();
        cursor.execute(sql)
        follow=cursor.fetchall()
        arg=init_dynamic(request.user,arg)
  
    
        arg=init_card(arg,userProfile)
        arg['myFollow']=myFollow
        arg['fans']=fans
        arg['follow']=len(follow)  
        return render(request, 'dynamic.html',arg )
    else:
        return render(request,'login.html',arg)
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
     
