# -*- encoding: utf-8 -*-
import re, os, time

def normalize_filename(filename):
    if re.match('^[0-9a-zA-Z\-\._]+$', filename) == None :
        print('match!!!!!!!!!!!!!!!!!!!!!!!')
        name, ext = os.path.splitext(filename)
        filename = time.strftime('%Y%m%d%H%M%S') + ext
        return filename
    print('not match ???????????????????')
    return filename
