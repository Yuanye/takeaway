# -*- coding: utf-8 -*- 
from __future__ import absolute_import, division, print_function, with_statement

from tornado import gen

from .base import APIHandler
from takeaway.config import QINIU
from takeaway.libs.upload import q, generate_file_name

class UploadHandler(APIHandler):

    def get(self):
        bucket_name = self.get_argument("bucket_name", QINIU['bucket'])

        key = generate_file_name(self.current_user_id)

        uptoken = q.upload_token(bucket_name, key)
        self._data["key"] = key 
        self._data["uptoken"] = uptoken
        self.make_response()
        return

if __name__ == "__main__":
    pass
