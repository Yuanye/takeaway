# -*- coding: utf-8 -*- 

class Counter(object):
    """ Counter
        e.g: PV counter
     """

    def __init__(self, redis, name=None):
        self.redis = redis
        self.name = name

    def _byID(self, key):
        if not self.name:
            return self.redis.get(key)
        return self.redis.hget(self.name, key)

    def _incr(self, key, value=1):
        if not self.name:
            return self.redis.incrby(key, value)
        return self.redis.hincrby(self.name, key, value)

    def _decr(self, key, value):
        if not self.name:
            return self.redis.decrby(key, value)
        return self.redis.hincrby(self.name, key, -value)

class SetCounter(object):
    """ Set Counter
        e.g: UV counter
    """

    def __init__(self, redis, name):
        self.redis = redis
        self.name = name

    def add(self, key, value):
        return self.redis.sadd("{0}:{1}".format(self.name, key), value)

    def count(self, key):
        return self.redis.scard("{0}:{1}".format(self.name, key))

    def delete(self, key, value):
        return self.redis.srem("{0}:{1}".format(self.name, key), value)



if __name__ == "__main__":
    pass

