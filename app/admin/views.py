# _*_ coding:utf-8 _*_
__author__ = 'Ando'
__date__ = '8/2/2017 11:59 PM'

from . import admin


@admin.route("/")
def index():
    return "<h1>Admin</h1>"
