'''
Created on 2013-6-27

@author: jin
'''
from django.db import models
class User(models.Model):
    userId=models.AutoField(primary_key=True,max_length=8)
    username=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    trueName=models.CharField(default = '',max_length=50)
    email=models.EmailField(max_length=128)
    age=models.IntegerField(max_length=8)
    sex=models.CharField(max_length=1)
    address=models.CharField(max_length=255)
    mobilePhone=models.CharField(max_length=50)
    height=models.IntegerField(max_length=8)
    birthday=models.DateField()
    job=models.CharField(max_length=50)
    position=models.CharField(max_length=50)
    educate=models.CharField(max_length=50)
    payRang=models.CharField(max_length=50)
    hobby=models.CharField(default = '',max_length=255)
    evaluate=models.TextField(default = '')
    marriageState=models.CharField(max_length=1)
    checkState=models.CharField(max_length=1)
    stauts=models.CharField(max_length=1)
    
class Friend(models.Model):
    myId=models.ForeignKey(User,related_name='user_myId')
    friendId=models.ForeignKey(User,related_name='user_friendId')
    type=models.CharField(max_length=1)
    
class Message(models.Model):
    messageId=models.AutoField(primary_key=True,max_length=8)
    fromId=models.ForeignKey(User,related_name='User_fromId')
    toId=models.ForeignKey(User,related_name='User_toId')
    messageContent=models.TextField()
    sendTime=models.DateTimeField()
    type=models.CharField(max_length=1)
    
class new(models.Model):
    newId=models.AutoField(primary_key=True,max_length=8)
    userId=models.ForeignKey(User,related_name='User_userId')
    createTime=models.DateTimeField()
    contentText=models.CharField(max_length=255)
    picture_path=models.ImageField(upload_to='user_img',max_length=128)
    video_path=models.CharField(max_length=128)
    commentNum=models.IntegerField(default=0)
    shareNum=models.IntegerField(default=0)
    type=models.CharField(max_length=1)