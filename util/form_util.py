# -*- coding: utf-8 -*-
'''
Created on Aug 17, 2013

@author: jin
'''
#radio 按键的样式
from django import forms
from django.utils.safestring import mark_safe
class HorizRadioRenderer(forms.RadioSelect.renderer):
    """ this overrides widget method to put radio buttons horizontally
        instead of vertically.
    """
    def render(self):
            """Outputs radios"""
            return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))
