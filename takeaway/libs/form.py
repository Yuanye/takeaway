# -*- coding: utf-8 -*- 
import re

from tornado import escape
from wtforms import form
from wtforms.compat import text_type

from wtforms.fields import (
    BooleanField,
    DecimalField, 
    DateField, 
    DateTimeField,
    FieldList, 
    FloatField, 
    FormField, 
    HiddenField, 
    IntegerField, 
    PasswordField, 
    RadioField, 
    SelectField, 
    SelectMultipleField, 
    SubmitField, 
    TextField, 
    TextAreaField
)

from wtforms.validators import (
    ValidationError, 
    Email, 
    email, 
    EqualTo, 
    equal_to, 
    IPAddress, 
    ip_address, 
    Length, 
    length, 
    NumberRange, 
    number_range, 
    Optional, 
    optional, 
    Required, 
    required, 
    Regexp, 
    regexp, 
    URL, 
    url, 
    AnyOf, 
    any_of, 
    NoneOf, 
    none_of
)

from wtforms.widgets import (
    CheckboxInput, 
    FileInput, 
    HiddenInput, 
    ListWidget, 
    PasswordInput, 
    RadioInput, 
    Select, 
    SubmitInput, 
    TableWidget, 
    TextArea, 
    TextInput
)

class TornadoInputWrapper(object):

    def __init__(self, multidict):
        self._wrapped = multidict

    def __iter__(self):
        return iter(self._wrapped)

    def __len__(self):
        return len(self._wrapped)

    def __contains__(self, name):
        return (name in self._wrapped)

    def __getitem__(self, name):
        return self._wrapped[name]

    def __getattr__(self, name):
        return self.__getitem__(name)

    def getlist(self, name):
        try:
            values = []
            for value in self._wrapped[name]:
                value = escape.to_unicode(value)
                if isinstance(value, text_type):
                    value = re.sub(r'[\x00-\x08\x0e-\x1f]', ' ', value)
                values.append(value)
            return values
        except KeyError:
            return []

class Form(form.Form):

    def __init__(self, formdata=None, *args, **kwargs):
        self.obj = kwargs.get('obj', None)
        super(Form, self).__init__(formdata, formdata, *args, **kwargs)

    def process(self, formdata=None, *args, **kwargs):
        if formdata is not None and not hasattr(formdata, 'getlist'):
            formdata = TornadoInputWrapper(formdata)
        super(Form, self).process(formdata, *args, **kwargs)

if __name__ == "__main__":
    pass

