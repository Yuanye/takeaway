# -*- coding: utf-8 -*- 
"""
    It's a pipeline or middleware?
"""
def has_used_mark(content):
    _content = content.split(" ")
    _has_mark = [w for w in _content if w.lower() == "mark"]
    if _has_mark:
        return True
    return False



if __name__ == "__main__":
    pass

