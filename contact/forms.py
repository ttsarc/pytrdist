# -*- encoding: utf-8 -*-
from django.conf import settings
from django import forms

class ContactForm(forms.Form):
    confirmation = forms.BooleanField(label="利用規約に同意する")
    error_css_class = 'error'
    required_css_class = 'required'


