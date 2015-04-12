# -*- coding: utf-8 -*- 
from __future__ import absolute_import, division, print_function, with_statement
import datetime

from tornado.web import HTTPError, authenticated

from .base import APIHandler
from takeaway.models.food import FoodDAO 
from takeaway.models.form import FoodForm

class FoodHandler(APIHandler):

    def get(self):
        offset = self.get_argument("offset", 0)
        limit = self.get_argument("limit", 50)
        foods = FoodDAO.get_all(self.db_session, offset=offset, limit=limit)
        self._data = [food.to_dict() for food in foods]
        self.make_response()
        return

    def post(self):
        now = datetime.datetime.now()
        arguments = self.json_arguments
        form = FoodForm(**arguments)
        user_id = self.current_user_id
        arguments["records"] = 0

    
        if form.validate():
            post = FoodDAO(**arguments)
            post.created_at = now
            try:
                post = post.add(self.db_session)
                self._data = post.to_dict()
                self.make_response()
                return
            except Exception as e:
                print(e)

        self._errors["message"] = "request failed, validate parameters try again"
        raise HTTPError(422, self._errors["message"])

class FoodDetailHandler(APIHandler):

    def prepare(self):
        super(FoodDetailHandler, self).prepare()
        try:
            self.food_id = self.path_args[0]
            self.food = FoodDAO.byID(self.db_session, self.food_id)
        except Exception as e:
            self._errors["message"] = "request failed, the specified resource does not exist"
            raise HTTPError(404, self._errors["message"])
            return
        self.owner_id = self.post.owner_id

    def get(self, food_id):
        # Add has mark & like
        self._data = self.food.to_dict()
        self.make_response()
        return

    def patch(self, food_id):
        arguments = self.json_arguments
        if self.current_user_id != self.owner_id:
            self._errors["code"] = "forbidden"
            self._errors["message"] = "request failed, validate parameters try again"
            raise HTTPError(403, self._errors["message"])

        for k,v in arguments:
            self.food[k] = v 

        post = self.post.add(self.db_session)
        self._data = post.to_dict()
        self.make_response()
        return

class FoodCategoryHandler(APIHandler):

    def get(self, category_id):
        offset = self.get_argument("offset", 0)
        limit = self.get_argument("limit", 50)
        foods = FoodDAO.get_all_by_category(self.db_session, category_id, offset=offset, limit=limit)
        self._data = [food.to_dict() for food in foods]
        self.make_response()
        return

class FoodHotHandler(APIHandler):

    def get(self, category_id):
        offset = self.get_argument("offset", 0)
        limit = self.get_argument("limit", 50)

        foods = FoodDAO.get_all_by_records(self.db_session, offset=offset, limit=limit)
        self._data = [food.to_dict() for food in foods]
        self.make_response()
        return

if __name__ == "__main__":
    pass
