# -*- encoding: utf-8 -*-
import csv, datetime
from django.http import HttpResponse
from django.utils.timezone import utc, make_naive, get_default_timezone

def export_csv(leads, csv_fields, filename = None):
    if filename == None:
        filename = 'trwk-' + datetime.datetime.now().strftime('%Y%m%d-%H%M%S') + '.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="'+ filename +'"'
    writer = csv.writer(response)
    head = []
    first = True
    csv_encode = 'cp932'
    for line in leads:
        items = []
        for key, field in sorted(csv_fields.items()):
            label = field[0]
            name = field[1]
            if first:
                head.append(label.encode( csv_encode ))
            val = getattr(line, name)
            if isinstance(val, unicode):
                items.append(val.encode( csv_encode ))
            elif isinstance(val, long):
                items.append(str(val))
            elif isinstance(val, datetime.datetime):
                #ローカルタイムに変換してる
                items.append(make_naive(val, get_default_timezone()).strftime('%Y-%m-%d %H:%M:%S') )
        if first:
            writer.writerow(head)
            first = False
        writer.writerow(items)
    return response
