# -*- coding: utf-8 -*-
import os, time
from django.db import models
from django.core.mail import send_mail
from django.core import signing
from django.utils import timezone
from django.conf import settings
from django.core.urlresolvers import reverse
from accounts.models import Company
from documents.choices import *
from trwk.libs.fields import ImageWithThumbsField, ContentTypeRestrictedFileField
from trwk.libs.file_utils import normalize_filename
from sorl.thumbnail import ImageField

class DocumentManager(models.Manager):
    pass

class Document(models.Model):
    title =       models.CharField('タイトル', max_length=80)
    user =        models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='作成ユーザー', null=True, on_delete=models.SET_NULL)
    company =     models.ForeignKey(Company, verbose_name='掲載企業')
    def get_pdf_uplod_path(self, filename):
        filename = normalize_filename(filename)
        root_path = os.path.join('document', 'pdf')
        user_path = os.path.join(root_path, str(self.company.pk), time.strftime('%Y/%m'))
        print(os.path.join(user_path, filename))
        return os.path.join(user_path, filename)

    pdf_file = ContentTypeRestrictedFileField(
        verbose_name='資料(PDF)',
        upload_to=get_pdf_uplod_path,
        content_types=['application/pdf'],
        max_upload_size=5242880
    )

    def get_thumb_uplod_path(self, filename):
        filename = normalize_filename(filename)
        root_path = os.path.join('document', 'thumb')
        user_path = os.path.join(root_path, str(self.company.pk), time.strftime('%Y/%m'))
        return os.path.join(user_path, filename)

    thumb_file = ImageField(
        verbose_name = 'サムネイル画像',
        upload_to = get_thumb_uplod_path,
        blank = True,
        default=settings.DEFAULT_THUMBNAIL,
    )

    category =        models.CharField('サービスカテゴリ', max_length=16, choices=SERVICE_CHOICES)
    target_type =     models.CharField('対象業種', max_length=16,choices=TARGET_TYPE_CHOICE)
    target_size =     models.CharField('対象会社規模', max_length=16, choices=TARGET_SIZE_CHOICE)
    catch =           models.TextField('資料概要（キャッチコピー）', max_length=150)
    detail =          models.TextField('資料詳細説明文', max_length=500, blank=True)
    results =         models.TextField('導入実績', max_length=500, blank=True)
    download_status = models.SmallIntegerField('ダウンロード状態', choices=DOWNLOAD_STATUS_CHOICES, default=1, help_text='ダウンロード可否')
    notable_rank =    models.SmallIntegerField('注目ランク', default=0, help_text='注目用。0で非表示、大きい方が上に出ます。0～32767')
    status =          models.SmallIntegerField('公開状態', choices=STATUS_CHOICE, default=0)
    add_date =        models.DateTimeField('登録日', auto_now_add=True)
    update_date =     models.DateTimeField('更新日', auto_now=True)

    objects = DocumentManager()

    def __unicode__(self):
        return self.title

    def id_sign(self):
        sign = signing.dumps(
            {'id' : self.id}
        )
        return sign

    def get_absolute_url(self):
        return reverse('document_detail', kwargs={'document_id':self.pk})

    def get_download_url(self):
        return reverse('document_download', kwargs={'document_id':self.pk})

    class Meta:
        verbose_name = "資料"
        verbose_name_plural = "資料"
        ordering = ['-update_date']


class DocumentDownloadUserManager(models.Manager):
    pass

class DocumentDownloadUser(models.Model):
    document =    models.ForeignKey(Document, verbose_name='資料')
    user =        models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='DLしたユーザー', db_index=True)
    update_date = models.DateTimeField('最新ダウンロード日', auto_now=True)
    add_date =    models.DateTimeField('初回ダウンロード日', auto_now_add=True)
    objects = DocumentDownloadUserManager()
    def __unicode__(self):
        return self.document.title
    class Meta:
        verbose_name = "ダウンロードユーザー"
        verbose_name_plural = "ダウンロードユーザー"
        ordering = ['-update_date']
        unique_together = ("document", "user")

class DocumentDownloadCountManager(models.Manager):
    pass

class DocumentDownloadCount(models.Model):
    document = models.ForeignKey(Document, verbose_name='資料', unique=True)
    count =    models.IntegerField(verbose_name='ダウンロード数', default=0)
    update_date = models.DateTimeField('更新日', auto_now=True)
    objects = DocumentDownloadCountManager()
    def __unicode__(self):
        return self.document.title
    class Meta:
        verbose_name = "ダウンロード数"
        verbose_name_plural = "ダウンロード数"
        ordering = ['-count']


class DocumentDownloadLogManager(models.Manager):
    pass

class DocumentDownloadLog(models.Model):
    download_date =   models.DateTimeField('ダウンロード日', auto_now_add=True)
    # Document
    document_id =     models.IntegerField(verbose_name='資料ID', null=True, blank=True)
    document_title =  models.CharField('資料タイトル', max_length=255)
    # Company
    company =         models.ForeignKey(Company, verbose_name='掲載企業', null=True, blank=True, on_delete=models.SET_NULL)
    # MyUser
    user_id =         models.IntegerField(verbose_name='ユーザーID', null=True, blank=True)
    email =           models.CharField('メールアドレス', max_length=255)
    # MyUserProfile
    last_name =       models.CharField('姓', max_length=64)
    first_name =      models.CharField('名', max_length=64)
    last_name_kana =  models.CharField('姓（ふりがな）', max_length=64)
    first_name_kana = models.CharField('名（ふりがな）', max_length=64)
    company_name =    models.CharField('会社名', max_length=255)
    tel =             models.CharField('電話番号', max_length=20)
    fax =             models.CharField('FAX', max_length=20, blank=True)
    post_number =     models.CharField('郵便番号', max_length=7)
    prefecture =      models.CharField('都道府県', max_length=16)
    address =         models.CharField('住所', max_length=255)
    site_url =        models.CharField('ホームページURL', max_length=255, blank=True)
    department =      models.CharField('部署名', max_length=255)
    position =        models.CharField('役職名', max_length=255, blank=True)
    position_class =  models.CharField('役職区分', max_length=64)
    business_type =   models.CharField('業種', max_length=64)
    job_content =     models.CharField('職務内容', max_length=64)
    firm_size =       models.CharField('従業員規模', max_length=64)
    yearly_sales =    models.CharField('年商', max_length=64)
    discretion =      models.CharField('立場', max_length=255)
    # DonwloadForm
    stage =           models.CharField('状況', max_length=255)

    # Other
    ip =              models.CharField('IPアドレス', max_length=64, blank=True)
    ua=               models.CharField('ユーザーエージェント', max_length=256, blank=True)

    objects = DocumentDownloadLogManager()

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

    def __unicode__(self):
        return self.email

    class Meta:
        verbose_name = "ダウンロードログ"
        verbose_name_plural = "ダウンロードログ"
        ordering = ['-download_date']


