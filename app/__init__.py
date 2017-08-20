# _*_ coding:utf-8 _*_
__author__ = 'Ando'
__date__ = '8/2/2017 11:56 PM'

from flask_sqlalchemy import SQLAlchemy
from flask import Flask,render_template

app = Flask(__name__)
app.debug = True
from app.home import home as home_blueprint
from app.admin import admin as admin_blueprint
import pymysql

# app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:sfg18110@127.0.0.1:3306/dumovie"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)


app.register_blueprint(home_blueprint)
app.register_blueprint(admin_blueprint, url_prefix="/admin")


# 404页面
@app.errorhandler(404)
def page_not_found(error):
    return render_template("home/404.html"), 404

