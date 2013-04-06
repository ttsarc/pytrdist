# -*- encoding: utf-8 -*-
from django.conf import settings
from accounts.models import MyUserProfile

from django.forms import ModelForm

class MyUserProfileForm(ModelForm):
    class Meta:
        model = MyUserProfile
        exclude = ('myuser',)

