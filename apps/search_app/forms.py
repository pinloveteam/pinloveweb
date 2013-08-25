# -*- coding: utf-8 -*-

from django import forms 
from django.contrib.auth.models import User 
from django.forms import ModelForm
from django.utils.translation import ugettext, ugettext_lazy as _

from apps.user_app.models import user_basic_profile, user_contact_link,\
    user_appearance, user_study_work, user_hobby_interest,\
    user_family_information, user_personal_habit, user_family_life
from apps.user_app import user_validators

