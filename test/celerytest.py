'''
Created on Nov 28, 2013

@author: jin
'''
from celery.app import task

@task
def add(x, y):
  return x + y