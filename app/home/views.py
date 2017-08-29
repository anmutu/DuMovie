from . import home
from flask import render_template, redirect, url_for, request, session, flash, Response
# 实体
from app.models import User, UserLog
# 表单
from app.home.forms import RegistForm, LoginForm
# 数据库
from app import db
# 密码判断使用
from werkzeug.security import generate_password_hash
import uuid

# _*_ coding:utf-8 _*_
__author__ = 'Ando'
__date__ = '8/15/2017 10:52 PM'

# _*_ coding:utf-8 _*_
__author__ = 'Ando'
__date__ = '8/2/2017 11:58 PM'


# 会员注册
@home.route("/register/", methods=["GET", "POST"])
def register():
    form = RegistForm()
    if form.validate_on_submit():
        data = form.data
        user = User(
            name=data["name"],
            email=data["email"],
            phone=data["phone"],
            pwd=generate_password_hash(data["pwd"]),
            uuid=uuid.uuid4().hex
        )
        db.session.add(user)
        db.session.commit()
        flash("注册成功！", "ok")
    return render_template("home/register.html", form=form)


@home.route("/")
def index():
    # return "<h1>Home</h1>"
    return render_template("home/index.html")


# 登录
@home.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(name=data["name"]).first()
        if not user.check_pwd(data["pwd"]):
            flash("密码错误！", "err")
            return redirect(url_for("home.login"))
        session["user"] = user.name
        session["user_id"] = user.id
        userlog = UserLog(
            user_id=user.id,
            ip=request.remote_addr
        )
        db.session.add(userlog)
        db.session.commit()
        return redirect(url_for("home.user"))
    return render_template("home/login.html", form=form)


@home.route("/logout/")
def logout():
    session.pop("user", None)
    session.pop("user_id", None)
    return redirect(url_for("home.login"))


# 用户
@home.route("/user/")
def user():
    return render_template("home/user.html")


# 修改密码
@home.route("/pwd/")
def pwd():
    return render_template("home/pwd.html")


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


# 播放
@home.route("/play/")
def play():
    return render_template("home/play.html")


# 动画
@home.route("/animation/")
def animation():
    return render_template("home/animation.html")


@home.route("/search/")
def search():
    return render_template("home/search.html")
