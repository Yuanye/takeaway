# -*- coding: utf-8 -*- 
from __future__ import absolute_import, division, print_function, with_statement
import datetime

from tornado.web import HTTPError

from .base import APIHandler
from takeaway.models.cart import CartDAO 
from takeaway.models.food import FoodDAO 
from takeaway.models.form import CartForm


class CartHandler(APIHandler):

    def get(self):
        user_id = self.current_user_id
        offset = self.get_argument("offset", 0)
        limit = self.get_argument("limit", 50)
        cart_list = CartDAO.get_all_by_user(self.db_session, user_id, offset=offset, limit=limit)

        cart_list = [cart.to_dict() for cart in cart_list]
        for cart in cart_list:
            cart["food"] = FoodDAO.byID(self.db_session, cart["food_id"]).to_dict()

        self._data = cart_list
        self.make_response()
        return

    def post(self):
        user_id = self.current_user_id
        now = datetime.datetime.now()
        arguments = self.json_arguments
        arguments["user_id"] = user_id
        form = CartForm(**arguments)
        if form.validate():
            food_id = self.get_argument("food_id", None)
            amount = self.get_argument("amount", 0)
            cart = CartDAO.get_by_user_and_food(self.db_session, user_id, food_id)
            # TODO check amount == 0
            if cart:
                cart.amount = amount
            else:
                cart = CartDAO(**arguments)
                cart.created_at = now
            cart.updated_at = now
            try:
                cart = cart.add(self.db_session).to_dict()
                cart["food"] = FoodDAO.byID(self.db_session, cart.food_id).to_dict()
                self._data = cart
                self.make_response()
                return
            except Exception as e:
                print(e)

        self._errors["message"] = "request failed, validate parameters try again"
        raise HTTPError(422, self._errors["message"])

class CartDetailHandler(APIHandler):

    def delete(self):
        user_id = self.current_user_id
        cart_id = self.get_argument("cart_id", 0)
        cart= CartDAO.byID(self.db_session, cart_id)

        # Authorized
        if cart.user_id == user_id:
            self.make_response()
            cart.delete(self.db_session, cart_id)
            cart["food"] = FoodDAO.byID(self.db_session, cart.food_id).to_dict()
            self._data = cart.to_dict()
            self.make_response()
            return

        self._errors["message"] = "request not authorized, provided credentials do not provide access to specified resource" 
        raise HTTPError(403, self._errors["message"])

class CartCountHandler(APIHandler):
    def get(self):
        user_id = self.current_user_id
        count = CartDAO.count(self.db_session, user_id)
        self._data["count"] = count
        self.make_response()
        return

if __name__ == "__main__":
    pass

