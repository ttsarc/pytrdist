# -*- encoding: utf-8 -*-
# Create your views here.
import datetime
from django.contrib import messages
from django.conf import settings
from django.utils.timezone import make_naive, get_default_timezone
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.core.paginator import Paginator
from django.template import RequestContext
from documents.models import DocumentDownloadLog
from documents.forms import LeadSearchForm
from seminars.models import SeminarEntryLog
from trwk.libs.csv_utils import export_csv
from accounts.models import Company


@login_required
def company_leads(request):
    if not request.user.is_superuser:
        messages.add_message(request, messages.ERROR, '管理者ではありません')
        return None
    companies = Company.objects.all()
    if 'search' in request.GET:
        form = LeadSearchForm(request.GET)
    else:
        form = LeadSearchForm()

    return render_to_response(
        'operations/company_list.html',
        {
            'companies': companies,
            'form': form,
        },
        context_instance=RequestContext(request)
    )


@login_required
def download_leads(request, log_type, company_id, type=None, page=1):
    if not request.user.is_superuser:
        messages.add_message(request, messages.ERROR, '管理者ではありません')
        return None
    if log_type == 'document':
        log_obj = DocumentDownloadLog
        date_field = 'download_date'
    elif log_type == 'seminar':
        log_obj = SeminarEntryLog
        date_field = 'entry_date'
    else:
        messages.add_message(request, messages.ERROR, 'log_typeが正しくありません')
        return None
    company = Company.objects.get(pk=company_id)
    csv_fields = log_obj.csv_fields_operation
    leads = log_obj.objects
    if company.slug_name:
        filename = company.slug_name
    else:
        filename = company_id
    filename += '-' + log_type
    if 'search' in request.GET:
        form = LeadSearchForm(request.GET)
        if form.is_valid():
            if form.cleaned_data['start_date']:
                start = datetime.datetime.strptime(
                    str(form.cleaned_data['start_date']),
                    '%Y-%m-%d').replace(tzinfo=timezone.utc)
                query = {
                    '{0}__{1}'.format(date_field, 'gte'): start,
                }
                leads = leads.filter(**query)
                filename += str(form.cleaned_data['start_date']) + '^'
            if form.cleaned_data['end_date']:
                #時刻まで条件に入っているっぽく、前日までしかとれないので+1日
                end = datetime.datetime.strptime(
                    str(form.cleaned_data['end_date']),
                    '%Y-%m-%d').replace(
                        tzinfo=timezone.utc) + datetime.timedelta(days=1)
                query = {
                    '{0}__{1}'.format(date_field, 'lte'): end,
                }
                leads = leads.filter(**query)
                if not form.cleaned_data['start_date']:
                    filename += '-^'
                filename += str(form.cleaned_data['end_date'])
    else:
        form = LeadSearchForm()
        filename += '-all(' + make_naive(
            datetime.datetime.utcnow().replace(tzinfo=timezone.utc),
            get_default_timezone()).strftime('%Y%m%d-%H%M%S') + ')'

    leads = leads.filter(
        company=company,
    ).order_by(date_field)
    filename += '.csv'
    if type == 'csv':
        return export_csv(leads, csv_fields, filename)
    else:
        paginator = Paginator(leads, settings.LOGS_PER_PAGE)
        leads_pages = paginator.page(page)
        return render_to_response(
            'operations/company_leads_list.html',
            {
                'company': company,
                'leads': leads_pages,
                'form': form,
            },
            context_instance=RequestContext(request)
        )
