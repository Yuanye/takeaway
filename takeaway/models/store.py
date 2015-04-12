# -*- coding: utf-8 -*- 
from __future__ import absolute_import, division, print_function, with_statement

import datetime
import decimal

from redis import StrictRedis 
from sqlalchemy import create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from tornado.util import ObjectDict

from takeaway.config import MYSQL_STORE, REDIS_STORE
from takeaway.libs.redis.decorator import cache, pcache, delete_cache
from takeaway.libs.utils.json_dict import JsonDict

# redis
redis = StrictRedis(**REDIS_STORE['enterprise'])
#TODO add redis cache instance

ONE_MINUTE = 60
HALF_HOUR = 1800
ONE_HOUR = 3600
HALF_DAY = ONE_HOUR * 12
ONE_DAY = ONE_HOUR * 24
ONE_WEEK = ONE_DAY * 7
ONE_MONTH = ONE_DAY * 30
ONE_YEAR = ONE_DAY * 365

# session 
engine = create_engine("{0}?charset=utf8".format(MYSQL_STORE["farms"]["tide_farm"]["master"]))
DB_Session = sessionmaker(bind=engine)
#DB_Session = sessionmaker(bind=engine, expire_on_commit=False)

# Base Model
#BaseModel = declarative_base()

#class ModelMixin(JsonDict):
class ModelMixin(object):

    @classmethod
    def byID(cls, session, id, columns=None, lock_mode=None):
        if hasattr(cls, 'id'):
            scalar = False
            if columns:
                if isinstance(columns, (tuple, list)):
                    query = session.query(*columns)
                else:
                    scalar = True
                    query = session.query(columns)
            else:
                query = session.query(cls)
            if lock_mode:
                query = query.with_lockmode(lock_mode)
            query = query.filter(cls.id == id)
            if scalar:
                u = query.scalar()
                if not u:
                    raise None 
                return  u
            try:
                return query.one()
            except Exception as e:
                raise e
        raise None 

    @classmethod
    def get_all(cls, session, columns=None, offset=None, limit=None, order_by=None, lock_mode=None):
        if columns:
            if isinstance(columns, (tuple, list)):
                query = session.query(*columns)
            else:
                query = session.query(columns)
                if isinstance(columns, str):
                    query = query.select_from(cls)
        else:
            query = session.query(cls)
        if order_by is not None:
            if isinstance(order_by, (tuple, list)):
                query = query.order_by(*order_by)
            else:
                query = query.order_by(order_by)
        elif hasattr(cls, 'created_at'):
            query = query.order_by(cls.id.desc())

        if offset:
            query = query.offset(offset)
        if limit:
            query = query.limit(limit)
        if lock_mode:
            query = query.with_lockmode(lock_mode)
        return query.all()

    @classmethod
    def count_all(cls, session, lock_mode=None):
        query = session.query(func.count('*')).select_from(cls)
        if lock_mode:
            query = query.with_lockmode(lock_mode)
        return query.scalar()

    @classmethod
    def exist(cls, session, id, lock_mode=None):
        if hasattr(cls, 'id'):
            query = session.query(func.count('*')).select_from(cls).filter(cls.id == id)
            if lock_mode:
                query = query.with_lockmode(lock_mode)
            return query.scalar() > 0
        return False

    @classmethod
    def delete(cls, session, id):
        if hasattr(cls, 'is_deleted'):
            cls.set_attrs(session, 'is_deleted', 1)
            return
        #TODO delete detail cache & count all cache
        session.query(cls).filter(cls.id==id).delete()
        session.commit()

    @classmethod
    def set_attr(cls, session, id, attr, value):
        if hasattr(cls, 'id'):
            session.query(cls).filter(cls.id == id).update({
                attr: value
            })
            session.commit()

    @classmethod
    def set_attrs(cls, session, id, attrs):
        if hasattr(cls, 'id'):
            session.query(cls).filter(cls.id == id).update(attrs)
            session.commit()

    @classmethod
    def _commit(cls, session, row):
        session.add(row)
        session.flush()
        session.commit()
        #session.refresh(row)

    def to_dict(self):
        """
        只有当class 有 __init__ 方法的时候, instance的self.__dict__ 才不为空
        """
        #_ = ObjectDict()
        #for name, value in self.__dict__.iteritems():
        #    if not name.startswith('_'):
        #        if isinstance(value, datetime.datetime):
        #            value = str(value)
        #        _[name] = value
        #return _

        _ = ObjectDict()
        for name in dir(self):
            if not name.startswith('_'):
                value = self.__getattribute__(name)
                # TODO 需要将所有的输入输出都要转化为同一个字符类型
                #print(name, value, type(value))
                if isinstance(value, (unicode, str, int, long, dict)):
                    _[name] =  value
                if isinstance(value, datetime.datetime):
                    _[name] =  str(value)
                if isinstance(value, decimal.Decimal):
                    _[name] = str(value)
                elif isinstance(value, ModelMixin):
                    _[name] = value.to_dict()
        return _

BaseModel = declarative_base(cls=ModelMixin)

if __name__ == "__main__":
    pass
