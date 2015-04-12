# -*- coding: utf-8 -*- 

class RequirementException(Exception):
    pass

def require(val):
    if not val:
        raise RequirementException
    return val

if __name__ == "__main__":
    pass

