# _*_ coding:utf-8 _*_
__author__ = 'Ando'
__date__ = '8/2/2017 11:59 PM'

from . import admin
from flask import Flask, render_template, url_for, redirect


# 主页
@admin.route("/")
def index():
    return render_template("admin/index.html")


# 登录
@admin.route("/login/")
def login():
    return render_template("admin/login.html")


# 退出
@admin.route("/logout/")
def logout():
    return redirect(url_for("admin.login"))


# 密码
@admin.route("/pwd/")
def pwd():
    return render_template("admin/pwd.html")


# 增加标签
@admin.route("/tag_add/")
def tag_add():
    return render_template("admin/tag_add.html")


# 标签列表
@admin.route("/tag_list/")
def tag_list():
    return render_template("admin/tag_list.html")


# 添加电影
@admin.route("/movie_add/")
def movie_add():
    return render_template("admin/movie_add.html")


# 增加列表
@admin.route("/movie_list/")
def movie_list():
    return render_template("admin/movie_list.html")


# 添加预告
@admin.route("/preview_add/")
def preview_add():
    return render_template("admin/preview_add.html")


# 预告列表
@admin.route("/preview_list/")
def preview_list():
    return render_template("admin/preview_list.html")


# 用户列表
@admin.route("/user/list/")
def user_list():
    return render_template("admin/user_list.html")


# 用户详情
@admin.route("/user/detail/")
def user_detail():
    return render_template("admin/user_detail.html")


# 用户列表
@admin.route("/comment/list/")
def comment_list():
    return render_template("admin/comment_list.html")


# 收藏列表
@admin.route("/enshrine/list/")
def enshrine_list():
    return render_template("admin/enshrine_list.html")


# 操作日志列表
@admin.route("/operlog/list/")
def operlog_list():
    return render_template("admin/operlog_list.html")


# 增加角色
@admin.route("/role/add/")
def role_add():
    return render_template("admin/role_add.html")


# 角色列表
@admin.route("/role/list/")
def role_list():
    return render_template("admin/role_list.html")


# 管理员日志
@admin.route("/adminloginlog/list/")
def adminlgoinlog_list():
    return render_template("admin/adminloginlog_list.html")


# 增加权限
@admin.route("/auth/add/")
def auth_add():
    return render_template("admin/auth_add.html")


# 权限列表
@admin.route("/auth/list/")
def auth_list():
    return render_template("admin/auth_list.html")



# 增加管理员
@admin.route("/admin/add/")
def admin_add():
    return render_template("admin/admin_add.html")


# 管理员列表
@admin.route("/admin/list/")
def admin_list():
    return render_template("admin/admin_list.html")