# -*- encoding: utf-8 -*-
"""
Views which edit user accounts

"""
from django import forms
from django.shortcuts import redirect, render_to_response, get_object_or_404, get_list_or_404
from django.http import Http404
from django.core import signing
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
from documents.forms import DocumentForm, DownloadForm, MyUserShowForm, MyUserProfileShowForm
from documents.models import Document, DocumentDownloadLog
from trwk.libs.request_utils import *
def _check_customer(user):
    if not user.is_customer:
        messages.add_message(request, messages.ERROR, '掲載企業の担当者として登録されていません')
        return redirect('mypage_home')
    return None

@login_required
@csrf_protect
def add(request):
    _check_customer(request.user)
    user = request.user
    company = user.customer_company
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.user = user
            document.company = company
            document.save()
            messages.add_message(request, messages.SUCCESS, '資料を保存しました')
            return redirect('document_edit', document_id=document.pk )
    else:
        form = DocumentForm()

    return render_to_response(
        'documents/add.html',
        {
            'form' : form,
        },
        context_instance=RequestContext(request)
    )

@login_required
@csrf_protect
def edit(request, document_id):
    _check_customer(request.user)
    document = get_object_or_404(Document, pk=document_id)
    user = request.user
    company = user.customer_company
    if user.customer_company.pk != document.company.pk:
        messages.add_message(request, messages.ERROR, 'この資料を編集する権限はありません')
        return redirect('mypage_home' )

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            document = form.save()
            messages.add_message(request, messages.SUCCESS, '資料を保存しました')
            return redirect('document_edit', document_id=document.pk )
    else:
        form = DocumentForm(instance=document)

    return render_to_response(
        'documents/edit.html',
        {
            'form' : form,
        },
        context_instance=RequestContext(request)
    )

@login_required
@csrf_protect
def edit_index(request):
    _check_customer(request.user)
    user = request.user
    company = user.customer_company
    documents = Document.objects.all().filter(company__exact=company)
    return render_to_response(
        'documents/edit_index.html',
        {
            'documents' : documents,
        },
        context_instance=RequestContext(request)
    )

def index(request):
    documents = get_list_or_404(Document, status=1)
    return render_to_response(
        'documents/index.html',
        {
            'documents' : documents,
        },
        context_instance=RequestContext(request)
    )

def detail(request, document_id):
    document = get_object_or_404(Document, pk=document_id, status=1)
    return render_to_response(
        'documents/detail.html',
        {
            'document' : document,
        },
        context_instance=RequestContext(request)
    )

def _add_download_log(document, form, user, company ,request):
    p = user.myuserprofile
    print(form.fields['stage'].choices)
    log = DocumentDownloadLog(
            # Document
            document_id =     document.id,
            document_title =  document.title,
            # Company
            company =         company,
            # MyUser
            user_id =         user.id,
            email =           user.email,
            # MyUserProfile
            last_name =       p.last_name,
            first_name =      p.first_name,
            last_name_kana =  p.last_name_kana,
            first_name_kana = p.first_name_kana,
            company_name =    p.company_name,
            tel =             p.tel,
            fax =             p.fax,
            post_number =     p.post_number,
            prefecture =      p.get_prefecture_display(),
            address =         p.address,
            site_url =        p.site_url,
            department =      p.department,
            position =        p.position,
            position_class =  p.get_position_class_display(),
            business_type =   p.get_business_type_display(),
            job_content =     p.get_job_content_display(),
            firm_size =       p.get_firm_size_display(),
            yearly_sales =    p.get_yearly_sales_display(),
            discretion =      p.get_discretion_display(),
            # DonwloadForm
            stage =           dict(form.fields['stage'].choices)[ int(form.cleaned_data['stage']) ],
            ip =              get_request_addr_or_ip(request),
            ua =              get_request_ua(request),
    )
    log.save()

@login_required
def send(request, download_sign):
    try:
        data = signing.loads(download_sign)
        document_id = data['id']
    except signing.BadSignature:
        raise Http404
    document = get_object_or_404(Document, pk=document_id, status=1)
    file = document.pdf_file
    filename = file.name.split('/')[-1]
    response = HttpResponse(file, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    response['Content-Length'] = file.tell()
    return response

def create_id_sign(id):
    sign = signing.dumps({'id': id })
    return sign

@login_required
def download(request, document_id):
    document = get_object_or_404(Document, pk=document_id, status=1)
    user = request.user
    if not user.myuserprofile:
        messages.add_message(request, messages.ERROR, 'ユーザー情報の設定が完了していません。お手数ですが管理者に御問合せください')
        return redirect('trwk_home' )
    company = document.company
    if not company:
        messages.add_message(request, messages.ERROR, '資料の提供元企業が存在しません')
        return redirect('trwk_home' )

    user_form = MyUserShowForm(instance=user)
    user_profile_form = MyUserProfileShowForm(instance=user.myuserprofile)
    if request.method == 'POST':
        form = DownloadForm(request.POST)
        if form.is_valid():
            _add_download_log(document, form, user, company, request)
            messages.add_message(request, messages.SUCCESS, '資料のダウンロードありがとうございました。')
            download_sign = create_id_sign(document.id)
            return render_to_response(
                'documents/download_complete.html',
                {
                    'download_sign': download_sign,
                    'document': document,
                },
                context_instance=RequestContext(request)
            )
    else:
        form = DownloadForm()

    return render_to_response(
        'documents/download.html',
        {
            'document' : document,
            'form' : form,
            'user_form' : user_form,
            'user_profile_form' : user_profile_form,
        },
        context_instance=RequestContext(request)
    )

