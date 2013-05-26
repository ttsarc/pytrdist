# -*- encoding: utf-8 -*-
import datetime
from django import forms
from django.forms.widgets import RadioSelect
from documents.models import Document,DocumentCategory
from documents.choices import STAGE_CHOICE
from trwk.libs.fields import confirmation_field


class DocumentForm(forms.ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'
    #cagtegory = forms.ModelMultipleChoiceField(
    #    widget=forms.CheckboxSelectMultiple(),
    #    queryset=DocumentCategory.objects.all(),
    #    required=True)

    class Meta:
        model = Document
        exclude = ('user', 'company', 'download_status', 'notable_rank')


class DownloadForm(forms.Form):
    error_css_class = 'error'
    required_css_class = 'required'
    stage = forms.ChoiceField(
        label='現在のご状況',
        choices=STAGE_CHOICE,
        widget=RadioSelect)
    confirmation = confirmation_field()


class LeadSearchForm(forms.Form):
    date_format = ['%Y/%m/%d', '%Y-%m-%d']
    start_date = forms.DateField(
        label='開始',
        input_formats=date_format,
        required=False)
    end_date = forms.DateField(
        label='終了',
        input_formats=date_format,
        initial=datetime.date.today().strftime('%Y/%m/%d'),
        required=False)
