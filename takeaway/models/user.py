# -*- coding: utf-8 -*- 
from __future__ import absolute_import, division, print_function, with_statement

import os
from hashlib import sha1

from sqlalchemy import Column, func
from sqlalchemy.types import Integer, String, TIMESTAMP
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method

from .store import BaseModel
#from tide.libs.redis.decorator import cache
from .session import generate_token

class UserExists(Exception):
    pass

class UserNotExists(Exception):
    pass

class UserDAO(BaseModel):

    __tablename__ = 'user'
    id = Column(Integer, primary_key=True) 
    name = Column(String)
    password = Column(String)
    session_id = Column(String)
    phone_num = Column(String)
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
    def by_name(cls, session, name):
        uid = cls._by_name_cache(session, name)
        return cls.byID(session, uid)


    @hybrid_method
    def _by_name_cache(cls, session, name):
        uid = session.query(cls.id).filter(cls.name == name).scalar()
        if not uid:  
            raise UserNotExists
        return uid 

    @hybrid_method
    def by_session_id(cls, session, session_id):
        user = session.query(cls).filter(cls.session_id == session_id).scalar()
        if not user:  
            raise UserNotExists
        return user 

    @hybrid_method
    def generate_token(cls):
        return generate_token(32)

    @hybrid_method
    def login(self, session):
        self.session_id = self.generate_token()
        self.add(session)

    @hybrid_method
    def validate_password(self, password):
        """Check the password against existing credentials."""
        hashed_pass = sha1()
        hashed_pass.update(password + self.hashed_password[:40])
        return self.hashed_password[40:] == hashed_pass.hexdigest()

    @hybrid_property
    def hashed_password(self):
        return self.password

    @hashed_password.setter
    def _set_password(self, password):
        self.password = self.hash_password(password)

    @hybrid_method
    def hash_password(cls, password):
        """Hash password."""
        hashed_password = password

        if isinstance(password, unicode):
            password_8bit = password.encode('UTF-8')
        else:
            password_8bit = password

        salt = sha1()
        salt.update(os.urandom(60))
        hash = sha1()
        hash.update(password_8bit + salt.hexdigest())
        hashed_password = salt.hexdigest() + hash.hexdigest()

        if not isinstance(hashed_password, unicode):
            hashed_password = hashed_password.decode('UTF-8')

        return hashed_password
    
if __name__ == "__main__":
    pass

