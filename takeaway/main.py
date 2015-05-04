# -*- coding: utf-8 -*- 
from __future__ import absolute_import, division, print_function, with_statement

import tornado.ioloop
import tornado.web

from config import APP_HTTP_PORT, SETTINGS
from takeaway.views.account import (
    AccountHandler, 
    LoginHandler, 
    LogoutHandler, 
    SignupHandler
)
from takeaway.views.category import CategoryHandler
from takeaway.views.cart import CartHandler, CartDetailHandler, CartCountHandler
from takeaway.views.food import (
    FoodHandler, 
    FoodDetailHandler, 
    FoodCategoryHandler,
    FoodHotHandler
)
from takeaway.views.order import OrderHandler, OrderDetailHandler, OrderByUserHandler
from takeaway.views.upload import UploadHandler

application = tornado.web.Application([
    (r"/account", AccountHandler),
    (r"/login", LoginHandler),
    (r"/logout", LogoutHandler),
    (r"/signup", SignupHandler),
    (r"/", FoodHandler),
    (r"/foods", FoodHandler),
    (r"/foods/(\d+)", FoodDetailHandler),
    (r"/foods/hot", FoodHotHandler),
    (r"/categories/(\d+)/foods", FoodCategoryHandler),
    (r"/categories", CategoryHandler),
    (r"/carts", CartHandler),
    (r"/carts/(\d+)", CartDetailHandler),
    (r"/carts/count", CartCountHandler),
    (r"/orders", OrderHandler),
    (r"/orders/(\d+)", OrderDetailHandler),
    (r"/users/(\d+)/orders", OrderByUserHandler),
    (r"/uploads", UploadHandler),
], **SETTINGS)

def main():
    application.listen(APP_HTTP_PORT)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
