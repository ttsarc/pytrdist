# -*- encoding: utf-8 -*-
from django.contrib import messages
from django.conf import settings
from django.core.mail import mail_admins
from accounts.models import MyUser

def email_company_staff(company_id, subject, content, email_from=None):
    if not email_from:
        email_from = settings.SERVER_EMAIL
    staffs = MyUser.objects.filter(customer_company=company_id).all()
    subject = subject.replace("\n","")
    for staff in staffs:
        staff.email_user(subject, content, email_from)
    mail_admins(subject=' admin ' + subject, message = content, fail_silently=True)

def is_company_staff(user, company_id=None):
    if not user.is_customer:
        messages.add_message(request, messages.ERROR, '掲載企業の担当者として登録されていません')
        return False

    if company_id != None and user.customer_company.pk != company_id:
        messages.add_message(request, messages.ERROR, '当該掲載企業の担当者ではありません')
        return False

    return True
