import sys, os
sys.path.append('../')
from back_system.api.login_api import *
from flask_login import UserMixin


class UserContext(UserMixin):
    def __init__(self, id, data=None):
        self.id = id
        self.data = data


class LoginModel:

    def on_login(self, password):
        return Login_API().on_login(password)

    def get_context(self, password):
        return Login_API().get_context(password)
