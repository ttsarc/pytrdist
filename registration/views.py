# -*- encoding: utf-8 -*-
"""
Views which allow users to create and activate accounts.

"""
from django import forms
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site
from django.views.decorators.csrf import csrf_protect
from registration.backends import get_backend
from registration.models import RegistrationProfile, ChangeEmailProfile
from registration.forms import ChangeEmailForm
from accounts.forms import MyUserProfileForm
from accounts.models import MyUser
from trwk.libs.request_utils import set_next_url

def activate_complete(request):
    
    return render_to_response(
        'registration/activation_complete.html',
        context_instance=RequestContext(request)
    )

def activate(request, backend,
             template_name='registration/activate.html',
             success_url=None, extra_context=None, **kwargs):
    """
    Activate a user's account.

    The actual activation of the account will be delegated to the
    backend specified by the ``backend`` keyword argument (see below);
    the backend's ``activate()`` method will be called, passing any
    keyword arguments captured from the URL, and will be assumed to
    return a ``User`` if activation was successful, or a value which
    evaluates to ``False`` in boolean context if not.

    Upon successful activation, the backend's
    ``post_activation_redirect()`` method will be called, passing the
    ``HttpRequest`` and the activated ``User`` to determine the URL to
    redirect the user to. To override this, pass the argument
    ``success_url`` (see below).

    On unsuccessful activation, will render the template
    ``registration/activate.html`` to display an error message; to
    override thise, pass the argument ``template_name`` (see below).

    **Arguments**

    ``backend``
        The dotted Python import path to the backend class to
        use. Required.

    ``extra_context``
        A dictionary of variables to add to the template context. Any
        callable object in this dictionary will be called to produce
        the end result which appears in the context. Optional.

    ``success_url``
        The name of a URL pattern to redirect to on successful
        acivation. This is optional; if not specified, this will be
        obtained by calling the backend's
        ``post_activation_redirect()`` method.
    
    ``template_name``
        A custom template to use. This is optional; if not specified,
        this will default to ``registration/activate.html``.

    ``\*\*kwargs``
        Any keyword arguments captured from the URL, such as an
        activation key, which will be passed to the backend's
        ``activate()`` method.
    
    **Context:**
    
    The context will be populated from the keyword arguments captured
    in the URL, and any extra variables supplied in the
    ``extra_context`` argument (see above).
    
    **Template:**
    
    registration/activate.html or ``template_name`` keyword argument.
    
    """
    try:
        is_activatable, user = RegistrationProfile.objects.is_activatable(**kwargs)
        print(user)
    except:
        is_activatable, user = False, None

    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value

    if is_activatable == False:
        messages.add_message(request, messages.ERROR, 'すでにプロフィールを登録済みです')
        return redirect('trwk_home')

    if request.method == 'POST':
        form = MyUserProfileForm(request.POST)
        if form.is_valid():
            if request.POST.get('complete') == '1':
                try:
                    form_valid = form.save(commit=False)
                    form_valid.myuser_id = user.pk
                    form_valid.save()
                except:
                    messages.add_message(request, messages.ERROR, 'すでにプロフィールを登録済みです')

                else:
                    backend = get_backend(backend)
                    account = backend.activate(request, **kwargs)
                    #自動ログイン
                    #http://stackoverflow.com/questions/2787650/manually-logging-in-a-user-without-password
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    login(request, user)
                    if account:
                        if success_url is None:
                            to, args, kwargs = backend.post_activation_redirect(request, account)
                            return redirect(to, *args, **kwargs)
                        else:
                            return redirect(success_url)
            #修正するをクリックした時
            elif request.POST.get('complete') == '0':
                pass
            else:
                template_name = "registration/activate_preview.html"
    else:
        form = MyUserProfileForm()
    kwargs['form'] = form
    kwargs['temp_user'] = user
    kwargs['is_activatable'] = is_activatable
    return render_to_response(template_name,
                              kwargs,
                              context_instance=context)

def register(request, backend, success_url=None, form_class=None,
             disallowed_url='registration_disallowed',
             template_name='registration/registration_form.html',
             extra_context=None):
    """
    Allow a new user to register an account.

    The actual registration of the account will be delegated to the
    backend specified by the ``backend`` keyword argument (see below);
    it will be used as follows:

    1. The backend's ``registration_allowed()`` method will be called,
       passing the ``HttpRequest``, to determine whether registration
       of an account is to be allowed; if not, a redirect is issued to
       the view corresponding to the named URL pattern
       ``registration_disallowed``. To override this, see the list of
       optional arguments for this view (below).

    2. The form to use for account registration will be obtained by
       calling the backend's ``get_form_class()`` method, passing the
       ``HttpRequest``. To override this, see the list of optional
       arguments for this view (below).

    3. If valid, the form's ``cleaned_data`` will be passed (as
       keyword arguments, and along with the ``HttpRequest``) to the
       backend's ``register()`` method, which should return the new
       ``User`` object.

    4. Upon successful registration, the backend's
       ``post_registration_redirect()`` method will be called, passing
       the ``HttpRequest`` and the new ``User``, to determine the URL
       to redirect the user to. To override this, see the list of
       optional arguments for this view (below).
    
    **Required arguments**
    
    None.
    
    **Optional arguments**

    ``backend``
        The dotted Python import path to the backend class to use.

    ``disallowed_url``
        URL to redirect to if registration is not permitted for the
        current ``HttpRequest``. Must be a value which can legally be
        passed to ``django.shortcuts.redirect``. If not supplied, this
        will be whatever URL corresponds to the named URL pattern
        ``registration_disallowed``.
    
    ``form_class``
        The form class to use for registration. If not supplied, this
        will be retrieved from the registration backend.
    
    ``extra_context``
        A dictionary of variables to add to the template context. Any
        callable object in this dictionary will be called to produce
        the end result which appears in the context.

    ``success_url``
        URL to redirect to after successful registration. Must be a
        value which can legally be passed to
        ``django.shortcuts.redirect``. If not supplied, this will be
        retrieved from the registration backend.
    
    ``template_name``
        A custom template to use. If not supplied, this will default
        to ``registration/registration_form.html``.
    
    **Context:**
    
    ``form``
        The registration form.
    
    Any extra variables supplied in the ``extra_context`` argument
    (see above).
    
    **Template:**
    
    registration/registration_form.html or ``template_name`` keyword
    argument.
    
    """
    backend = get_backend(backend)
    if not backend.registration_allowed(request):
        return redirect(disallowed_url)
    if form_class is None:
        form_class = backend.get_form_class(request)

    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES)
        if form.is_valid():
            try:
                new_user = backend.register(request, **form.cleaned_data)
            except:
                #確認メール再送
                email = form.cleaned_data['email']
                user = MyUser.objects.get(email=email)
                profile = RegistrationProfile.objects.filter(user=user.id).order_by('-id')[0]
                profile.send_activation_email(site = Site.objects.get_current())
                messages.add_message(request, messages.WARNING, 'すでに送信済みのメールアドレスです。確認メールを再送しましたのでご確認ください')
            else:
                if success_url is None:
                    to, args, kwargs = backend.post_registration_redirect(request, new_user)
                    return redirect(to, *args, **kwargs)
                else:
                    return redirect(success_url)
    else:
        form = form_class()

    set_next_url(request)

    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value

    return render_to_response(template_name,
                              {'form': form},
                              context_instance=context)

@csrf_protect
@login_required
def change_email(request, backend, success_url=None, form_class=None,
             disallowed_url='change_email_disallowed',
             template_name='registration/change_email_form.html',
             extra_context=None):

    if Site._meta.installed:
        site = Site.objects.get_current()
    else:
        site = RequestSite(request)

    if request.method == 'POST':
        form = ChangeEmailForm(data=request.POST)
        if form.is_valid():
            try:
                create = ChangeEmailProfile.objects.create_profile(request.user, form.cleaned_data['new_email'] )
                create.send_activation_email(site)
            except:
                messages.add_message(request, messages.ERROR, '送信に失敗しました')
            else:
                return redirect('registration_change_email_send')
    else:
        form = ChangeEmailForm()
    context = RequestContext(request)
    if extra_context is None:
        extra_context = {}
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value

    return render_to_response(template_name,
                              {'form': form},
                              context_instance=context)

@login_required
def change_email_done(request, activation_key,
                      template_name='registration/change_email_done.html',
                      extra_context=None):
    
    result = ChangeEmailProfile.objects.change_email(activation_key, request.user)
    
    if result:
        return redirect('registration_change_email_complete')
    
    context = RequestContext(request)
    if extra_context is None:
        extra_context = {}
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value

    return render_to_response(template_name,
                              {'result': result},
                              context_instance=context)
