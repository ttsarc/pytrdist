# -*- encoding: utf-8 -*-
from django import forms


class SearchForm(forms.Form):
    error_css_class = 'error'
    required_css_class = 'required'
    keyword = forms.CharField(label="キーワード", max_length=16)
