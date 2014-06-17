'''

@author: jin
'''
from django.contrib.auth.models import User
for i in range(3,14):User.objects.filter(id=i).delete()