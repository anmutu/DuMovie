from . import admin
from flask import Flask, render_template, url_for, redirect, flash, session, request
from app.admin.forms import LoginForm, TagForm, MovieForm
from app.models import Admin, Tag, Movie, User, Comment
# 登录装饰器用的到
from functools import wraps
from app import db, app
# 上传文件,用到的四个引用
from werkzeug.utils import secure_filename
import os
import uuid
import datetime

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


# 修改文件名称,电影模块用的到。
def change_filename(filename):
    fileintro = os.path.splitext(filename)
    filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + str(uuid.uuid4().hex) + fileintro[-1]
    return filename


# 添加电影
@admin.route("/movie/add/", methods=["GET", "POST"])
@admin_login_req
def movie_add():
    form = MovieForm()
    # 实时拉取出标签
    form.tag_id.choices = [(v.id, v.name) for v in Tag.query.all()]
    if form.validate_on_submit():
        data = form.data
        file_url = secure_filename(form.url.data.filename)
        file_cover = secure_filename(form.cover.data.filename)
        if not os.path.exists(app.config["UP_DIR"]):
            os.makedirs(app.config["UP_DIR"])
            os.chmod(app.config["UP_DIR"], "rw")
        url = change_filename(file_url)
        cover = change_filename(file_cover)
        form.url.data.save(app.config["UP_DIR"] + url)
        form.cover.data.save(app.config["UP_DIR"] + cover)
        movie = Movie(
            name=data["name"],
            url=url,
            intro=data["intro"],
            cover=cover,
            star=int(data["star"]),
            playnum=0,
            commentnum=0,
            tag_id=int(data["tag_id"]),
            area=data["area"],
            release_time=data["release_time"],
            mins=data["mins"]
        )
        db.session.add(movie)
        db.session.commit()
        flash("添加电影成功！", "ok")
        return redirect(url_for('admin.movie_add'))
    return render_template("admin/movie_add.html", form=form)


# 电影列表
@admin.route("/movie/list/<int:page>/", methods=["GET"])
@admin_login_req
def movie_list(page=None):
    if page is None:
        page = 1
    page_data = Movie.query.join(Tag).filter(
        Tag.id == Movie.tag_id
    ).order_by(
        Movie.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/movie_list.html", page_data=page_data)


# 编辑电影
@admin.route("/movie/edit/<int:id>/", methods=["GET", "POST"])
@admin_login_req
# @admin_auth
def movie_edit(id=None):
    form = MovieForm()
    form.url.validators = []
    form.cover.validators = []
    movie = Movie.query.get_or_404(int(id))
    if request.method == "GET":
        form.intro.data = movie.intro
        form.tag_id.data = movie.tag_id
        form.star.data = movie.star
    if form.validate_on_submit():
        data = form.data
        movie_count = Movie.query.filter_by(name=data["name"]).count()
        if movie_count == 1 and movie.name != data["name"]:
            flash("片名已经存在！", "err")
            return redirect(url_for('admin.movie_edit', id=id))

        if not os.path.exists(app.config["UP_DIR"]):
            os.makedirs(app.config["UP_DIR"])
            os.chmod(app.config["UP_DIR"], "rw")

        if form.url.data.filename != "":
            file_url = secure_filename(form.url.data.filename)
            movie.url = change_filename(file_url)
            form.url.data.save(app.config["UP_DIR"] + movie.url)

        if form.cover.data.filename != "":
            file_cover = secure_filename(form.cover.data.filename)
            movie.cover = change_filename(file_cover)
            form.cover.data.save(app.config["UP_DIR"] + movie.cover)

        movie.star = data["star"]
        movie.tag_id = data["tag_id"]
        movie.intro = data["intro"]
        movie.name = data["name"]
        movie.area = data["area"]
        movie.mins = data["mins"]
        movie.release_time = data["release_time"]
        db.session.add(movie)
        db.session.commit()
        flash("修改电影成功！", "ok")
        return redirect(url_for('admin.movie_edit', id=id))
    return render_template("admin/movie_edit.html", form=form, movie=movie)


# 删除电影
@admin.route("/movie/del/<int:id>/", methods=["GET"])
@admin_login_req
def movie_del(id=None):
    movie = Movie.query.get_or_404(int(id))
    db.session.delete(movie)
    db.session.commit()
    flash("成功删除电影！", "ok")
    return redirect(url_for('admin.movie_list', page=1))


# 添加预告
@admin.route("/preview_add/")
def preview_add():
    return render_template("admin/preview_add.html")


# 预告列表
@admin.route("/preview_list/")
def preview_list():
    return render_template("admin/preview_list.html")


# 会员列表
# @admin.route("/user/list/< int:page >/", methods=["GET"])
@admin.route("/user/list/<int:page>/", methods=["GET"])
@admin_login_req
def user_list(page=None):
    if page is None:
        page = 1
    page_data = User.query.order_by(
        User.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/user_list.html", page_data=page_data)


# 删除会员
@admin.route("/user/del/<int:id>/", methods=["GET"])
@admin_login_req
def user_del(id=None):
    user = User.query.get_or_404(int(id))
    db.session.delete(user)
    db.session.commit()
    flash("删除会员成功！", "ok")
    return redirect(url_for('admin.user_list', page=1))


# 用户详情
@admin.route("/user/detail/")
@admin.route("/user/view/<int:id>/", methods=["GET"])
def user_detail(id=None):
    user = User.query.get_or_404(int(id))
    return render_template("admin/user_detail.html", user=user)


# 评论列表
@admin.route("/comment/list/<int:page>/", methods=["GET"])
@admin_login_req
# @admin_auth
def comment_list(page=None):
    if page is None:
        page = 1
    page_data = Comment.query.join(
        Movie
    ).join(
        User
    ).filter(
        Movie.id == Comment.movie_id,
        User.id == Comment.user_id
    ).order_by(
        Comment.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/comment_list.html", page_data=page_data)


# 删除评论
@admin.route("/comment/del/<int:id>/", methods=["GET"])
@admin_login_req
def comment_del(id=None):
    comment = Comment.query.get_or_404(int(id))
    db.session.delete(comment)
    db.session.commit()
    flash("删除评论成功！", "ok")
    return redirect(url_for('admin.comment_list', page=1))



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
