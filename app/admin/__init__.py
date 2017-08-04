# _*_ coding:utf-8 _*_
__author__ = 'Ando'
__date__ = '8/2/2017 11:58 PM'

from flask import Blueprint

admin = Blueprint("admin", __name__)
import app.admin.views
