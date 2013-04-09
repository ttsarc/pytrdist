# -*- encoding: utf-8 -*-
"""
Views which edit user accounts

"""
from django import forms
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site
from django.views.decorators.csrf import csrf_protect

from documents.forms import DocumentForm
from documents.models import Document

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
    if user.customer_company.pk == document_id:
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
