# -*- coding: utf-8 -*- 
from __future__ import absolute_import, division, print_function, with_statement

from base64 import urlsafe_b64encode
from os import urandom

#from tide.models.store import redis

def generate_token(size):
    return urlsafe_b64encode(urandom(size)).rstrip("=")

if __name__ == "__main__":
    print(generate_token(32))
    pass
