# -*- encoding: utf-8 -*-

from accounts.models import MyUser, MyUserProfile, Company
from django.conf import settings
import logging
from django.core.mail import mail_admins

def email_company_staff(company_id, subject, content, email_from=None):
    if not email_from:
        email_from = settings.SERVER_EMAIL
    staffs = MyUser.objects.filter(customer_company=company_id).all()
    subject = subject.replace("\n","")
    for staff in staffs:
        staff.email_user(subject, content, email_from)
    mail_admins(subject=' admin ' + subject, message = content, fail_silently=True)
