# -*- encoding: utf-8 -*-
import datetime
from django.conf import settings
from django import forms
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple, SubWidget
from documents.models import Document
from documents.choices import STAGE_CHOICE
from django.utils.encoding import force_text, python_2_unicode_compatible

class DocumentForm(forms.ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'
    class Meta:
        model = Document
        exclude = ('user', 'company','download_status')

class DownloadForm(forms.Form):
    error_css_class = 'error'
    required_css_class = 'required'
    stage = forms.ChoiceField(label='現在のご状況',choices=STAGE_CHOICE, widget=RadioSelect)
    confirmation = forms.BooleanField(label="規約に同意する")


class LeadSearchForm(forms.Form):
    date_format = ['%Y/%m/%d', '%Y-%m-%d',]
    start_date = forms.DateField(label='開始', input_formats=date_format, required=False)
    end_date = forms.DateField(label='終了', input_formats=date_format, initial=datetime.date.today().strftime('%Y/%m/%d'), required=False)
