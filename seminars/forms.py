# -*- encoding: utf-8 -*-
import datetime
from django import forms
from seminars.models import Seminar, SeminarCategory
from trwk.libs.fields import confirmation_field


class SeminarForm(forms.ModelForm):
    date_format = ['%Y/%m/%d', '%Y-%m-%d', ]
    datetime_format = [
        '%Y/%m/%d %H:%M',
        '%Y-%m-%d %H:%M:%S',
        '%Y/%m/%d %H:%M:%S',
    ]
    exhibition_date = forms.DateField(
        label='開催日',
        input_formats=date_format,
        help_text='例：2013-05-01')
    close_date = forms.DateField(
        label='終了日',
        input_formats=date_format,
        required=False,
        help_text='例：2013-05-10 一定の期間開催する場合はご記入ください。')
    limit_datetime = forms.DateTimeField(
        label='申し込み終了時間',
        input_formats=datetime_format)
    error_css_class = 'error'
    required_css_class = 'required'
    Cat = SeminarCategory
    category_choice = [
        [top.name, [
            [sub.pk, sub.name]
            for sub in Cat.objects.filter(parent=top.pk).order_by('pk')
        ]]
        for top in Cat.objects.filter(parent=None).order_by('pk')
    ]
    category = forms.MultipleChoiceField(
        choices=category_choice,
        required=True,
        label='カテゴリ',
        #最大数はadd_edit.htmlのjs側で変更
        help_text='最大3つまで選択出来ます')

    class Meta:
        model = Seminar
        exclude = ('user', 'company', 'notable_rank')


class EntryForm(forms.Form):
    error_css_class = 'error'
    required_css_class = 'required'
    note = forms.CharField(
        label="備考",
        max_length=500,
        widget=forms.Textarea,
        required=False)
    confirmation = confirmation_field()


class LeadSearchForm(forms.Form):
    date_format = ['%Y/%m/%d', '%Y-%m-%d', ]
    start_date = forms.DateField(
        label='開始',
        input_formats=date_format,
        required=False)
    end_date = forms.DateField(
        label='終了',
        input_formats=date_format,
        initial=datetime.date.today().strftime('%Y/%m/%d'),
        required=False)
