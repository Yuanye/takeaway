# -*- coding: utf-8 -*- 
from __future__ import absolute_import, division, print_function, with_statement

import datetime

from sqlalchemy import Column, func
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.types import Integer, String, TIMESTAMP, DECIMAL

#from tide.libs.redis.decorator import cache, pcache
from .store import BaseModel, redis, ONE_MINUTE, ONE_HOUR
from .user import UserDAO 
from .food import FoodDAO 

class OrderNotExists(Exception):
    pass

ORDER_STATE = {
    "created": 10,
    "delivery": 20,
    "finished": 40,
    "cancel": -1 
}

class OrderDAO(BaseModel):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True) 
    user_id = Column(Integer)
    total = Column(DECIMAL(5, 2))
    consignee = Column(String)
    phone_num = Column(String)
    address = Column(String)
    state = Column(TINYINT)
    created_at = Column(TIMESTAMP(timezone=False), nullable=False, server_default=func.current_timestamp())

    @hybrid_method
    def owner(self, session):
        return UserDAO.byID(session, self.owner_id) 

    @hybrid_method
    def foods(self, session):
        return OrderDetailDAO.by_order_id(session, self.id) 

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
    def get_all_by_user(cls, session, user_id, offset=None, limit=None): 
        query = session.query(cls).filter(cls.user_id == user_id)
        if offset:
            query = query.offset(offset)
        if limit:
            query = query.limit(limit)
        return query.all() 

    @hybrid_method
    def get_all_by_state(cls, session, state, offset=None, limit=None): 
        query = session.query(cls).filter(cls.state == state)
        if offset:
            query = query.offset(offset)
        if limit:
            query = query.limit(limit)
        return query.all() 

class OrderDetailDAO(BaseModel):
    __tablename__ = 'order_detail'

    id = Column(Integer, primary_key=True) 
    order_id = Column(Integer)
    food_id = Column(Integer)
    amount = Column(Integer)
    price = Column(DECIMAL(5, 2))
    created_at = Column(TIMESTAMP(timezone=False), nullable=False, server_default=func.current_timestamp())

    @hybrid_method
    def add(self, session): 
        try:
            self._commit(session, self)
            return self 
        except Exception as e:
            session.rollback()
            raise e

    @hybrid_method
    def food(self, session):
        return FoodDAO.byID(session, self.food_id) 

    @hybrid_method
    def by_order_id(cls, session, order_id): 
        query = session.query(cls).filter(cls.order_id== order_id)
        return query.all() 

if __name__ == "__main__":
    pass
