# -*- coding: utf-8 -*- 
from __future__ import absolute_import, division, print_function, with_statement
import datetime

from tornado.web import HTTPError

from .base import APIHandler
from takeaway.models.category import CategoryDAO 
from takeaway.models.form import CategoryForm 

class CategoryHandler(APIHandler):

    def get(self):

        categories = CategoryDAO.get_all(self.db_session)
        self._data = [category.to_dict() for category in categories]
        self.make_response()
        return

    def post(self):

        now = datetime.datetime.now()
        arguments = self.json_arguments 
        print(arguments)
        form = CategoryForm(**arguments)
        if form.validate():
            #arguments['name'] = name 

            category = CategoryDAO(**arguments)
            category.created_at = now
            try:
                category = category.add(self.db_session)
                self._data = category.to_dict()
                self.make_response()
                return
            except Exception as e:
                print(e)

        self._errors["message"] = "request failed, validate parameters try again"
        raise HTTPError(422, self._errors["message"])

if __name__ == "__main__":
    pass

