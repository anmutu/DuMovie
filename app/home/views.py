# _*_ coding:utf-8 _*_
__author__ = 'Ando'
__date__ = '8/2/2017 11:58 PM'

from . import home
from flask import render_template, redirect, url_for


@home.route("/")
def index():
    # return "<h1>Home</h1>"
    return render_template("home/index.html")


# 登录
@home.route("/login/")
def logout():
    return render_template("home/login.html")


# 退出
@home.route("/logout/")
def login():
    return redirect(url_for("home.login"))


# 注册
@home.route("/register/")
def register():
    return render_template("home/register.html")


# # 首页
# @home.route("/index/")
# def index():
#     return render_template("home/index.html")


# 动画
@home.route("/animation/")
def animation():
    return render_template("home/animation.html")


# 评论纪录
@home.route("/comments/")
def comments():
    return render_template("home/comments.html")



# 电影收藏
@home.route("/enshrine/")
def enshrine():
    return render_template("home/enshrine.html")


# 登录日志
@home.route("/loginlog/")
def loginlog():
    return render_template("home/loginlog.html")



# 搜索页面
@home.route("/search/")
def search():
    return render_template("home/search.html")

# 登录日志
@home.route("/user/")
def user():
    return render_template("home/user.html")



# 修改密码
@home.route("/pwd/")
def pwd():
    return render_template("home/pwd.html")



# 修改密码
@home.route("/play/")
def play():
    return render_template("home/play.html")




