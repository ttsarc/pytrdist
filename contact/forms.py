# -*- encoding: utf-8 -*-
from django.conf import settings
from django import forms
from accounts.validators import TelFaxValidaor

class ContactForm(forms.Form):
    TYPE_CHOICES = (
        ('掲載について','掲載について'),
        ('ユーザー登録について','ユーザー登録について'),
        ('サイトについて','サイトについて'),
        ('取材について','取材について'),
        ('その他','その他'),
    )
    type = forms.ChoiceField(choices=TYPE_CHOICES, label="お問い合わせ種別")
    company_name = forms.CharField(label="会社名")
    department = forms.CharField(label='部署名', required=False)
    last_name = forms.CharField(label="姓")
    first_name = forms.CharField(label="名")
    tel = forms.CharField(label="電話番号", validators=[TelFaxValidaor], help_text='例：03-3343-5746')
    fax = forms.CharField(label="FAX", validators=[TelFaxValidaor], help_text='例：03-5326-0360', required=False)
    email = forms.EmailField(label='メールアドレス')
    site_url = forms.URLField(label='ホームページURL', required=False)
    message = forms.CharField(label="お問い合わせ内容", max_length=2000, widget=forms.Textarea)
    confirmation = forms.BooleanField(label="利用規約に同意する")
    error_css_class = 'error'
    required_css_class = 'required'

