# -*- coding: utf-8 -*- 
import os

# TODO move conf to etcd

DOMAIN = os.environ.get('STARTREK_DOMAIN') or 'test.com'
API_HOST = "api.{domain}".format(domain=DOMAIN)

APP_HTTP_PORT = os.environ.get('APP_STARTREK_PORT') or 8000

DEVELOPER_URI = 'http://developer.{domain}'.format(domain=DOMAIN)

MYSQL_TCP_ADDR = os.environ.get('MYSQL_TCP_ADDR') or '127.0.0.1'
MYSQL_TCP_PORT = os.environ.get('MYSQL_TCP_PORT') or 6379 
MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE') or 'test' 

MYSQL_STORE = {
    "farms": {
        "tide_farm": {
            "master":"mysql://root:123456@{addr}:{port}/{database}".format(addr=MYSQL_TCP_ADDR, port=MYSQL_TCP_PORT, database=MYSQL_DATABASE)
        }
    }
}

REDIS_TCP_ADDR = os.environ.get('REDIS_TCP_ADDR') or '127.0.0.1'
REDIS_TCP_PORT = os.environ.get('REDIS_TCP_PORT') or 6379 

REDIS_STORE = {
    'enterprise': {
        'host': REDIS_TCP_ADDR, 'port': REDIS_TCP_PORT,
    },
    'spirit': {
        'host': REDIS_TCP_ADDR, 'port': REDIS_TCP_PORT,
    }
}

OAUTH2_LOGIN_SETTINGS= {
	'weibo': {
	'key':"3557397975",
	'secret':"5c7b0d9499e1b5dbc7d1e13fd9ad6d0e",
	},
} 

SETTINGS = {
    "cookie_secret": "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
    "debug": True,
    'template_path' : os.path.join(os.path.dirname(__file__), 'templates'),
}

SENTRY_APP_KEY = os.environ.get('SENTRY_APP_KEY') or None 
SENTRY_APP_SECRET= os.environ.get('SENTRY_APP_SECRET') or None
SENTRY_HTTP_ADDR = os.environ.get('SENTRY_HTTP_ADDR') or '127.0.0.1'

SENTRY_SETTING = {
    "key": SENTRY_APP_KEY, 
    "secret": SENTRY_APP_SECRET,
    "addr": SENTRY_HTTP_ADDR,
}

# Qiniu

QINIU = {
    "bucket": "tardisimg",
    "access_key": "t41npOZLA4SclwpkPdFm8d_XxwZvWdrZJbMJdp7M",
    "secret_key": "K6VWH41VvoiNOCSBqkVKglDVf_oV9f9ojHyPOB3J"
}

# throttle

THROTTLES = { 
    "app": (100000, 60),
    "ip": (1000, 60),
    "oauth2": (600, 60)
}

if __name__ == "__main__":
    pass

