#-*- coding: UTF-8 -*- 
from django.contrib.auth.models import User
from apps.game_app import jigswgl
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson
from apps.user_app.models import UserProfile
import datetime

@csrf_exempt
def jigsaw(request):
    selected=request.POST.get("selected",'')
    currentuser = request.user.username
    gender = UserProfile.objects.get(user=request.user).gender
    selected_set = [int(i) for i in selected.split("-") if i]#用户提交的集合
    cha1 = jigswgl.UNIVERSAL_SET - set(selected_set)#与之互补的集合
    cha2 = set(selected_set) - jigswgl.UNIVERSAL_SET
    
    if cha1 == jigswgl.UNIVERSAL_SET or cha1 == set([]) or cha2 != set([]):
        message = [{'message':'1'}]
        return HttpResponse(simplejson.dumps(message), mimetype='application/javascript')
    if jigswgl.JIGSW_COUNT.get(currentuser) == 0:
        message = [{'message':'2'}]
        return HttpResponse(simplejson.dumps(message), mimetype='application/javascript')
    if gender == 'M':
        jigswgl.JIGSW_BOYS[str(set(selected_set))] = currentuser#如果位男性，则将其存入JIGSW_BOYS
        otherone = jigswgl.JIGSW_GIRLS.get(str(cha1))#从JIGSW_GIRLS中寻找与之互补的异性
    else :
        jigswgl.JIGSW_GIRLS[str(set(selected_set))] = currentuser#同上
        otherone = jigswgl.JIGSW_BOYS.get(str(cha1))
    #游戏计数    
    if jigswgl.JIGSW_COUNT.get(currentuser) == None:
        jigswgl.JIGSW_COUNT[currentuser] = jigswgl.COUNT - 1
    else:
        jigswgl.JIGSW_COUNT[currentuser] = jigswgl.JIGSW_COUNT.get(currentuser) - 1
    #如果otherone不为空，表示找到匹配异性将其姓名，年龄，身高，头像传至前台
    if otherone != None:
        print otherone
        otheruser = UserProfile.objects.get(user=User.objects.get(username=otherone))
        message = [{'message':otherone,'height':otheruser.height,'age':otheruser.age,'avatar_name':otheruser.avatar_name,'count':jigswgl.JIGSW_COUNT.get(currentuser)}]
        return HttpResponse(simplejson.dumps(message), mimetype='application/javascript')#message为1表示前台提交的数据有错，或者已经参加过游戏
    else:
        message = [{'message':'0','count':jigswgl.JIGSW_COUNT.get(currentuser)}]
        return HttpResponse(simplejson.dumps(message), mimetype='application/javascript') 

def pintu(request):
    if jigswgl.TODAY != datetime.date.today():
        jigswgl.JIGSW_GIRLS = {} #存放girl数据
        jigswgl.JIGSW_BOYS = {}  #存放boy数据
        jigswgl.JIGSW_COUNT = {} #游戏次数
        jigswgl.TODAY = datetime.date.today()
    count = jigswgl.JIGSW_COUNT.get(request.user.username)
    if count == None:
        count = jigswgl.COUNT
    return render(request, 'pintu.html',{'count': count})
