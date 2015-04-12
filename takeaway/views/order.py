# -*- coding: utf-8 -*- 
from __future__ import absolute_import, division, print_function, with_statement

from tornado.web import HTTPError

from .base import APIHandler
from takeaway.models.order import ORDER_STATE, OrderDAO, OrderDetailDAO
from takeaway.models.food import FoodDAO
from takeaway.models.cart import CartDAO

def json_order(db_session, order):
    _order = order.to_dict() 
    _order["foods"] = []

    order_detail_list = OrderDetailDAO.by_order_id(db_session, order.id)
    for detail in order_detail_list:
        food  = FoodDAO.byID(db_session, detail.food_id)
        _food = detail.to_dict()
        _food["name"] = food.name
        _food["cover"] = food.cover
        _order["foods"].append(_food)
    return _order

class OrderHandler(APIHandler):

    def get(self):
        """
        {
            [
                {
                    "id": 123,
                    "state": 10,
                    "total": 50,
                    "created_at": "2015-03-15",
                    "foods": [
                        {"id": 1,
                        "order_id": 10,
                        "cover": "http://test.com/rice.jpg",
                        "name": "Apple",
                        "price": 15,
                        "amount": 1}
                    ]
                },
            ]
            }
        """
        offset = self.get_argument("offset", 0)
        limit = self.get_argument("limit", 50)
        state = self.get_argument("state",  ORDER_STATE["pre-delivery"])
        orders = OrderDAO.get_all_by_state(self.db_session, state, offset=offset, limit=limit)

        _ = []
        for order in orders:
            _.append(json_order(self.db_session, order))

        self._data = _
        self.make_response()
        return

    # TODO require create privilege 
    def post(self):
        cart_ids = self.get_argument("cart_ids", [])
        if cart_ids:
            carts = [CartDAO.byID(self.db_session, cart_id) for cart_id in cart_ids]

            # Create Order
            total = 0
            for cart in carts:
                food = FoodDAO.byID(self.db_session, cart.food_id)
                total = food.price * cart.amount

            order = OrderDAO()
            order.user_id = self.current_user_id
            order.total = total
            order.state = ORDER_STATE["pre-delivery"] 

            order = order.add(self.db_session)

            for cart in carts:
                # add order detail
                order_detail = OrderDetailDAO()
                order_detail.order_id = order.id
                order_detail.food_id = cart.food_id
                order_detail.price = cart.price
                order_detail.add(self.db_session)
                # delete cart detail
                cart.delete(self.db_session, cart.id)

            self._data = json_order(self.db_session, order)
            self.make_response()
            return

        self._errors["message"] = "request failed, validate parameters try again"
        raise HTTPError(422, self._errors["message"])


class OrderDetailHandler(APIHandler):

    def patch(self, order_id):
        state = self.get_argument("state", None) 
        order = OrderDAO.byID(self.db_session, order_id)
        order.state = state
        self._data = json_order(self.db_session, order)
        self.make_response()
        return

    def delete(self, order_id):
        order = OrderDAO.byID(self.db_session, order_id)
        if order.state == ORDER_STATE["created"]:
            order.state = ORDER_STATE["cancel"]
            order.add(self.db_session)
        self._data = json_order(self.db_session, order)
        self.make_response()
        return

class OrderByUserHandler(APIHandler):
    def get(self, user_id):
        orders = OrderDAO.get_all_by_user(self.db_session, self.current_user_id)
        _ = []
        for order in orders:
            _.append(json_order(self.db_session, order))

        self._data = _
        self.make_response()
        return

if __name__ == "__main__":
    pass

