# -*- coding: utf-8 -*-
import os, time
from django.db import models
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
from accounts.models import Company
from documents.choices import *
from trwk.libs.fields import ImageWithThumbsField, ContentTypeRestrictedFileField
from trwk.libs.file_utils import normalize_filename

# Create your models here.

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
        #upload_to='document/pdf',
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

    class Meta:
        verbose_name = "資料"
        verbose_name_plural = "資料"
        ordering = ['-update_date']
