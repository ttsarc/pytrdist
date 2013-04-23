# -*- encoding: utf-8 -*-
from django.conf import settings
from django import forms
from accounts.models import MyUser, MyUserProfile, Company

class MyUserProfileForm(forms.ModelForm):
    confirmation = forms.BooleanField(label="下記規約に同意する")
    error_css_class = 'error'
    required_css_class = 'required'
    class Meta:
        model = MyUserProfile
        exclude = ('myuser',)

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
        exclude = ('slug_name','status')

class MyUserShowForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ('email',)

class MyUserProfileShowForm(forms.ModelForm):
    class Meta:
        model = MyUserProfile
        fields = (
            'last_name',
            'first_name',
            'last_name_kana',
            'first_name_kana',
            'company_name',
            'tel',
            'fax',
            'post_number',
            'prefecture',
            'address',
            'site_url',
            'department',
            'position',
            'position_class',
            'business_type',
            'job_content',
            'firm_size',
            'yearly_sales',
            'discretion',
        )
