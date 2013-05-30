# -*- encoding: utf-8 -*-
from datetime import datetime
from documents.models import Document, DocumentDownloadLog
from seminars.models import Seminar, SeminarEntryLog
from django.utils import timezone


def get_all_data_count():
    counts = (
        Document.objects.filter(
            status=1,
            download_status=1,
        ).count(),
        Seminar.objects.filter(
            status=1,
            entry_status=1,
            limit_datetime__gt=datetime.utcnow().replace(tzinfo=timezone.utc)
        ).count(),
    )
    return sum(counts)


def get_all_log_count():
    counts = (
        DocumentDownloadLog.objects.count(),
        SeminarEntryLog.objects.count(),
    )
    return sum(counts)
