# -*- coding: utf-8 -*-
import os, time
from django.db import models
from django.core.mail import send_mail
from django.core import signing
from django.utils import timezone
from django.conf import settings
from accounts.models import Company
from documents.choices import *
from trwk.libs.fields import ImageWithThumbsField, ContentTypeRestrictedFileField
from trwk.libs.file_utils import normalize_filename

class DocumentManager(models.Manager):
    pass

class Document(models.Model):
    title =       models.CharField('タイトル', max_length=40)
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

    thumb_file = ImageWithThumbsField(
        verbose_name = 'サムネイル画像',
        sizes = ((200,200),),
        upload_to = get_thumb_uplod_path,
        blank = True
    )

    category =    models.CharField('サービスカテゴリ', max_length=16, choices=SERVICE_CHOICES)
    target_type = models.CharField('対象業種', max_length=16,choices=TARGET_TYPE_CHOICE)
    target_size = models.CharField('対象会社規模', max_length=16, choices=TARGET_SIZE_CHOICE)
    catch =       models.TextField('資料概要（キャッチコピー）', max_length=150)
    detail =      models.TextField('資料詳細説明文', max_length=500, blank=True)
    results =     models.TextField('導入実績', max_length=500, blank=True)
    status =      models.SmallIntegerField('公開状態', choices=STATUS_CHOICE, default=0)
    add_date =    models.DateTimeField('登録日', auto_now_add=True)
    update_date = models.DateTimeField('更新日', auto_now=True)

    objects = DocumentManager()

    def __unicode__(self):
        return self.title

    def id_sign(self):
        sign = signing.dumps(
            {'id' : self.id}
        )
        return sign

    class Meta:
        verbose_name = "資料"
        verbose_name_plural = "資料"
        ordering = ['-update_date']

class DocumentDownloadLogManager(models.Manager):
    pass

class DocumentDownloadLog(models.Model):
    download_date =    models.DateTimeField('ダウンロード日', auto_now_add=True)
    # Document
    document_id =      models.IntegerField(verbose_name='資料ID', null=True, blank=True)
    document_title =   models.CharField('資料タイトル', max_length=255)
    # Company
    company =          models.ForeignKey(Company, verbose_name='掲載企業', null=True, blank=True, on_delete=models.SET_NULL)
    # MyUser
    user_id =          models.IntegerField(verbose_name='ユーザーID', null=True, blank=True)
    email =            models.CharField('メールアドレス', max_length=255)
    # MyUserProfile
    last_name =        models.CharField('姓', max_length=64)
    first_name =       models.CharField('名', max_length=64)
    last_name_kana =   models.CharField('姓（ふりがな）', max_length=64)
    first_name_kana =  models.CharField('名（ふりがな）', max_length=64)
    company_name =     models.CharField('会社名', max_length=255)
    tel =              models.CharField('電話番号', max_length=20)
    fax =              models.CharField('FAX', max_length=20, blank=True)
    post_number =      models.CharField('郵便番号', max_length=7)
    prefecture =       models.CharField('都道府県', max_length=16)
    address =          models.CharField('住所', max_length=255)
    site_url =         models.CharField('ホームページURL', max_length=255, blank=True)
    department =       models.CharField('部署名', max_length=255)
    position =         models.CharField('役職名', max_length=255, blank=True)
    position_class =   models.CharField('役職区分', max_length=64)
    business_type =    models.CharField('業種', max_length=64)
    job_content =      models.CharField('職務内容', max_length=64)
    firm_size =        models.CharField('従業員規模', max_length=64)
    yearly_sales =     models.CharField('年商', max_length=64)
    discretion =       models.CharField('立場', max_length=255)
    # DonwloadForm
    stage =            models.CharField('状況', max_length=255)

    # Other
    ip =               models.CharField('IPアドレス', max_length=64, blank=True)
    ua=                models.CharField('ユーザーエージェント', max_length=256, blank=True)

    objects = DocumentDownloadLogManager()

    def __unicode__(self):
        return self.email

    class Meta:
        verbose_name = "ダウンロードログ"
        verbose_name_plural = "ダウンロードログ"
        ordering = ['-download_date']
