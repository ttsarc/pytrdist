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
from seminars.forms import SeminarForm, EntryForm, LeadSearchForm
from seminars.models import Seminar, SeminarEntryLog, SeminarEntryUser
from seminars.choices import *
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
        form = SeminarForm(request.POST, request.FILES)
        if form.is_valid():
            seminar = form.save(commit=False)
            seminar.user = user
            seminar.company = company
            seminar.save()
            messages.add_message(request, messages.SUCCESS, 'セミナーを保存しました')
            return redirect('seminar_edit', seminar_id=seminar.pk )
    else:
        form = SeminarForm()

    return render_to_response(
        'seminars/add_edit.html',
        {
            'action'  : 'add',
            'form' : form,
        },
        context_instance=RequestContext(request)
    )

@login_required
@csrf_protect
def edit(request, seminar_id):
    _check_customer(request.user)
    seminar = get_object_or_404(Seminar, pk=seminar_id)
    user = request.user
    company = user.customer_company
    if user.customer_company.pk != seminar.company.pk:
        messages.add_message(request, messages.ERROR, 'このセミナーを編集する権限はありません')
        return redirect('mypage_home' )

    if request.method == 'POST':
        form = SeminarForm(request.POST, request.FILES, instance=seminar)
        if form.is_valid():
            seminar = form.save()
            messages.add_message(request, messages.SUCCESS, 'セミナーを保存しました')
            return redirect('seminar_edit', seminar_id=seminar.pk )
    else:
        form = SeminarForm(instance=seminar)

    return render_to_response(
        'seminars/add_edit.html',
        {
            'action': 'edit',
            'form' : form,
        },
        context_instance=RequestContext(request)
    )

@login_required
@csrf_protect
def edit_index(request):
    _check_customer(request.user)
    company = request.user.customer_company
    seminars = Seminar.objects.all().filter(company__exact=company)
    return render_to_response(
        'seminars/edit_index.html',
        {
            'seminars' : seminars,
        },
        context_instance=RequestContext(request)
    )

def index(request, page=1):
    seminars = get_list_or_404(Seminar, status=1)
    paginator = Paginator(seminars, settings.DOCUMENTS_PER_PAGE)
    try:
        paged_seminars = paginator.page(page)
    except PageNotAnInteger:
        raise Http404
    except EmptyPage:
        raise Http404

    return render_to_response(
        'seminars/index.html',
        {
            'seminars' : paged_seminars,
            'count': paginator.count,
        },
        context_instance=RequestContext(request)
    )

def detail(request, seminar_id):
    seminar = get_object_or_404(Seminar, pk=seminar_id, status=1)
    return render_to_response(
        'seminars/detail.html',
        {
            'seminar' : seminar,
        },
        context_instance=RequestContext(request)
    )

@login_required
def preview(request, seminar_id):
    _check_customer(request.user)
    company = request.user.customer_company
    if request.user.is_superuser:
        seminar = get_object_or_404(Seminar, pk=seminar_id)
    else:
        seminar = get_object_or_404(Seminar, pk=seminar_id, company=company)
    return render_to_response(
        'seminars/detail.html',
        {
            'seminar' : seminar,
            'preview' : True,
        },
        context_instance=RequestContext(request)
    )


def _add_entry_log(seminar, form, user, company ,request):
    p = user.myuserprofile
    log = SeminarEntryLog(
            # Seminar
            seminar_id =      seminar.id,
            seminar_title =   seminar.title,
            seminar_type =    seminar.type,
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
            note =            form.cleaned_data['note'],
            ip =              get_request_addr_or_ip(request),
            ua =              get_request_ua(request),
    )
    log.save()
    return log

def _notify_company_staff(log, request):
    content = render_to_string(
        'email/notify_entry.txt',
        {
            'log' : log,
        },
        context_instance=RequestContext(request)
    )
    subject = render_to_string(
        'email/notify_entry_subject.txt',
        {
            'log' : log,
        },
        context_instance=RequestContext(request)
    )
    email_company_staff(log.company.id, subject = subject, content = content)

def _add_entry_user(seminar, user):
    dl_user_obj, created = SeminarEntryUser.objects.get_or_create(seminar=seminar, user=user)
    if not created:
        dl_user_obj.save()

@login_required
def entry(request, seminar_id):
    seminar = get_object_or_404(Seminar, pk=seminar_id, status=1)
    user = request.user
    template_name = 'seminars/entry.html'
    if not user.myuserprofile:
        messages.add_message(request, messages.ERROR, 'ユーザー情報の設定が完了していません。お手数ですが管理者に御問合せください')
        return redirect('trwk_home' )
    company = seminar.company
    if not company:
        messages.add_message(request, messages.ERROR, 'セミナーの提供元企業が存在しません')
        return redirect('trwk_home' )

    user_form = MyUserShowForm(instance=user)
    user_profile_form = MyUserProfileShowForm(instance=user.myuserprofile)
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            if request.POST.get('complete') == '1':
                log = _add_entry_log(seminar, form, user, company, request)
                _notify_company_staff(log, request)
                _add_entry_user(seminar, user)
                #messages.add_message(request, messages.SUCCESS, 'セミナーの申し込みありがとうございました。')
                return redirect('seminar_entry_complete', seminar_id=seminar.id )
            elif not request.POST.get('complete'):
                template_name = 'seminars/entry_preview.html'
    else:
        form = EntryForm()

    return render_to_response(
        template_name,
        {
            'seminar' : seminar,
            'form' : form,
            'user_form' : user_form,
            'user_profile_form' : user_profile_form,
        },
        context_instance=RequestContext(request)
    )

@login_required
def entry_complete(request, seminar_id):
    seminar = get_object_or_404(Seminar, pk=seminar_id, status=1)
    return render_to_response(
                'seminars/entry_complete.html',
                    {
                        'seminar': seminar,
                    },
                    context_instance=RequestContext(request)
                )

def _export_csv(leads):
    filename = 'trwk-semi-' + datetime.datetime.now().strftime('%Y%m%d-%H%M%S') + '.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="'+ filename +'"'

    csv_fields = {
        1  : ('申し込み日',       'entry_date'),
        2  : ('セミナータイトル', 'seminar_title'),
        3  : ('種別',             'seminar_type'),
        4  : ('会社名',           'company_name'),
        5  : ('姓',               'last_name'),
        6  : ('名',               'first_name'),
        7  : ('姓（ふりがな）',   'last_name_kana'),
        8  : ('名（ふりがな）',   'first_name_kana'),
        9  : ('電話番号',         'tel'),
        10 : ('FAX',              'fax'),
        11 : ('郵便番号',         'post_number'),
        12 : ('都道府県',         'prefecture'),
        13 : ('住所',             'address'),
        14 : ('ホームページURL',  'site_url'),
        15 : ('部署名',           'department'),
        16 : ('役職名',           'position'),
        17 : ('役職区分',         'position_class'),
        18 : ('業種',             'business_type'),
        19 : ('職務内容',         'job_content'),
        20 : ('従業員規模',       'firm_size'),
        21 : ('年商',             'yearly_sales'),
        22 : ('立場',             'discretion'),
        23 : ('備考',             'note'),
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
def entry_log(request, page=1, type='list'):
    _check_customer(request.user)
    user = request.user
    company = user.customer_company
    leads = SeminarEntryLog.objects
    if 'search' in request.GET:
        form = LeadSearchForm(request.GET)
        if form.is_valid():
            if form.cleaned_data['start_date']:
                start = datetime.datetime.strptime( str(form.cleaned_data['start_date']),'%Y-%m-%d').replace(tzinfo=timezone.utc)
                leads = leads.filter(entry_date__gte=start)
            if form.cleaned_data['end_date']:
                #時刻まで条件に入っているっぽく、前日までしかとれないので+1日
                end =   datetime.datetime.strptime( str(form.cleaned_data['end_date']),'%Y-%m-%d').replace(tzinfo=timezone.utc) + datetime.timedelta(days=1)
                leads = leads.filter(entry_date__lte=end)
    else:
        form = LeadSearchForm()
    try:
        leads = leads.filter(
            company=company,
        ).order_by('-entry_date')
    except:
        messages.add_message(request, messages.ERROR, 'まだリード情報はありません')
        return redirect('mypage_home' )
    if type == 'list':
        paginator = Paginator(leads, settings.LOGS_PER_PAGE)
        leads_pages = paginator.page(page)
        return render_to_response(
            'seminars/entry_leads_list.html',
            {
                'leads' : leads_pages,
                'form'  : form,
            },
            context_instance=RequestContext(request)
        )
    elif type == "csv":
        return _export_csv(leads)

@login_required
def my_entry_history(request):
    """自分が申し込みした書式の一覧
    """
    try:
        histories = SeminarEntryUser.objects.filter(user=request.user).order_by('-add_date')
    except SeminarEntryUser.DoesNotExist:
        histories = None

    return render_to_response(
        'seminars/my_entry_history.html',
        {
            'histories' : histories,
        },
        context_instance=RequestContext(request)
    )

