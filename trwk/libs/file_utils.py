# -*- encoding: utf-8 -*-
import re
import os
import time


def normalize_filename(filename):
    if re.match('^[0-9a-zA-Z\-\._]+$', filename) is None:
        print('match!!!!!!!!!!!!!!!!!!!!!!!')
        name, ext = os.path.splitext(filename)
        filename = time.strftime('%Y%m%d%H%M%S') + ext
        return filename
    print('not match ???????????????????')
    return filename
