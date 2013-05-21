# -*- encoding: utf-8 -*-
from django import forms
from accounts.models import MyUser, MyUserProfile, Company
from trwk.libs.fields import confirmation_field


class MyUserProfileForm(forms.ModelForm):
    confirmation = confirmation_field()
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
        exclude = ('slug_name', 'status')


class CompanyEntryform(forms.ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'
    note = forms.CharField(
        label="備考",
        max_length=500,
        widget=forms.Textarea,
        required=False)
    confirmation = confirmation_field()
    website = forms.CharField(required=False, label="空のままにしてください（スパム対策）")

    def clean_website(self):
        if self.cleaned_data['website']:
            raise forms.ValidationError("Invalid form")
        return ''

    class Meta:
        model = Company
        exclude = ('slug_name', 'status', 'logo_file')


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
