# -*- encoding: utf-8 -*-
from django.conf import settings
from accounts.models import MyUserProfile, Company

from django import forms

class MyUserProfileForm(forms.ModelForm):
    confirmation = forms.BooleanField(label="下記規約に同意する")

    class Meta:
        model = MyUserProfile
        exclude = ('myuser',)

class MyUserProfileEditForm(forms.ModelForm):
    class Meta:
        model = MyUserProfile
        exclude = ('myuser',)

class CompanyEditform(forms.ModelForm):
    class Meta:
        model = Company
