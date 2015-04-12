# -*- coding: utf-8 -*- 
from __future__ import absolute_import, division, print_function, with_statement

import datetime

from sqlalchemy import Column, func
#from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.types import Integer, String, TIMESTAMP, Text, DECIMAL

#from tide.libs.redis.decorator import cache, pcache, delete_cache
from .store import BaseModel, redis, ONE_MINUTE, ONE_HOUR
from .category import CategoryDAO 

class FoodNotExists(Exception):
    pass

class FoodDAO(BaseModel):

    __tablename__ = 'food'

    id = Column(Integer, primary_key=True) 
    category_id = Column(Integer)
    name = Column(String)
    price = Column(DECIMAL(5, 2))
    cover = Column(String)
    records = Column(Integer)
    created_at = Column(TIMESTAMP(timezone=False), nullable=False, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP(timezone=False), nullable=False, server_default=func.current_timestamp())

    @hybrid_method
    def category(self, session):
        return CategoryDAO.byID(session, self.category_id) 

    @hybrid_method
    def add(self, session): 
        now = datetime.datetime.now()
        self.updated_at = now
        try:
            self._commit(session, self)
            return self 
        except Exception as e:
            session.rollback()
            raise e

    @hybrid_method
    def incr_records(self, session, count): 
        now = datetime.datetime.now()
        self.updated_at = now
        self.records = self.records + count
        try:
            self._commit(session, self)
            return self 
        except Exception as e:
            session.rollback()
            raise e

    @hybrid_method
    def get_all_by_category(cls, session, category_id, offset=None, limit=None): 
        query = session.query(cls).filter(cls.category_id == category_id).order_by(cls.created_at)
        if offset:
            query = query.offset(offset)
        if limit:
            query = query.limit(limit)
        return query.all() 

    @hybrid_method
    def get_all_by_records(cls, session, offset=None, limit=None): 
        query = session.query(cls).order_by(cls.records)
        if offset:
            query = query.offset(offset)
        if limit:
            query = query.limit(limit)
        return query.all() 

if __name__ == "__main__":
    pass
