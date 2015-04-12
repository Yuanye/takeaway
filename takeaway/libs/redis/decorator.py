# -*- coding: utf-8 -*-

''' redis cache decorator '''
import sys
import inspect
import time
from functools import wraps
from warnings import warn
import cPickle as pickle

import msgpack

from takeaway.libs.utils.format import format

def gen_key(key_pattern, arg_names, defaults, *a, **kw):
    return gen_key_factory(key_pattern, arg_names, defaults)(*a, **kw)

def gen_key_factory(key_pattern, arg_names, defaults):
    args = dict(zip(arg_names[-len(defaults):], defaults)) if defaults else {}
    if callable(key_pattern):
        names = inspect.getargspec(key_pattern)[0]
    def gen_key(*a, **kw):
        aa = args.copy()
        aa.update(zip(arg_names, a))
        aa.update(kw)
        if callable(key_pattern):
            key = key_pattern(*[aa[n] for n in names])
        else:
            key = format(key_pattern, *[aa[n] for n in arg_names], **aa)
        return key and  key.replace(' ', '_'), aa
    return gen_key

def cache(key_pattern, redis, expire=60, max_retry=0 ):
    def deco(f):
        arg_names, varargs, varkw, defaults = inspect.getargspec(f)
        if varargs or varkw:
            raise Exception("do not support varargs")
        gen_key = gen_key_factory(key_pattern, arg_names, defaults)
        @wraps(f)
        def _(*a, **kw):
            key, args = gen_key(*a, **kw)
            if not key:
                return f(*a, **kw)
            force = kw.pop('force', False)
            r = redis.get(key) if not force else None

            retry = max_retry
            while r is None and retry > 0:
                if redis.set(key + '#mutex', 1, int(max_retry * 0.1)):
                    break
                time.sleep(0.1)
                r = redis.get(key)
                retry -= 1
            if r is None:
                r = f(*a, **kw)
                try:
                    _r = msgpack.dumps(r)
                except Exception as e:
                    _r = pickle.dumps(r)
                redis.set(key, _r, expire)
            else:
                try:
                    r = msgpack.loads(r)
                except Exception as e:
                    try:
                        r = pickle.loads(r)
                    except Exception as e:
                        pass
            if max_retry > 0:
                redis.delete(key + '#mutex')
            return r
        _.original_function = f
        return _
    return deco

def pcache(key_pattern, redis, count=300, expire=60, max_retry=0):
    def deco(f):
        arg_names, varargs, varkw, defaults = inspect.getargspec(f)
        if varargs or varkw:
            raise Exception("do not support varargs")
        if not ('limit' in arg_names):
            raise Exception("function must has 'limit in args'")
        gen_key = gen_key_factory(key_pattern, arg_names, defaults)
        @wraps(f)
        def _(*a, **kw):
            key, args = gen_key(*a, **kw)
            offset = args.pop('offset', 0)
            limit = args.pop('limit')
            if not key or limit is None or offset+limit > count:
                return f(*a, **kw)

            force = kw.pop('force', False)
            r = redis.get(key) if not force else None

            retry = max_retry
            while r is None and retry > 0:
                if redis.set(key + '#mutex', 1, int(max_retry * 0.1)):
                    break
                print >>sys.stderr, "@cache(): wait for", key, 'to return'
                time.sleep(0.1)
                r = redis.get(key)
                retry -= 1
            if r is None:
                r = f(offset=0,limit=count, **args)
                try:
                    _r = msgpack.dumps(r)
                except Exception:
                    _r = pickle.dumps(r)
                redis.set(key, _r, expire)
            else:
                try:
                    r = msgpack.loads(r)
                except Exception as e:
                    r = pickle.loads(r)
            redis.delete(key + '#mutex')
            return r[offset:offset+limit]
        _.original_function = f
        return _
    return deco

def listcache(key_pattern, redis, expire=60):
    def deco(f):
        arg_names, varargs, varkw, defaults = inspect.getargspec(f)
        if varargs or varkw:
            raise Exception("do not support varargs")
        gen_key = gen_key_factory(key_pattern, arg_names, defaults)
        @wraps(f)
        def _(*a, **kw):
            key, args = gen_key(*a, **kw)
            if not key:
                return f(*a, **kw)
            force = kw.pop('force', False)
            r = redis.get(key) if not force else None
            if r is not None:
                r = msgpack.loads(r)
            else:
                r = f(*a, **kw)
                if isinstance(r, (list, tuple)):
                    redis.set(key, r, expire)
                else:
                    warn("func %s (%s) should return list or tuple" % (f.__name__, key))
            return r
        _.original_function = f
        return _
    return deco

def delete_cache(key_pattern, redis):
    def deco(f):
        try:
            arg_names, varargs, varkw, defaults = inspect.getargspec(f.original_function)
        except:
            arg_names, varargs, varkw, defaults = inspect.getargspec(f)
        if varargs or varkw:
            raise Exception("do not support varargs")
        gen_key = gen_key_factory(key_pattern, arg_names, defaults)
        @wraps(f)
        def _(*a, **kw):
            key, args = gen_key(*a, **kw)
            r = f(*a, **kw)
            redis.delete(key)
            return r
        _.original_function = f
        return _
    return deco
