# -*- encoding: utf-8 -*-
"""
view of Documents

"""
from datetime import datetime, timedelta
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.http import Http404, HttpResponse
from django.core import signing
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.template import RequestContext
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone
from django.db.models import Count
from accounts.forms import MyUserShowForm, MyUserProfileShowForm
from documents.forms import DocumentForm, DownloadForm, LeadSearchForm
from documents.models import (
    Document,
    DocumentDownloadLog,
    DocumentDownloadCount,
    DocumentDownloadUser, )
from trwk.libs.request_utils import (
    get_request_addr_or_ip,
    get_request_ua,
    set_recent_checked,)
from trwk.libs.csv_utils import export_csv
from trwk.api.company_utility import is_company_staff, email_company_staff

@login_required
@csrf_protect
def add(request):
    if not is_company_staff(request.user):
        return redirect('mypage_home')
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
            return redirect('document_edit', document_id=document.pk)
    else:
        form = DocumentForm()

    return render_to_response(
        'documents/add_edit.html',
        {
            'action': 'add',
            'form': form,
        },
        context_instance=RequestContext(request)
    )


@login_required
@csrf_protect
def edit(request, document_id):
    document = get_object_or_404(Document, pk=document_id, status__in=[0, 1])
    if not is_company_staff(request.user, document.company.pk):
        return redirect('mypage_home')

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            document = form.save()
            if form.cleaned_data['status'] == 2:
                messages.add_message(request, messages.SUCCESS, '資料を削除しました')
            else:
                messages.add_message(request, messages.SUCCESS, '資料を保存しました')
            return redirect('document_edit_index')
    else:
        form = DocumentForm(instance=document)

    return render_to_response(
        'documents/add_edit.html',
        {
            'document': document,
            'action': 'edit',
            'form': form,
        },
        context_instance=RequestContext(request)
    )


@login_required
@csrf_protect
def edit_index(request):
    if not is_company_staff(request.user):
        return redirect('mypage_home')
    company = request.user.customer_company
    documents = Document.objects.filter(
        company__exact=company,
        status__in=[0, 1],
    ).annotate(download_count=Count('documentdownloaduser'))

    return render_to_response(
        'documents/edit_index.html',
        {
            'documents': documents,
        },
        context_instance=RequestContext(request)
    )


def index(request, page=1):
    documents = Document.objects.filter(status=1)
    paged_documents = None
    count = None
    if documents:
        paginator = Paginator(documents, settings.DOCUMENTS_PER_PAGE)
        try:
            paged_documents = paginator.page(page)
            count = paginator.count
        except PageNotAnInteger:
            raise Http404
        except EmptyPage:
            raise Http404

    return render_to_response(
        'documents/index.html',
        {
            'documents': paged_documents,
            'count': count,
        },
        context_instance=RequestContext(request)
    )


def detail(request, document_id):
    document = get_object_or_404(Document, pk=document_id, status=1)
    response = render_to_response(
        'documents/detail.html',
        {
            'document': document,
        },
        context_instance=RequestContext(request)
    )
    set_recent_checked(request, 'Document', document_id)

    return response


@login_required
def preview(request, document_id):
    if not is_company_staff(request.user):
        return redirect('mypage_home')
    company = request.user.customer_company
    if request.user.is_superuser:
        document = get_object_or_404(Document, pk=document_id)
    else:
        document = get_object_or_404(Document, pk=document_id, company=company)
    return render_to_response(
        'documents/detail.html',
        {
            'document': document,
            'preview': True,
        },
        context_instance=RequestContext(request)
    )


def _add_download_log(document, form, user, company, request):
    p = user.myuserprofile
    log = DocumentDownloadLog(
        # Document
        document_id=document.id,
        document_title=document.title,
        # Company
        company=company,
        # MyUser
        user_id=user.id,
        email=user.email,
        # MyUserProfile
        last_name=p.last_name,
        first_name=p.first_name,
        last_name_kana=p.last_name_kana,
        first_name_kana=p.first_name_kana,
        company_name=p.company_name,
        tel=p.tel,
        fax=p.fax,
        post_number=p.post_number,
        prefecture=p.get_prefecture_display(),
        address=p.address,
        site_url=p.site_url,
        department=p.department,
        position=p.position,
        position_class=p.get_position_class_display(),
        business_type=p.get_business_type_display(),
        job_content=p.get_job_content_display(),
        firm_size=p.get_firm_size_display(),
        yearly_sales=p.get_yearly_sales_display(),
        discretion=p.get_discretion_display(),
        # DonwloadForm
        stage=dict(form.fields['stage'].choices)[
            int(form.cleaned_data['stage'])
        ],
        # request
        ip=get_request_addr_or_ip(request),
        ua=get_request_ua(request),
    )
    log.save()
    return log


def _notify_company_staff(log, request):
    content = render_to_string(
        'email/notify_download.txt',
        {'log': log},
        context_instance=RequestContext(request)
    )
    subject = render_to_string(
        'email/notify_download_subject.txt',
        {'log': log},
        context_instance=RequestContext(request)
    )
    email_company_staff(log.company.id, subject=subject, content=content)


def _add_download_count(document):
    count_obj, created = DocumentDownloadCount.objects.get_or_create(
        document=document)
    if created:
        count_obj.count = 1
    else:
        new_count = count_obj.count + 1
        count_obj.count = new_count
    count_obj.save()


def _add_download_user(document, user):
    dl_user_obj, created = DocumentDownloadUser.objects.get_or_create(
        document=document,
        user=user)
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
        messages.add_message(
            request,
            messages.ERROR,
            'ユーザー情報の設定が完了していません。お手数ですが管理者に御問合せください')
        return redirect('trwk_home')
    company = document.company
    if not company:
        messages.add_message(
            request,
            messages.ERROR,
            '資料の提供元企業が存在しません')
        return redirect('trwk_home')

    user_form = MyUserShowForm(instance=user)
    user_profile_form = MyUserProfileShowForm(instance=user.myuserprofile)
    if request.method == 'POST':
        form = DownloadForm(request.POST)
        if form.is_valid():
            if request.POST.get('complete') == '1':
                log = _add_download_log(document, form, user, company, request)
                _notify_company_staff(log, request)
                _add_download_count(document)
                return redirect(
                    'document_download_complete',
                    id_sign=document.id_sign())
            elif not request.POST.get('complete'):
                template_name = 'documents/download_preview.html'
    else:
        form = DownloadForm()

    return render_to_response(
        template_name,
        {
            'document': document,
            'form': form,
            'user_form': user_form,
            'user_profile_form': user_profile_form,
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
        {'document': document, },
        context_instance=RequestContext(request))


@login_required
def download_log(request, page=1, type='list'):
    if not is_company_staff(request.user):
        return redirect('mypage_home')
    user = request.user
    company = user.customer_company
    leads = DocumentDownloadLog.objects
    filename = 'trwk-doc'
    if 'search' in request.GET:
        form = LeadSearchForm(request.GET)
        if form.is_valid():
            if form.cleaned_data['start_date']:
                start = datetime.strptime(
                    str(form.cleaned_data['start_date']),
                    '%Y-%m-%d').replace(tzinfo=timezone.utc)
                leads = leads.filter(download_date__gte=start)
                filename = filename + '-' + str(
                    form.cleaned_data['start_date']) + '^'
            if form.cleaned_data['end_date']:
                #時刻まで条件に入っているっぽく、前日までしかとれないので+1日
                end = datetime.strptime(
                    str(form.cleaned_data['end_date']),
                    '%Y-%m-%d'
                ).replace(tzinfo=timezone.utc) + timedelta(days=1)
                leads = leads.filter(download_date__lte=end)
                if not form.cleaned_data['start_date']:
                    filename += '-^'
                filename += str(form.cleaned_data['end_date'])
    else:
        form = LeadSearchForm()
        filename += '-all(' + timezone.make_naive(
            datetime.utcnow().replace(tzinfo=timezone.utc),
            timezone.get_default_timezone()
        ).strftime('%Y%m%d-%H%M%S') + ')'
    try:
        leads = leads.filter(
            company=company,
        ).order_by('-download_date')
    except:
        messages.add_message(request, messages.ERROR, 'まだリード情報はありません')
        return redirect('mypage_home')
    if type == 'list':
        paginator = Paginator(leads, settings.LOGS_PER_PAGE)
        leads_pages = paginator.page(page)
        return render_to_response(
            'documents/mypage_leads_list.html',
            {
                'leads': leads_pages,
                'form': form,
            },
            context_instance=RequestContext(request)
        )
    elif type == "csv":
        csv_fields = DocumentDownloadLog.csv_fields
        filename += '.csv'
        return export_csv(leads, csv_fields, filename)


@login_required
def my_download_history(request):
    """自分がダウンロードした書式の一覧
    """
    try:
        histories = DocumentDownloadUser.objects.filter(
            user=request.user
        ).order_by('-update_date')
    except DocumentDownloadUser.DoesNotExist:
        histories = None

    return render_to_response(
        'documents/mypage_download_history.html',
        {
            'histories': histories,
        },
        context_instance=RequestContext(request)
    )
