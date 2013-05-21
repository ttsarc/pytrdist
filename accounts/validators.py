# -*- encoding: utf-8 -*-
from django.core.validators import RegexValidator
import re
TelFaxValidaor = RegexValidator(
    regex=re.compile(r'^[0-9]+[0-9\-]{4,12}[0-9]+$'),
    message='電話番号、Fax番号は半角英数字と-（ハイフン）で入力をお願い致します'
)

PostNumberValidaor = RegexValidator(
    regex=re.compile(r'^([0-9]{7})$'),
    message='郵便番号は半角数字7桁（例：1630648）でお願い致します'
)
