#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import datetime
import time
from hashlib import md5

from qiniu import Auth

from takeaway.config import QINIU

q = Auth(QINIU['access_key'], QINIU['secret_key'])

def generate_file_name(user_id):
    dt = datetime.datetime.today()
    dt = dt.strftime('%Y-%m-%d-')
    filename = '%s%s'%(dt, md5('%s%s'%(user_id, time.time())).hexdigest())

    return filename

if __name__ == "__main__":
    pass
