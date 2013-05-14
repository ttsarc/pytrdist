# -*- coding: utf-8 -*-
import os
from django.db import models
from django.core.mail import send_mail
from django.core.validators import validate_slug
from django.core.validators import RegexValidator,MinLengthValidator, validate_slug
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import (
    PermissionsMixin, BaseUserManager, AbstractBaseUser
)
from accounts.choices import *
from accounts.validators import TelFaxValidaor, PostNumberValidaor
from trwk.libs.fields import ImageWithThumbsField
from trwk.libs.file_utils import normalize_filename
from sorl.thumbnail import ImageField
from django.core.urlresolvers import reverse

class CompanyManager(models.Manager):
    pass

class Company(models.Model):
    name =             models.CharField('掲載企業名', max_length=100)
    kana =             models.CharField('掲載企業名（フリガナ）', max_length=100)
    slug_name =        models.SlugField('スラッグ', blank=True, help_text='CSVのファイル名などに使われます。半角英数字')
    business_type  =   models.SmallIntegerField('業種', choices=BUSINESS_TYPE_CHOICES, blank=True, null=True)
    tel =              models.CharField('電話番号', max_length=16,validators=[TelFaxValidaor], help_text='例：03-3343-5746')
    fax =              models.CharField('FAX', max_length=16, validators=[TelFaxValidaor], help_text='例：03-5326-0360')
    post_number =      models.CharField('郵便番号', max_length=8, validators=[PostNumberValidaor], help_text="例：1630648")
    prefecture =       models.SmallIntegerField('都道府県', choices=PREFECTURES_CHOICES)
    address=           models.CharField('住所', max_length=200)
    site_url =         models.URLField('ホームページURL')
    email =            models.EmailField('代表メールアドレス')
    representative =   models.CharField('代表者名', max_length=100, blank=True)
    foundation_date =  models.CharField('設立', max_length=30)
    account_closing =  models.CharField('決算月', max_length=30, blank=True)
    employee_number =  models.CharField('従業員数', max_length=30)
    capital =          models.CharField('資本金', max_length=30)
    yearly_sales =     models.CharField('年商', max_length=30, blank=True)
    listing =          models.CharField('上場有無', max_length=30, blank=True)
    status =           models.SmallIntegerField('公開状態', choices=STATUS_CHOICES, default=1, help_text='非公開にすると掲載企業一覧で表示されなくなります')

    def get_logo_uplod_path(self, filename):
        filename = normalize_filename(filename)
        root_path = os.path.join('company', 'logo')
        user_path = os.path.join(root_path, str(self.pk))
        return os.path.join(user_path, filename)

    logo_file = ImageField(
        verbose_name = '企業ロゴ',
        upload_to = get_logo_uplod_path,
        blank = True
    )

    add_date =         models.DateTimeField('登録日', auto_now_add=True)
    update_date =      models.DateTimeField('更新日', auto_now=True)

    objects = CompanyManager()

    def get_absolute_url(self):
        return reverse('company_detail', kwargs={'company_id':self.pk})


    class Meta:
        verbose_name = "掲載企業"
        verbose_name_plural = "掲載企業"

    def __unicode__(self):
        return self.name

class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, username=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=MyUserManager.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, username=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email,
            password=password,
            username = username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='メールアドレス',
        max_length=255,
        unique=True,
        db_index=True,
    )
    username =         models.CharField('ユーザー名', max_length=30, blank=True, help_text="システム内で使われます。半角英数字",validators=[validate_slug])
    is_active =        models.BooleanField('有効', default=True)
    is_admin =         models.BooleanField('管理者', default=False)
    is_staff =         models.BooleanField('スタッフ', default=False)
    customer_company = models.ForeignKey(Company, verbose_name='掲載企業', blank=True, null=True, on_delete=models.SET_NULL, help_text="ここで企業が選択されていると、その企業の担当者となります。ミスのないように注意してください。")
    date_joined =      models.DateTimeField('登録日', default=timezone.now, editable=False)
    update_date =      models.DateTimeField('更新日', auto_now=True, editable=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def get_display_name(self):
        if self.username:
            return self.username
        else:
            return self.email

    def is_customer(self):
        if self.customer_company:
            return True
        return False

    def __unicode__(self):
        if self.username:
            return self.username
        else:
            return self.email

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.username)

    def myuserprofile(self):
        return self.myuserprofile

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        subject = subject.replace("\n","")
        send_mail(subject, message, from_email, [self.email])
        #send_mail_jp(subject, message, from_email, [self.email,])

    def get_profile(self):
        """
        Returns site-specific profile for this user. Raises
    SiteProfileNotAvailable if this site does not allow profiles.
        """
        warnings.warn("The use of AUTH_PROFILE_MODULE to define user profiles has been deprecated.",
            PendingDeprecationWarning)
        if not hasattr(self, '_profile_cache'):
            from django.conf import settings
            if not getattr(settings, 'AUTH_PROFILE_MODULE', False):
                raise SiteProfileNotAvailable(
                    'You need to set AUTH_PROFILE_MODULE in your project '
                    'settings')
            try:
                app_label, model_name = settings.AUTH_PROFILE_MODULE.split('.')
            except ValueError:
                raise SiteProfileNotAvailable(
                    'app_label and model_name should be separated by a dot in '
                    'the AUTH_PROFILE_MODULE setting')
            try:
                model = models.get_model(app_label, model_name)
                if model is None:
                    raise SiteProfileNotAvailable(
                        'Unable to load the profile model, check '
                        'AUTH_PROFILE_MODULE in your project settings')
                self._profile_cache = model._default_manager.using(
                                   self._state.db).get(user__id__exact=self.id)
                self._profile_cache.user = self
            except (ImportError, ImproperlyConfigured):
                raise SiteProfileNotAvailable
        return self._profile_cache

class MyUserProfileManager(models.Manager):
    pass

class MyUserProfile(models.Model):
    myuser =           models.OneToOneField(MyUser, verbose_name="ユーザー")
    last_name =        models.CharField('姓', max_length=30)
    first_name =       models.CharField('名', max_length=30)
    last_name_kana =   models.CharField('姓（ふりがな）', max_length=100)
    first_name_kana =  models.CharField('名（ふりがな）', max_length=100)
    company_name =     models.CharField('会社名', max_length=100)
    tel =              models.CharField('電話番号', max_length=16,validators=[TelFaxValidaor], help_text='例：03-3343-5746')
    fax =              models.CharField('FAX', max_length=16, blank=True, validators=[TelFaxValidaor], help_text='例：03-5326-0360')
    post_number =      models.CharField('郵便番号', max_length=8, validators=[PostNumberValidaor], help_text="例：1630648")
    prefecture =       models.SmallIntegerField('都道府県', choices=PREFECTURES_CHOICES)
    address =          models.CharField('住所', max_length=255)
    site_url =         models.URLField( 'ホームページURL', blank=True)
    department =       models.CharField('部署名', max_length=100)
    position =         models.CharField('役職名', max_length=100, blank=True)
    position_class =   models.SmallIntegerField('役職区分', choices=POSITION_CLASS_CHOICES)
    business_type  =   models.SmallIntegerField('業種', choices=BUSINESS_TYPE_CHOICES)
    job_content =      models.SmallIntegerField('職務内容', choices=JOB_CONTENT_CHOICES)
    firm_size =        models.SmallIntegerField('従業員数', choices=FIRM_SIZE_CHOICES)
    yearly_sales =     models.SmallIntegerField('年商', choices=YEARLY_SALES_CHOICES)
    discretion  =      models.SmallIntegerField('あなたの立場', choices=DISCRETION_CHOICES)
    update_date =      models.DateTimeField('更新日', auto_now=True)

    def __unicode__(self):
        return self.myuser.email

    objects = MyUserProfileManager()
    class Meta:
        verbose_name = "プロフィール"
        verbose_name_plural = "プロフィール"

