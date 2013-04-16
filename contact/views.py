# -*- encoding: utf-8 -*-
from django.shortcuts import redirect, render_to_response
from django.template.loader import render_to_string
from django.template import RequestContext
from django.contrib import messages
from django.conf import settings
from django.views.decorators.csrf import csrf_protect
from django.core.mail import send_mail, EmailMessage
from contact.forms import ContactForm

def _notify_sender(form_data, request):
    content = render_to_string(
        'email/contact_general.txt',
        {'data' : form_data},
        context_instance=RequestContext(request)
    )
    subject = render_to_string(
        'email/contact_general_subject.txt',
        {'data' : form_data},
        context_instance=RequestContext(request)
    )
    subject = subject.replace("\n","")
    mail = EmailMessage(
            subject=subject,
            body=content,
            from_email=settings.SERVER_EMAIL,
            to=[form_data['email']],
           )
    mail.send()
    admin_mail = EmailMessage(
            subject=subject,
            body=content,
            from_email=settings.SERVER_EMAIL,
            to=[settings.CONTACT_EMAIL],
           )
    admin_mail.send()
@csrf_protect
def general(request):
    template_name = 'contact/general.html'
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            if request.POST.get('complete') == '1':
                _notify_sender( form.cleaned_data , request )
                messages.add_message(request, messages.SUCCESS, 'お問い合わせを承りました。確認のメールを送信しました。')
                return redirect('home')
            elif not request.POST.get('complete'):
                template_name = 'contact/general_confirm.html'
    else:
        #ログインしてたら登録情報をセット
        if request.user.is_authenticated():
            u = request.user
            p = u.myuserprofile
            form = ContactForm(initial={
                'email': u.email,
                'first_name': p.first_name,
                'last_name': p.last_name,
                'department' : p.department,
                'company_name' : p.company_name,
                'tel' : p.tel,
                'fax' : p.fax,
                'site_url': p.site_url,
            })
        else:
            form = ContactForm()
    return render_to_response(
        template_name,
        {
            'form' : form,
        },
        context_instance=RequestContext(request)
    )
