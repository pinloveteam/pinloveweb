# -*- coding: utf-8 -*-
'''
Created on Sep 1, 2013

@author: jin
'''
#分页
# Attributes:
#    querySet 分页数据集
#    page_num 每页显示的数目, 默认是10
#      after_range_num: int类型, 默认是4
#     bevor_range_num: int类型, 默认是4
#     current_page: int 当前页数,must
from util.util_settings import PAGE_NUM, BEVOR_RANGE_NUM, AFTER_RANGE_NUM
from django.core.paginator import Paginator
from django.db.models.query import RawQuerySet
def page(request,querySet,**kwargs):
     after_range_num = kwargs.get('after_range_num', AFTER_RANGE_NUM)
     bevor_range_num = kwargs.get('bevor_range_num', BEVOR_RANGE_NUM)
     per_page_num = kwargs.get('page_num', PAGE_NUM)
     
     try:
         page=int(request.GET.get('page', '1'))
         if page<1:
             page=1
     except:
         page=1
     paginator =Paginator(querySet,per_page_num)
     
     try:
        if type(querySet)==RawQuerySet:
            paginator._count = len(list(querySet))
            pages = paginator.page(page)
        else:
            pages = paginator.page(page)
     except:
        pages = paginator.page(1)
     if page >= after_range_num:
        page_range = paginator.page_range[page-after_range_num:page+bevor_range_num]
     else:
        page_range = paginator.page_range[0:int(page)+bevor_range_num]
     return {'pages': pages, 'page_range': page_range}


#原始sql查询分页
# Attributes:
#    querySet 分页数据集
#    page_num 每页显示的数目, 默认是10
#      after_range_num: int类型, 默认是4
#     bevor_range_num: int类型, 默认是4
#     current_page: int 当前页数,must      
# def raw_sql_page(request,sql,**kwargs):
#      after_range_num = kwargs.get('after_range_num', AFTER_RANGE_NUM)
#      bevor_range_num = kwargs.get('bevor_range_num', BEVOR_RANGE_NUM)
#      per_page_num = kwargs.get('page_num', PAGE_NUM)
#      
#      try:
#          page=int(request.GET.get('page', '1'))
#          if page<1:
#              page=1
#      except:
#          print "数据转换出错！"
#          pass
#      sql+=" limit "+per_page_num*(page-1)+","+per_page_num*page
#      
#      