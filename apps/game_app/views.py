#-*- coding: UTF-8 -*- 
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson
from apps.game_app.models import Yuanfenjigsaw, get_count
from apps.the_people_nearby.tt import request



@csrf_exempt
def jigsaw(request):
    match_result = Yuanfenjigsaw(request).get_match_result()
    json=simplejson.dumps(match_result)
    return HttpResponse(json, mimetype='application/javascript')

def pintu(request):
    count = get_count(request)
    return render(request, 'pintu.html',{'count':count})


'''
获取facebook授权登录地址,跳转到回调地址（redirect_uri）
'''
@csrf_exempt
def facebook_login_url(request):
    from apps.third_party_login_app.facebook import auth_url
    from apps.third_party_login_app.setting import FaceBookAppID
    url=auth_url(FaceBookAppID,'http://pinpinlove.com/game/pintu_for_facebook/')
    from django.http.response import HttpResponseRedirect
    return HttpResponseRedirect(url)
@csrf_exempt
def pintu_for_facebook(request):
    return render(request, 'pintu_for_facebook.html',)