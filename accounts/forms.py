# -*- encoding: utf-8 -*-
from django.conf import settings
from accounts.models import MyUserProfile, Company

from django import forms
from django.contrib.formtools.preview import FormPreview

class MyUserProfileForm(forms.ModelForm):
    confirmation = forms.BooleanField(label="下記規約に同意する")
    error_css_class = 'error'
    required_css_class = 'required'
    class Meta:
        model = MyUserProfile
        exclude = ('myuser',)

class MyUserProfilePreviewForm(FormPreview):
    def done(self, request, cleaned_data):
        return HttpResponseRedirect('/')


class MyUserProfileEditForm(forms.ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'
    class Meta:
        model = MyUserProfile
        exclude = ('myuser',)

class CompanyEditform(forms.ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'
    class Meta:
        model = Company
