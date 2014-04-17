# -*- coding: utf-8 -*-
'''
Created on 2014年4月17日

@author: jin
'''
from django.core.management.base import BaseCommand
class Command(BaseCommand):
    def handle(self, *args, **options):
        from apps.user_score_app.method import reset_count
        reset_count()
        self.stdout.write('score cache reset success!')