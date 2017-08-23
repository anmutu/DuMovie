from . import admin
from flask import Flask, render_template, url_for, redirect, flash, session, request
from app.admin.forms import LoginForm, TagForm
from app.models import Admin, Tag
# 登录装饰器用的到
from functools import wraps
from app import db, app

# _*_ coding:utf-8 _*_
__author__ = 'Ando'
__date__ = '8/2/2017 11:59 PM'


# 登录装饰器
def admin_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin" not in session:
            return redirect(url_for("admin.login", next=request.url))
        return f(*args, **kwargs)

    return decorated_function


# 主页
@admin.route("/")
@admin_login_req
def index():
    return render_template("admin/index.html")


# 登录
@admin.route("/login/", methods=["GET", "POST"])
# @admin_login_req   login没有装饰器，不然会导致重定向，访问不了
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        admin = Admin.query.filter_by(name=data["account"]).first()
        if not admin.check_pwd(data["pwd"]):
            flash("密码错误！", 'err')
            return redirect(url_for("admin.login"))
        session["admin"] = data["account"]
        return redirect(request.args.get("next") or url_for("admin.index"))
    return render_template("admin/login.html", form=form)


# 退出
@admin.route("/logout/")
@admin_login_req
def logout():
    session.pop("admin", None)
    return redirect(url_for("admin.login"))


# 密码
@admin.route("/pwd/")
def pwd():
    return render_template("admin/pwd.html")


# 增加标签
@admin.route("/tag_add/", methods=["GET", "POST"])
def tag_add():
    form = TagForm()
    if form.validate_on_submit():
        data = form.data
        tag = Tag.query.filter_by(name=data["name"]).count()
        if tag == 1:
            flash("名称已经存在！", "err")
            return redirect(url_for('admin.tag_add'))
        tag = Tag(
            name=data["name"]
        )
        db.session.add(tag)
        db.session.commit()
        flash("添加标签成功！", "ok")
        redirect(url_for('admin.tag_add'))
    return render_template("admin/tag_add.html", form=form)


# 编辑标签
@admin.route("/tag/edit/<int:id>/", methods=["GET", "POST"])
@admin_login_req
def tag_edit(id=None):
    form = TagForm()
    tag = Tag.query.get_or_404(id)
    if form.validate_on_submit():
        data = form.data
        tag_count = Tag.query.filter_by(name=data["name"]).count()
        if tag.name != data["name"] and tag_count == 1:
            flash("名称已经存在！", "err")
            return redirect(url_for('admin.tag_edit', id=id))
        tag.name = data["name"]
        db.session.add(tag)
        db.session.commit()
        flash("修改标签成功！", "ok")
        redirect(url_for('admin.tag_edit', id=id))
    return render_template("admin/tag_edit.html", form=form, tag=tag)


# 标签列表
@admin.route("/tag/list/<int:page>/", methods=["GET"])
def tag_list(page=None):
    if page is None:
        page = 1
    page_data = Tag.query.order_by(
        Tag.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/tag_list.html", page_data=page_data)


# 标签删除
@admin.route("/tag/del/<int:id>/", methods=["GET"])
@admin_login_req
def tag_del(id=None):
    tag = Tag.query.filter_by(id=id).first_or_404()
    db.session.delete(tag)
    db.session.commit()
    flash("删除标签成功！", "ok")
    return redirect(url_for('admin.tag_list', page=1))  # 添加电影


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


# 角色修改
@admin.route("/role/edit/")
def role_edit():
    return render_template("admin/role_edit.html")



# 角色删除
@admin.route("/role/del/")
def role_del():
    return render_template("admin/role_del.html")


# 管理员日志
@admin.route("/adminloginlog/list/")
def adminloginlog_list():
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
