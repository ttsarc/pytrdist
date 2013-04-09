# -*- encoding: utf-8 -*-
from django.conf import settings
from django import forms
from documents.models import Document

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        exclude = ('user', 'company')
