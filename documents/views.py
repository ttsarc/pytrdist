# -*- encoding: utf-8 -*-
"""
Views which edit user accounts

"""
import csv, datetime
from django import forms
from django.shortcuts import redirect, render_to_response, get_object_or_404, get_list_or_404
from django.http import Http404,HttpResponse
from django.core import signing
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.template import RequestContext
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.sites.models import RequestSite, Site
from django.conf import settings
from django.views.decorators.csrf import csrf_protect
from django.utils.timezone import utc, make_naive, get_default_timezone
from django.utils import timezone
from accounts.forms import MyUserShowForm, MyUserProfileShowForm
from documents.forms import DocumentForm, DownloadForm, LeadSearchForm
from documents.models import Document, DocumentDownloadLog, DocumentDownloadCount, DocumentDownloadUser, DocumentDownloadUser
from trwk.libs.request_utils import *
from trwk.api.email_utility import email_company_staff
def _check_customer(user):
    if not user.is_customer:
        messages.add_message(request, messages.ERROR, '掲載企業の担当者として登録されていません')
        return redirect('mypage_home')
    return True

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
    company = request.user.customer_company
    documents = Document.objects.all().filter(company__exact=company)
    return render_to_response(
        'documents/edit_index.html',
        {
            'documents' : documents,
        },
        context_instance=RequestContext(request)
    )

def index(request, page=1):
    documents = get_list_or_404(Document, status=1)
    paginator = Paginator(documents, settings.DOCUMENTS_PER_PAGE)
    try:
        paged_documents = paginator.page(page)
    except PageNotAnInteger:
        raise Http404
    except EmptyPage:
        raise Http404

    return render_to_response(
        'documents/index.html',
        {
            'documents' : paged_documents,
            'count': paginator.count,
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

@login_required
def preview(request, document_id):
    _check_customer(request.user)
    company = request.user.customer_company
    if request.user.is_superuser:
        document = get_object_or_404(Document, pk=document_id)
    else:
        document = get_object_or_404(Document, pk=document_id, company=company)
    return render_to_response(
        'documents/detail.html',
        {
            'document' : document,
            'preview' : True,
        },
        context_instance=RequestContext(request)
    )


def _add_download_log(document, form, user, company ,request):
    p = user.myuserprofile
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
    return log

def _notify_company_staff(log, request):
    content = render_to_string(
        'email/notify_download.txt',
        {'log' : log},
        context_instance=RequestContext(request)
    )
    subject = render_to_string(
        'email/notify_download_subject.txt',
        {'log' : log},
        context_instance=RequestContext(request)
    )
    email_company_staff(log.company.id, subject = subject, content = content)

def _add_download_count(document):
    count_obj, created= DocumentDownloadCount.objects.get_or_create(document=document)
    if created:
        count_obj.count = 1
    else:
        new_count = count_obj.count + 1
        count_obj.count = new_count
    count_obj.save()

def _add_download_user(document, user):
    dl_user_obj, created = DocumentDownloadUser.objects.get_or_create(document=document, user=user)
    if not created:
        dl_user_obj.save()

@login_required
def download_link(request, id_sign):
    try:
        data = signing.loads(id_sign)
        document_id = data['id']
    except signing.BadSignature:
        raise Http404
    document = get_object_or_404(Document, pk=document_id, status=1)
    _add_download_user(document, request.user)
    file = document.pdf_file
    filename = file.name.split('/')[-1]
    response = HttpResponse(file, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    response['Content-Length'] = file.tell()
    return response

@login_required
def download(request, document_id):
    document = get_object_or_404(Document, pk=document_id, status=1)
    user = request.user
    template_name = 'documents/download.html'
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
            if request.POST.get('complete') == '1':
                log = _add_download_log(document, form, user, company, request)
                _notify_company_staff(log, request)
                _add_download_count(document)
                #messages.add_message(request, messages.SUCCESS, '資料のダウンロードありがとうございました。')
                return redirect('document_download_complete', id_sign=document.id_sign() )
            elif not request.POST.get('complete'):
                template_name = 'documents/download_preview.html'
    else:
        form = DownloadForm()

    return render_to_response(
        template_name,
        {
            'document' : document,
            'form' : form,
            'user_form' : user_form,
            'user_profile_form' : user_profile_form,
        },
        context_instance=RequestContext(request)
    )

@login_required
def download_complete(request, id_sign):
    try:
        data = signing.loads(id_sign)
        document_id = data['id']
    except signing.BadSignature:
        raise Http404
    document = get_object_or_404(Document, pk=document_id, status=1)
    return render_to_response(
                'documents/download_complete.html',
                    {
                        'document': document,
                    },
                    context_instance=RequestContext(request)
                )

def _export_csv(leads):
    filename = 'trwk-doc-' + datetime.datetime.now().strftime('%Y%m%d-%H%M%S') + '.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="'+ filename +'"'

    csv_fields = {
        1  : ('ダウンロード日', 'download_date'),
        2  : ('資料タイトル',   'document_title'),
        3  : ('会社名',         'company_name'),
        4  : ('姓',             'last_name'),
        5  : ('名',             'first_name'),
        6  : ('姓（ふりがな）', 'last_name_kana'),
        7  : ('名（ふりがな）', 'first_name_kana'),
        8  : ('電話番号',       'tel'),
        9  : ('FAX',            'fax'),
        10 : ('郵便番号',       'post_number'),
        11 : ('都道府県',       'prefecture'),
        12 : ('住所',           'address'),
        13 : ('ホームページURL','site_url'),
        14 : ('部署名',         'department'),
        15 : ('役職名',         'position'),
        16 : ('役職区分',       'position_class'),
        17 : ('業種',           'business_type'),
        18 : ('職務内容',       'job_content'),
        19 : ('従業員規模',     'firm_size'),
        20 : ('年商',           'yearly_sales'),
        21 : ('立場',           'discretion'),
        22 : ('状況',           'stage'),
    }
    writer = csv.writer(response)
    head = []
    first = True
    csv_encode = 'cp932'
    for line in leads:
        items = []
        for key, field in sorted(csv_fields.items()):
            label = field[0]
            name = field[1]
            if first:
                head.append(label.encode( csv_encode ))
            val = getattr(line, name)
            if isinstance(val, unicode):
                items.append(val.encode( csv_encode ))
            elif isinstance(val, long):
                items.append(str(val))
            elif isinstance(val, datetime.datetime):
                #ローカルタイムに変換してる
                items.append(make_naive(val, get_default_timezone()).strftime('%Y-%m-%d %H:%M:%S') )
        if first:
            writer.writerow(head)
            first = False
        writer.writerow(items)
    return response

@login_required
def download_log(request, page=1, type='list'):
    _check_customer(request.user)
    user = request.user
    company = user.customer_company
    leads = DocumentDownloadLog.objects
    if 'search' in request.GET:
        form = LeadSearchForm(request.GET)
        if form.is_valid():
            if form.cleaned_data['start_date']:
                start = datetime.datetime.strptime( str(form.cleaned_data['start_date']),'%Y-%m-%d').replace(tzinfo=timezone.utc)
                leads = leads.filter(download_date__gte=start)
            if form.cleaned_data['end_date']:
                #時刻まで条件に入っているっぽく、前日までしかとれないので+1日
                end =   datetime.datetime.strptime( str(form.cleaned_data['end_date']),'%Y-%m-%d').replace(tzinfo=timezone.utc) + datetime.timedelta(days=1)
                leads = leads.filter(download_date__lte=end)
    else:
        form = LeadSearchForm()
    try:
        leads = leads.filter(
            company=company,
        ).order_by('-download_date')
    except:
        messages.add_message(request, messages.ERROR, 'まだリード情報はありません')
        return redirect('mypage_home' )
    if type == 'list':
        paginator = Paginator(leads, settings.LOGS_PER_PAGE)
        leads_pages = paginator.page(page)
        return render_to_response(
            'documents/download_leads_list.html',
            {
                'leads' : leads_pages,
                'form'  : form,
            },
            context_instance=RequestContext(request)
        )
    elif type == "csv":
        return _export_csv(leads)

@login_required
def my_download_history(request):
    """自分がダウンロードした書式の一覧
    """
    try:
        histories = DocumentDownloadUser.objects.filter(user=request.user).order_by('-update_date')
    except DocumentDownloadUser.DoesNotExist:
        histories = None

    return render_to_response(
        'documents/my_download_history.html',
        {
            'histories' : histories,
        },
        context_instance=RequestContext(request)
    )

