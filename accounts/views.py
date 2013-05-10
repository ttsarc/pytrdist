# -*- encoding: utf-8 -*-
"""
Views which edit user accounts

"""
from django import forms
from django.shortcuts import redirect, render_to_response, get_object_or_404, get_list_or_404
from django.template import RequestContext
from django.template.loader import render_to_string
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.sites.models import RequestSite, Site
from django.conf import settings
from django.core.mail import send_mail
from registration.forms import ChangeEmailForm
from registration.backends import get_backend
from registration.models import RegistrationProfile, ChangeEmailProfile
from accounts.forms import MyUserProfileEditForm, CompanyEditform, CompanyEntryform
from accounts.models import MyUserProfile, Company
from trwk.libs.request_utils import set_next_url, get_next_url
from documents.models import Document
from seminars.models import Seminar
from blog.models import Post
from django.core.mail import mail_admins

@login_required
def mypage_home(request):
    member_info = Post.objects.filter(status=1,category__in=[2,])[0:5]
    customer_info = None
    if request.user.is_customer():
        customer_info = Post.objects.filter(status=1,category__in=[3,])[0:5]

    return render_to_response(
        'accounts/mypage.html',
        {
            'member_info'   : member_info,
            'customer_info' : customer_info,
        },
        context_instance=RequestContext(request)
    )

@login_required
@csrf_protect
def mypage_edit_profile(request):
    user_pk = request.user.pk
    current_profile = MyUserProfile.objects.get(myuser=user_pk)
    set_next_url(request)
    if request.method == 'POST':
        form = MyUserProfileEditForm(request.POST, instance=current_profile)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'ユーザー情報の変更に成功しました')
            if get_next_url(request):
                return redirect(get_next_url(request))
            else:
                return redirect('mypage_home')
    else:
        form = MyUserProfileEditForm(instance=current_profile)

    return render_to_response(
        'accounts/edit_profile.html',
        {
            'form' : form,
        },
        context_instance=RequestContext(request)
    )
@login_required
@csrf_protect
def mypage_edit_company(request):
    company = request.user.customer_company
    if not company:
        messages.add_message(request, messages.ERROR, '掲載企業が登録されていません')
        return redirect('mypage_home')
    current_company = Company.objects.get(pk=company.pk)
    if request.method == 'POST':
        form = CompanyEditform(request.POST, request.FILES, instance=current_company)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, '掲載企業情報を保存しました')
            return redirect('mypage_home')
    else:
        form = CompanyEditform(instance=current_company)

    return render_to_response(
        'accounts/edit_company.html',
        {
            'form' : form,
        },
        context_instance=RequestContext(request)
    )

def _notify_company_entry(form, request):
    content = render_to_string(
        'email/company_entry.txt',
        {'form' : form},
        context_instance=RequestContext(request)
    )
    subject = render_to_string(
        'email/company_entry_subject.txt',
        {'form' : form},
        context_instance=RequestContext(request)
    )
    subject = subject.replace("\n","")
    send_mail(subject=subject, message=content, from_email=settings.SERVER_EMAIL, recipient_list=[settings.CONTACT_EMAIL,])
    mail_admins(subject=subject, message=content)

def company_entry(request):
    if request.method == 'POST':
        form = CompanyEntryform(request.POST)
        if form.is_valid():
            messages.add_message(request, messages.SUCCESS, '掲載企業のお申し込みありがとうございます。後ほど担当者よりご連絡させて頂きます。')
            _notify_company_entry(form, request)
            return redirect('home')
    else:
        form = CompanyEntryform()

    return render_to_response(
        'accounts/company_entry.html',
        {
            'form' : form,
        },
        context_instance=RequestContext(request)
    )

def company_detail(request, company_id):
    company = get_object_or_404(Company, pk=company_id, status=1)

    documents = Document.objects.filter(company=company_id).order_by('-update_date')[0:10]
    seminars = Seminar.objects.filter(company=company.id).order_by('-update_date')[0:10]
    return render_to_response(
        'accounts/company_detail.html',
        {
            'company' : company,
            'documents' : documents,
            'seminars' : seminars,
        },
        context_instance=RequestContext(request)
    )

def company_index(request):
    companies = get_list_or_404(Company.objects.order_by('pk'), status=1)
    return render_to_response(
        'accounts/company_index.html',
        {
            'companies' : companies,
        },
        context_instance=RequestContext(request)
    )
