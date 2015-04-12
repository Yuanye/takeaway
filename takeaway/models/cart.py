# -*- coding: utf-8 -*- 
from __future__ import absolute_import, division, print_function, with_statement

from sqlalchemy import Column, func
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.types import Integer, String, TIMESTAMP

from .store import BaseModel
from .user import UserDAO 
from .food import FoodDAO 

class CartNotExists(Exception):
    pass

class CartDAO(BaseModel):

    __tablename__ = 'cart'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    food_id = Column(Integer)
    amount = Column(Integer)
    has_ordered = Column(TINYINT)
    created_at = Column(TIMESTAMP(timezone=False), nullable=False, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP(timezone=False), nullable=False, server_default=func.current_timestamp())

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
    def count(cls, session, user_id):
        query = session.query(cls).filter(
            cls.user_id == user_id).filter(
            cls.has_ordered == 0)
        return query.count()

    @hybrid_method
    def get_by_user_and_food(cls, session, user_id, food_id):
        query = session.query(cls).filter(
            cls.user_id == user_id).filter(
            cls.food_id == food_id).filter(
            cls.has_ordered == 0).order_by(
            cls.created_at)
        return query.scalar()

    @hybrid_method
    def get_all_by_user(cls, session, user_id, offset=None, limit=None):
        query = session.query(cls).filter(
            cls.user_id == user_id).filter(
            cls.has_ordered == 0).order_by(
            cls.created_at)
        if offset: 
            query = query.offset(offset)
        if limit:
            query = query.limit(limit)
        return query.all()

if __name__ == "__main__":
    pass
