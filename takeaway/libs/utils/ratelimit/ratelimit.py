# -*- coding: utf-8 -*- 
from __future__ import absolute_import, division, print_function, with_statement

import time
from functools import update_wrapper

class RatelimitError(Exception):
    def __init__(self, e):
        self.wrapped = e

    def __str__(self):
        return str(self.wrapped)

class RateLimit(object):
    expiration_window = 10

    def __init__(self, redis, key_prefix, limit, per):
        self.reset = (int(time.time()) // per) * per + per
        self.key = key_prefix + str(self.reset)
        self.limit = limit
        self.per = per
        p = redis.pipeline()
        p.incr(self.key)
        p.expireat(self.key, self.reset + self.expiration_window)
        self.current = min(p.execute()[0], limit)

    @property
    def remaining(self):
        r = self.limit - self.current
        if r < 0:
            return 0
        return r

    @property
    def over_limit(self):
        return self.current >= self.limit

def on_over_limit(limit):
    return 'You hit the rate limit: {0}'.format(limit)

def ratelimit(redis, limit, per=60,
              over_limit=on_over_limit,
              scope_func=lambda: "127.0.0.1",
              key_func=lambda: "api"):
    def deco(f):
        def rate_limited(*args, **kwargs):
            key = 'rate-limit/%s/%s/'% (key_func(), scope_func())
            print(key)
            rl = RateLimit(redis, key, limit, per)
            if rl.over_limit:
                raise RatelimitError(over_limit(limit))
            return f(*args, **kwargs)
        return update_wrapper(rate_limited, f)
    return deco

if __name__ == "__main__":
    pass
