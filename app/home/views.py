# _*_ coding:utf-8 _*_
__author__ = 'Ando'
__date__ = '8/2/2017 11:58 PM'

from . import home


@home.route("/")
def index():
    return "<h1>Home</h1>"
