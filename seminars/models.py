# -*- coding: utf-8 -*-
import os, time, datetime
from django.db import models
from django.core.mail import send_mail
from django.core import signing
from django.utils import timezone
from django.utils.timezone import utc
from django.conf import settings
from django.core.urlresolvers import reverse
from accounts.models import Company
from seminars.choices import *
from accounts.choices import PREFECTURES_CHOICES
from trwk.libs.fields import ImageWithThumbsField
from trwk.libs.file_utils import normalize_filename
from sorl.thumbnail import ImageField

class SeminarManager(models.Manager):
    pass

class Seminar(models.Model):
    title =       models.CharField('タイトル', max_length=100)
    user =        models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='作成ユーザー', null=True, on_delete=models.SET_NULL)
    company =     models.ForeignKey(Company, verbose_name='掲載企業')
    def get_thumb_uplod_path(self, filename):
        filename = normalize_filename(filename)
        root_path = os.path.join('seminar', 'thumb')
        user_path = os.path.join(root_path, str(self.company.pk), time.strftime('%Y/%m'))
        return os.path.join(user_path, filename)

    thumb_file = ImageField(
        verbose_name = 'イメージ画像',
        upload_to = get_thumb_uplod_path,
        blank = True
    )
    type =            models.SmallIntegerField('種別', choices=TYPE_CHOICES)
    category =        models.CharField('カテゴリー', max_length=16, choices=CATEGORY_CHOICES)
    catch =           models.TextField('概要（キャッチコピー）', max_length=150, help_text='例：今、最も旬なマーケティングツールはこれだ！')
    target =          models.TextField('対象企業', max_length=200, blank=True, help_text='ターゲットとする方がどんな方かご記入ください')
    detail =          models.TextField('詳細説明文', max_length=5000, help_text='セミナーの詳細をご記入ください')
    exhibition_date = models.DateField('開催日', help_text='例：2013-05-01')
    close_date =      models.DateField('終了日', blank=True, help_text='例：2013-05-10 一定の期間開催する場合はご記入ください。')
    exhibition_time = models.CharField('開催時間', max_length=50, help_text='例：18:00 - 20:00')
    accepting_start = models.CharField('受付開始時間', max_length=50, help_text='例：17:30受付開始')
    promoter =        models.CharField('主催者', max_length=50, help_text='例：株式会社ミロク情報サービス')
    capacity =        models.CharField('定員', max_length=50, help_text='例：50名')
    expenses =        models.CharField('費用', max_length=50, help_text='例：5,000円')
    place_name=       models.CharField('会場名', max_length=100, help_text='例：新宿センタービル')
    prefecture =      models.SmallIntegerField('都道府県', choices=PREFECTURES_CHOICES)
    address =         models.CharField('会場住所', max_length=255)
    place_url =       models.URLField('会場に関するURL',blank=True, help_text='施設のサイトURL、GoogleマップのURL等')
    limit_number =    models.IntegerField('申し込み上限数', help_text='半角数字でご入力ください。システムで利用する数字です。申し込み数がこの数に達すると満員となり、申し込みができなくなります。')
    limit_datetime =  models.DateTimeField('申し込み終了時間', blank=True, help_text='この時刻を過ぎると申し込みができなくなります。')
    mail_title =      models.CharField('自動返信メールタイトル', max_length=50, help_text='例：マーケティングセミナー受付完了')
    mail_text =       models.TextField('自動返信メール本文', max_length=2000, help_text='申し込み完了メールに記載される文章です。詳細、連絡先などを必ずご記入ください。')
    entry_status =    models.SmallIntegerField('受付状態', choices=ENTRY_STATUS_CHOICES, default=1, help_text='満員になると自動で受付終了になります。再開する場合は手動でご変更ください。')
    notable_rank =    models.SmallIntegerField('注目ランク', default=0, help_text='注目用。0で非表示、大きい方が上に出ます。0～32767')
    status =          models.SmallIntegerField('公開状態', choices=STATUS_CHOICES, default=0)
    add_date =        models.DateTimeField('登録日', auto_now_add=True)
    update_date =     models.DateTimeField('更新日', auto_now=True)

    objects = SeminarManager()
    def is_open(self):
        #print(self.limit_datetime)
        #print(datetime.datetime.utcnow().replace(tzinfo=utc))
        if self.limit_datetime < datetime.datetime.utcnow().replace(tzinfo=utc):
            return False
        else:
            return True

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('seminar_detail', kwargs={'seminar_id':self.pk})

    def get_entry_url(self):
        return reverse('seminar_entry', kwargs={'seminar_id':self.pk})

    class Meta:
        verbose_name = "セミナー"
        verbose_name_plural = "セミナー"
        ordering = ['-add_date']


class SeminarEntryUserManager(models.Manager):
    def count_entry(self, seminar):
        return self.filter(seminar=seminar).count()

    def is_entered(self, seminar, user):
        if self.filter(seminar=seminar, user=user).count():
            return True
        else:
            return False

class SeminarEntryUser(models.Model):
    seminar =     models.ForeignKey(Seminar, verbose_name='セミナー')
    user =        models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='参加したユーザー', db_index=True)
    add_date =    models.DateTimeField('申し込み日', auto_now_add=True)
    objects = SeminarEntryUserManager()
    def __unicode__(self):
        return self.seminar.title
    class Meta:
        verbose_name = "申し込みユーザー"
        verbose_name_plural = "申し込みユーザー"
        ordering = ['-add_date']

class SeminarEntryLogManager(models.Manager):
    pass

class SeminarEntryLog(models.Model):
    entry_date =       models.DateTimeField('申し込み日', auto_now_add=True)
    # Seminar
    seminar_id =       models.IntegerField(verbose_name='セミナーID', null=True, blank=True)
    seminar_title =    models.CharField('セミナータイトル', max_length=255)
    seminar_type =     models.CharField('種別', max_length=10)
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
    note =             models.CharField('備考', max_length=500)

    # Other
    ip =               models.CharField('IPアドレス', max_length=64, blank=True)
    ua=                models.CharField('ユーザーエージェント', max_length=256, blank=True)

    objects = SeminarEntryLogManager()

    csv_fields = {
                1  : ('申し込み日',       'entry_date'),
                2  : ('セミナータイトル', 'seminar_title'),
                3  : ('種別',             'seminar_type'),
                4  : ('会社名',           'company_name'),
                5  : ('姓',               'last_name'),
                6  : ('名',               'first_name'),
                7  : ('姓（ふりがな）',   'last_name_kana'),
                8  : ('名（ふりがな）',   'first_name_kana'),
                9  : ('電話番号',         'tel'),
                10 : ('FAX',              'fax'),
                11 : ('郵便番号',         'post_number'),
                12 : ('都道府県',         'prefecture'),
                13 : ('住所',             'address'),
                14 : ('ホームページURL',  'site_url'),
                15 : ('部署名',           'department'),
                16 : ('役職名',           'position'),
                17 : ('役職区分',         'position_class'),
                18 : ('業種',             'business_type'),
                19 : ('職務内容',         'job_content'),
                20 : ('従業員規模',       'firm_size'),
                21 : ('年商',             'yearly_sales'),
                22 : ('立場',             'discretion'),
                23 : ('備考',             'note'),
    }
    csv_fields_operation = dict(csv_fields.items() + {
                23 : ('ユーザーID',   'user_id'),
                24 : ('IP',           'ip'),
                25 : ('UA',           'ua'),
    }.items())

    def __unicode__(self):
        return self.email

    class Meta:
        verbose_name = "申し込みログ"
        verbose_name_plural = "申し込みログ"
        ordering = ['-entry_date']
