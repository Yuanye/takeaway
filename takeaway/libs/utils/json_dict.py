# -*- coding: utf-8 -*- 
from datetime import datetime

class JsonDict(dict):
    """
        class B(JsonDict):
            def __init__(self, foo="foo"):
                self.foo = foo
        class C(JsonDict):
            def __init__(self, bar="bar"):
                self.bar = bar
            @property
            def d(self):
                return B()
        c = C()
        print type(c.d) # <class '__main__.B'>
        m = c.to_dict() 
        print m # {'bar': 'bar', 'name': {'foo': 'foo'}}
        print m.d # {'foo': 'foo'}
        print type(m.d) # <class '__main__.B'>
        print type(c.d) # <class '__main__.B'>
    """
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        self[name] = value


    def to_dict(self):
        #_dict = copy.deepcopy(self)
        for name in dir(self):
            if not name.startswith('_'):
                value = self.__getattribute__(name)
                if isinstance(value, datetime):
                    self.name =  str(value)
                elif isinstance(value, JsonDict):
                    self.name = value.to_dict()
                #else:
                #    print type(value)
        return self

if __name__ == "__main__":
    pass

