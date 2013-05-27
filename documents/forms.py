# -*- encoding: utf-8 -*-
import datetime
from django import forms
from django.forms.widgets import RadioSelect
from documents.models import Document, DocumentCategory
from documents.choices import STAGE_CHOICE
from trwk.libs.fields import confirmation_field


class DocumentForm(forms.ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'
    Cat = DocumentCategory
    category_choice = [
        #optgroupで使われるテキスト
        [top.name, [
            #optionで使われるvalue、ラベル
            [sub.pk, sub.name]
            #下で取得した親カテゴリごとの子カテゴリを取得
            for sub in Cat.objects.filter(parent=top.pk).order_by('pk')
        ]]
        #親カテゴリを取得
        for top in Cat.objects.filter(parent=None).order_by('pk')
    ]
    category = forms.MultipleChoiceField(
        choices=category_choice,
        required=True,
        label='カテゴリ',
        #最大数はadd_edit.htmlのjs側で変更
        help_text='最大3つまで選択出来ます')

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
