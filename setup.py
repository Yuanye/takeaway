import os
from setuptools import setup, find_packages

# package met info
NAME = "TakeAway"
VSESION = "0.0.1"
DESCRIPTION = "Have a takeaway"
AUTHOR = "Yuanye Ge"
URL = "https://github.com/Yuanye/have-a"
KEYWORDS = ""
CLASSIFIERS = []


commands= {} 

ENTRY_POINTS = """
"""

# dependencies
requires = [
    "gunicorn",
    "gevent",
    "mako",
    "msgpack-python",
    "MySQL-python",
    "qiniu",
    "redis",
    "requests",
    "SQLAlchemy",
    "tornado",
    "WTForms",
]

setup(
    name='takeaway',
    version=VSESION,
    description=DESCRIPTION,
    author=AUTHOR,
    url = URL,
    packages=find_packages(),
    install_package_data=True,
    commands=commands,
    zip_safe=False,
    install_requires=requires,
    entry_points=ENTRY_POINTS,
)

