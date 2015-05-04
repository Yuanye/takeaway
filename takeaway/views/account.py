# -*- coding: utf-8 -*- 
from __future__ import absolute_import, division, print_function, with_statement

import datetime

#from tornado.escape import json_decode
from tornado.web import HTTPError

from .base import APIHandler
from takeaway.config import DOMAIN
from takeaway.models.user import UserDAO 
from takeaway.models.form import LoginForm, SignupForm

class AccountHandler(APIHandler):

    def prepare(self):
        super(AccountHandler, self).prepare()
        if not self.current_user:
            self.make_response()
            return

    def get(self):
        self._data = self.current_user.to_dict()
        self.make_response()

class LoginHandler(APIHandler):

    def prepare(self):
        super(LoginHandler, self).prepare()
        if self.current_user:
            next_url = self.get_argument('next', "/")
            self.redirect(next_url)
            return

    def post(self):
        form = LoginForm(**self.json_arguments)
        name = self.get_argument("name", None)
        password = self.get_argument("password", None)
        if form.validate():
            try:
                user = UserDAO.by_name(self.db_session, name)
                if user and user.validate_password(password):
                    user.login(self.db_session)
                    self.login(user)
                    return
                # username and password  didn't match
                raise None
            except Exception as e:
                print(e)
                self._errors["message"] = "request failed, your username and password didn't match. Please try again. "
                raise HTTPError(422, self._errors["message"])

        #self._errors["message"] = "request failed, validate parameters try again"
        raise HTTPError(422, self._errors["message"])

class LogoutHandler(APIHandler):

    def get(self):
        if self.current_user:
            self.clear_cookie('S', domain=DOMAIN)
            next_url = self.get_argument('next', "")
            if next_url:
                self.redirect(next_url)
            return

class SignupHandler(APIHandler): 

    def post(self):
        arguments = self.json_arguments
        form = SignupForm(**self.json_arguments)
        phone_num = arguments["phone_num"]
        name = arguments["name"]
        password = arguments["password"]

        if form.validate():
            try:
                UserDAO.by_name(self.db_session, name)
                self._errors["message"] = "request failed, name already used"
            except Exception as e:
                print(e)
                pass

            if self._errors["message"]:
                raise HTTPError(422, self._errors["message"])

            password = UserDAO.hash_password(password)
            user = UserDAO()
            user.name = name
            user.phone_num = phone_num 
            user.password = password
            user.session_id = UserDAO.generate_token()
            user.created_at = datetime.datetime.now()
            try:
                user = user.add(self.db_session)
            except Exception as e:
                print(e)
                raise HTTPError(500)

            #TODO sendmail
            self.login(user)
            return

        self._errors["message"] = "request failed, validate parameters try again"
        raise HTTPError(422, self._errors["message"])
        return

if __name__ == "__main__":
    pass
