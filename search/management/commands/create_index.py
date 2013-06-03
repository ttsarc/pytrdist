# -*- encoding: utf-8 -*-
from django.core.management.base import BaseCommand
from documents.models import Document
from seminars.models import Seminar
from search.models import Search
from search.libs import update_all_seach_data
from django.db import connection


class Command(BaseCommand):
    def handle(self, *args, **options):
        #reset table
        search = Search.objects.all()
        search.delete()
        cursor = connection.cursor()
        table_name = Search._meta.db_table
        cursor.execute('ALTER TABLE ' + table_name + ' AUTO_INCREMENT = 1;')
        update_all_seach_data()
