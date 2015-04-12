# -*- coding: utf-8 -*- 
from __future__ import absolute_import, division, print_function, with_statement

import datetime

from sqlalchemy import Column, func
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.types import Integer, String, TIMESTAMP


from .store import BaseModel

class CategoryNotExists(Exception):
    pass

class CategoryDAO(BaseModel):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True) 
    name = Column(String)
    created_at = Column(TIMESTAMP(timezone=False), nullable=False, server_default=func.current_timestamp())

    @hybrid_method
    def add(self, session): 
        try:
            self._commit(session, self)
            return self 
        except Exception as e:
            session.rollback()
            raise e


if __name__ == "__main__":
    pass
