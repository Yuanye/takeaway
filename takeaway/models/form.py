# -*- coding: utf-8 -*- 
from __future__ import absolute_import, division, print_function, with_statement

from takeaway.libs.form import (
    Form, 
    TextField, 
    PasswordField, 
    SubmitField, 
    TextAreaField, 
    BooleanField, 
    HiddenField, 
    ValidationError,  
    required, 
    regexp, 
    equal_to, 
    email, 
    optional, 
    url
)

USERNAME_RE = r'^[\w.+-]+$'
is_username = regexp(USERNAME_RE, 
                    message="You can only use letters, numbers or dashes")

class FormError(Exception):
    pass

class LoginForm(Form):
    name = TextField("User", validators=[required("You must provide an Username")])
    password = PasswordField("Password")
    #next = HiddenField()
    submit = SubmitField("Login")

class SignupForm(Form):
    password = PasswordField("Password", validators=[required("Password required")])
    name = TextField("Name", validators=[required(message="Username required")])
    phone_num = TextField("PhoneNum", validators=[required(message="Phone Number required")])
    next = HiddenField()
    submit = SubmitField("signup")

class FoodForm(Form):
    category_id = TextField("CategoryId", validators=[required(message="Category required")])
    name = TextField("Name", validators=[required(message="Name required")])
    price = TextField("Price", validators=[required(message="Price required")])
    cover = TextField("Cover", validators=[required(message="Cover required")])
    next = HiddenField()
    submit = SubmitField("Save")

class CategoryForm(Form):
    
    name = TextAreaField("Name", validators=[required(message="name required")])
    submit = SubmitField("Add category")
    cancel = SubmitField("Cancel")

class CartForm(Form):
    food_id = TextField("FoodId", validators=[required(message="Food required")])
    amount = TextField("amount", validators=[required(message="amount required")])
    next = HiddenField()
    submit = SubmitField("Save")

class Order(Form):
    pass

if __name__ == "__main__":
    pass
