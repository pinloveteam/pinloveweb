# -*- coding: utf-8 -*-
'''
Created on 2014年2月17日

@author: jin
'''
from django.shortcuts import render
def apprequest_test(request):
    from apps.third_party_login_app.models import FacebookUser
    user= FacebookUser.objects.get(uid='100007247470289')
    from apps.game_app.models import get_count
    from apps.game_app.models import get_game_count_forever
    count=get_count(user.username)+get_game_count_forever('100007247470289')
    request.session['apprequest']=['100007203789389','100007563789389','100007203789332']
    users=[{'uid':'100007203789389','username':'Jin Snail'},{'uid':'100007563789389','username':'Jin sd'},{'uid':'100007203789332','username':'Jin er'}]
    return render(request, 'pintu_for_facebook.html',{'uid':user.uid,'price':user.price,'count':count,'data':users,'userCount':len(users)})
   
   
