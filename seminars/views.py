# -*- encoding: utf-8 -*-
"""
Views which edit user accounts

"""
import datetime
from django import forms
from django.shortcuts import redirect, render_to_response, get_object_or_404, get_list_or_404
from django.http import Http404,HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.template import RequestContext
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone
from accounts.forms import MyUserShowForm, MyUserProfileShowForm
from seminars.forms import SeminarForm, EntryForm, LeadSearchForm
from seminars.models import Seminar, SeminarEntryLog, SeminarEntryUser
from seminars.choices import *
from trwk.libs.request_utils import *
from trwk.api.company_utility import is_company_staff, email_company_staff
from trwk.libs.csv_utils import export_csv

@login_required
@csrf_protect
def add(request):
    if not is_company_staff(request.user):
        return redirect('mypage_home')
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
    seminar = get_object_or_404(Seminar, pk=seminar_id)
    user = request.user
    company = user.customer_company
    if not is_company_staff(request.user, seminar.company.pk):
        return redirect('mypage_home')

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
            'seminar' : seminar,
            'action': 'edit',
            'form' : form,
        },
        context_instance=RequestContext(request)
    )

@login_required
@csrf_protect
def edit_index(request):
    if not is_company_staff(request.user):
        return redirect('mypage_home')
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
    seminars = Seminar.objects.filter(
        status=1,
        entry_status=1,
        limit_datetime__gt=datetime.datetime.utcnow().replace(tzinfo=timezone.utc)
    )
    paged_seminars = None
    count = 0
    if seminars:
        paginator = Paginator(seminars, settings.SEMINARS_PER_PAGE)
        try:
            paged_seminars = paginator.page(page)
            count = paginator.count
        except PageNotAnInteger:
            raise Http404
        except EmptyPage:
            raise Http404

    return render_to_response(
        'seminars/index.html',
        {
            'seminars' : paged_seminars,
            'count': count,
        },
        context_instance=RequestContext(request)
    )

def detail(request, seminar_id):
    seminar = get_object_or_404(Seminar, pk=seminar_id, status=1)
    entry_count = SeminarEntryUser.objects.count_entry(seminar)
    is_entered = False
    if request.user.is_authenticated() and SeminarEntryUser.objects.is_entered(seminar, request.user):
        is_entered = True
    return render_to_response(
        'seminars/detail.html',
        {
            'seminar' : seminar,
            'entry_count': entry_count,
            'is_entered' : is_entered,
        },
        context_instance=RequestContext(request)
    )

@login_required
def preview(request, seminar_id):
    if not is_company_staff(request.user):
        return redirect('mypage_home')
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
            seminar_type =    dict(TYPE_CHOICES)[seminar.type],
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
            # request
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

def _notify_user(user, log, seminar, request):
    data = {
                'user': user,
                'log' : log,
                'seminar' : seminar,
                'request' : request,
            }
    content = render_to_string(
        'email/notify_entry_user.txt',
        data,
        context_instance=RequestContext(request)
    )
    subject = render_to_string(
        'email/notify_entry_user_subject.txt',
        data,
        context_instance=RequestContext(request)
    )
    user.email_user(subject, content, from_email=settings.SERVER_EMAIL)

def _add_entry_user(seminar, user):
    dl_user_obj, created = SeminarEntryUser.objects.get_or_create(seminar=seminar, user=user)
    #満員になったら受付終了処理
    if SeminarEntryUser.objects.count_entry(seminar) >= seminar.limit_number :
        seminar.entry_status = 0
        seminar.save()

@login_required
def entry(request, seminar_id):
    seminar = get_object_or_404(Seminar, pk=seminar_id, status=1)
    entry_count = SeminarEntryUser.objects.count_entry(seminar)
    if seminar.entry_status == 0:
        messages.add_message(request, messages.ERROR, '申し訳ございません。定員数を超えてしまったため申込できません。')
        return redirect('seminar_detail', seminar_id=seminar_id )

    user = request.user
    if SeminarEntryUser.objects.is_entered(seminar_id, user):
        messages.add_message(request, messages.ERROR, 'このセミナーにはすでに申し込み済みです')
        return redirect('seminar_detail', seminar_id=seminar_id )

    if not user.myuserprofile:
        messages.add_message(request, messages.ERROR, 'ユーザー情報の設定が完了していません。お手数ですが管理者に御問合せください')
        return redirect('trwk_home' )
    company = seminar.company
    if not company:
        messages.add_message(request, messages.ERROR, 'セミナーの提供元企業が存在しません')
        return redirect('trwk_home' )

    template_name = 'seminars/entry.html'
    user_form = MyUserShowForm(instance=user)
    user_profile_form = MyUserProfileShowForm(instance=user.myuserprofile)
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            if request.POST.get('complete') == '1':
                log = _add_entry_log(seminar, form, user, company, request)
                _notify_user(user, log, seminar, request)
                _notify_company_staff(log, request)
                _add_entry_user(seminar, user)
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

@login_required
def entry_log(request, page=1, type='list'):
    if not is_company_staff(request.user):
        return redirect('mypage_home')
    user = request.user
    company = user.customer_company
    leads = SeminarEntryLog.objects
    filename = 'trwk-semi'
    if 'search' in request.GET:
        form = LeadSearchForm(request.GET)
        if form.is_valid():
            if form.cleaned_data['start_date']:
                start = datetime.datetime.strptime( str(form.cleaned_data['start_date']),'%Y-%m-%d').replace(tzinfo=timezone.utc)
                leads = leads.filter(entry_date__gte=start)
                filename = filename + '-' + str(form.cleaned_data['start_date'])+ '^'
            if form.cleaned_data['end_date']:
                #時刻まで条件に入っているっぽく、前日までしかとれないので+1日
                end =   datetime.datetime.strptime( str(form.cleaned_data['end_date']),'%Y-%m-%d').replace(tzinfo=timezone.utc) + datetime.timedelta(days=1)
                leads = leads.filter(entry_date__lte=end)
                if not form.cleaned_data['start_date']:
                    filename += '-^'
                filename += str(form.cleaned_data['end_date'])
    else:
        form = LeadSearchForm()
        filename += '-all(' + timezone.make_naive(datetime.datetime.utcnow().replace(tzinfo=timezone.utc), timezone.get_default_timezone()).strftime('%Y%m%d-%H%M%S') + ')'
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
            'seminars/mypage_leads_list.html',
            {
                'leads' : leads_pages,
                'form'  : form,
            },
            context_instance=RequestContext(request)
        )
    elif type == "csv":
        csv_fields = SeminarEntryLog.csv_fields
        filename += '.csv'
        return export_csv(leads, csv_fields, filename)

@login_required
def my_entry_history(request):
    """自分が申し込みした書式の一覧
    """
    try:
        histories = SeminarEntryUser.objects.filter(user=request.user).order_by('-add_date')
    except SeminarEntryUser.DoesNotExist:
        histories = None

    return render_to_response(
        'seminars/mypage_entry_history.html',
        {
            'histories' : histories,
        },
        context_instance=RequestContext(request)
    )
