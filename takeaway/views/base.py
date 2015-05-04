# -*- coding: utf-8 -*- 
from __future__ import absolute_import, division, print_function, with_statement

import re
import time

from mako.lookup import TemplateLookup
import tornado.web
from tornado.web import HTTPError
from tornado.escape import json_encode, json_decode
from tornado.log import access_log, app_log, gen_log

from takeaway.config import DOMAIN, DEVELOPER_URI
from takeaway.libs.utils import http_utils
from takeaway.models.user import UserDAO 
from takeaway.models.store import DB_Session


class BaseHandler(tornado.web.RequestHandler):
    """
    """

    def prepare(self):
        # TODO add rate limits
        self._form_errors = {}
        self._start_time = time.time()

        # set headers
        self.set_access_headers()
        # ratelimit ip, access_token

    @property
    def current_user_id(self):
        if not hasattr(self, '_current_user_id'):
            current_user = self.current_user
            if current_user:
                self._current_user_id = current_user.id
            else:
                self._current_user_id = 0
        return self._current_user_id

    def user_id_by_cookie(self):
        s = self.get_cookie("S")
        if s:
            try:
                user = UserDAO.by_session_id(self.db_session, s)
            except Exception as e:
                self.clear_cookie('S')
                return None
            #TODO update last vist 
            return user.id
        return None

    def get_current_user(self):
        user = self.user_id_by_cookie()
        if user:
            return user 
        self.clear_cookie('S')
        return None

    @property
    def user_is_loggedin(self):
        if self.current_user:
            return True
        return False


    def set_access_headers(self):
        #self.set_header("Access-Control-Allow-Origin", "http://{0}".format(DOMAIN))
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods", \
            "GET, POST, PUT, PATCH, DELETE, OPTIONS")
        self.set_header("Access-Control-Allow-Headers", "Authorization, Content-Type, Accept")
        self.set_header("Access-Control-Allow-Credentials", "false")
        self.set_header("Access-Control-Expose-Headers", \
            "X-Ratelimit-Limit, X-Ratelimit-Remaining, X-Ratelimit-Reset")

class MinimalHanlder(BaseHandler):
    def initialize(self):
        self.db_session = DB_Session()
        template_path = self.get_template_path()
        self.lookup = TemplateLookup(directories=[template_path], 
                                     input_encoding='utf-8', 
                                     output_encoding='utf-8') 

    def on_finish(self):
        self.db_session.close()
        self._finish_time = time.time()

    def login(self, user):
        session = user.session_id
        self.set_cookie('S', session, domain=DOMAIN)

    def logout(self, user):
        self.clear_cookie('S', domain=DOMAIN)

    def form_error(self, name, msg):
        self._form_errors[name] = msg

    def render_string(self, template_path, **kwargs):
        template = self.lookup.get_template(template_path)
        return template.render(**kwargs)

    def render(self, template_path, **kwargs):
        kwargs['current_user'] = self.current_user
        kwargs['current_user_id'] = self.current_user_id
        kwargs['_xsrf'] = self.xsrf_token
        self.finish(self.render_string(template_path, **kwargs))

CAMEL_CASE_PATTERN = re.compile(r'([a-z0-9])([A-Z])')
class APIHandler(MinimalHanlder):

    def initialize(self):
        self.db_session = DB_Session()
        self._data = {} 
        self._errors = {} 
        self.set_header('Content-Type', 'application/json; charset=UTF-8')

        if self.user_is_loggedin:
            token  = self.request.headers.get('Authorization', None)
            if token: self.set_header('Authorization', token)

        self._inject_json_arguments()
        super(APIHandler, self).initialize()

    def _inject_json_arguments(self, strip=True):
        try:
            json_arguments = json_decode(self.request.body)
        except Exception as e:
            print(e)
            json_arguments = {}
        for k, v in json_arguments.items():
            if v != None:
                v = unicode(v)
            self.request.arguments.setdefault(k, []).append(v)

    @property
    def json_arguments(self):
        # Tornado's request arguments return key: values, eg: "name": ["jack", ]
        _json_arguments = [(name, args[-1]) for name, args in self.request.arguments.iteritems()]
        return dict(_json_arguments)

    def prepare(self):
        if not self._errors:
            self._errors = {"code": None, "message": None, "url": DEVELOPER_URI}
        super(APIHandler, self).prepare()


    def options(self):
        pass

    def make_response(self):
        self.finish(json_encode(self._data))
        return

    def get_current_user(self):
        user_id = self.user_id_by_authorization()
        # Cookies 不支持跨域
        #if not user_id:
        #    ua  = self.request.headers.get('User-Agent')
        #    if ua.find("iphone") or ua.find("ipad") or ua.find("andriod"):
        #        user_id  = self.user_id_by_cookie()
        if user_id:
            return UserDAO.byID(self.db_session, user_id)
        return None

    def user_id_by_authorization(self):
        token  = self.request.headers.get('Authorization')
        if token:
            token = token.split(" ")[-1]
            user = UserDAO.get_session_id(token)
            return user.id
        else:
            return self.user_id_by_cookie()
        return None

    def login(self, user):
        access_token = user.session_id
        self.set_cookie('S', access_token, domain=DOMAIN)
        self.set_header('Authorization', 'Bearer ' + access_token)
        self._data["access_token"] = access_token
        self.make_response()
        return 

    def logout(self, user):
        self.set_header('Authorization', 'Bearer ')
        self.clear_cookie('S', domain=DOMAIN)
        self.make_response()
        return 

    def send_error(self, status_code=500, **kwargs):
        """Sends the given HTTP error code to the browser.
        If `flush()` has already been called, it is not possible to send
        an error, so this method will simply terminate the response.
        If output has been written but not yet flushed, it will be discarded
        and replaced with the error page.
        Override `write_error()` to customize the error page that is returned.
        Additional keyword arguments are passed through to `write_error`.
        """
        if self._headers_written:
            gen_log.error("Cannot send error response after headers written")
            if not self._finished:
                self.finish()
            return
        # Need keep headers 
        #self.clear()

        reason = kwargs.get('reason')
        if 'exc_info' in kwargs:
            exception = kwargs['exc_info'][1]
            if isinstance(exception, HTTPError) and exception.reason:
                reason = exception.reason
        self.set_status(status_code, reason=reason)
        try:
            self.write_error(status_code, **kwargs)
        except Exception:
            app_log.error("Uncaught exception in write_error", exc_info=True)
        if not self._finished:
            self.finish()

    def write_error(self, status_code, **kwargs):
        code =  self._errors.get('code', None)
        if not code:
            code = http_utils.error_codes[status_code]
            #code = CAMEL_CASE_PATTERN.sub(r'\1_\2', code)
        # send_error will call self.clear() to clear headers before invoke write_error,
        # but, self.prepare will reset self._errors
        #self.prepare()
        self.finish({ "code": code,  "message": self._errors["message"], "url": self._errors["url"]})
        

class OAuth2Handler(APIHandler):

    def initialize(self):
        super(APIHandler, self).initialize()

    def prepare(self):
        super(APIHandler, self).prepare()
        if not self.current_user_id:
            self._errors["message"] = "request not authenticated, API token is missing, invalid or expired"
            raise tornado.web.HTTPError(401, self._errors["message"])

if __name__ == "__main__":
    pass
