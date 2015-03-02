# -*- coding: utf-8 -*-
'''
Created on Nov 7, 2013

@author: jin
'''
import string
import random
import urllib 
from json import loads, JSONEncoder
 
from django.core.serializers import serialize
from django.db.models.query import QuerySet
from django.utils import simplejson
from apps.user_app.models import UserProfile
import re
'''
生成长度固定的字符串
'''
def random_str(randomlength=32):
    a = list(string.ascii_letters)
    random.shuffle(a)
    return ''.join(a[:randomlength])
 
def download_pic(url,filename):
#     urllib.urlretrieve(url, "00000001.jpg")
    data = urllib.urlopen(url).read() 
    f = file(filename,"wb") 
    f.write(data) 
    f.close() 
     
class DjangoJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, QuerySet):
            # `default` must return a python serializable
            # structure, the easiest way is to load the JSON
            # string produced by `serialize` and return it
            return loads(serialize('json', obj))
        return JSONEncoder.default(self,obj)
'''
转换类成dict
instance[class]:类
fields:属性
'''   
def model_to_dict(instance,fields=None):
    list=[]
    for object in instance:
        args={}
        for field in fields:
            if field.find('.')!=-1:
                fieldList=field.split('.')
                attr = object
                for f in fieldList:
                    attr = getattr(attr, f)
                args[fieldList[len(fieldList)-1]]=attr
            else:
                args[field]=getattr(object,field)
        list.append(args)
    return list
 
 
'''
匹配表情
'''  
def regex_expression(content):
    if not isinstance(content,basestring):
        return content
    regex=u'{:pinlove_(?:7[0-5]|[1-6][0-9]|[1-9]):}'
    return re.sub(regex, dashrepl, content)
 
def dashrepl(matchobj):
    s=matchobj.group(0)
    num=s[10:-2]
    return '%s%s%s' % ('<img src="/static/img/arclist/',num,'.png" style="width: 24px; height: 24px;">')
 
'''
匹配字符串里的连接
'''
def regex_url(content):
    if not isinstance(content,basestring):
        return content
    regex=u'((http|ftp|https)://)(([a-zA-Z0-9\._-]+\.[a-zA-Z]{2,6})|([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}))(:[0-9]{1,4})*(/[a-zA-Z0-9\&%_\./-~-]*)?'
    return re.sub(regex, dashrepl_url, content)
 
def dashrepl_url(matchobj):
    s=matchobj.group(0)
    return '%s%s%s%s%s' % ('<a target="_blank" href="',s,'">',s,'</a>')

'''
判断是否引导过
attridute:
guide[UserProfile.guide] UserProfile的引导字段
guideField[string]  引导类型    
                     value: 对比 compareButton
return
  false 未引导
'''
def is_guide(userId,guide,guideField):
    if guide==None:
        guideDict={}
    else:
        guideDict=simplejson.loads(guide)
    if not guideDict.get(guideField,False):
        guideDict[guideField]=True
        guideDict=simplejson.dumps(guideDict)
        UserProfile.objects.filter(user_id=userId).update(guide=guideDict)
        return False
    else:
        return True
    
'''
距离现在的时间
@param dateTime:datetime 
'''
   

def time_for_now(dateTime):
    import calendar
    import datetime
    now=datetime.datetime.today()
    monthRange = calendar.monthrange(now.year,now.month)[1]
    print monthRange
    timedelta=(now-dateTime)
    second=timedelta.total_seconds()
    print second
    if timedelta.days>=365:
        return  '%s%s'%(now.year-dateTime.year,'年以前')
    elif timedelta.days>=monthRange:
        return  '%s%s'%(((now.year-dateTime.year)*12+(now.month-dateTime.month)),'月以前')
    elif  second>=60*60*24:
        return  '%s%s'%(int(second/(60*60*24)),'天以前')
    elif second<60*60*24 and second>=60*60:
        return '%s%s'%(int(second/(60*60)),'小时以前')
    elif second<60*60 and second>=60:
        return '%s%s'%(int(second/60),'分钟以前')
    elif second<60:
        return  '刚刚'
        return  '%s%s'%(second,'秒')
 
    
'''
验证评论，动态内容
'''
def verify_content(content,limit_length):
    content=content.strip()
    p = re.compile('[\n\r]*')
    content=p.sub('',content)
    if content.rstrip()=='':
        raise Exception('内容不能为空!')
    elif len(content.rstrip())>limit_length:
        raise Exception('%s%s%s'%('内容长度不得大于',limit_length,'!'))
    from django.utils.html import escape
    content=escape(content)
    return content