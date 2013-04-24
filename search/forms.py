# -*- encoding: utf-8 -*-
from django.conf import settings
from django import forms
from accounts.validators import TelFaxValidaor

class SearchForm(forms.Form):
    error_css_class = 'error'
    required_css_class = 'required'
    keyword = forms.CharField(label="キーワード")
