# _*_ coding:utf-8 _*_
__author__ = 'Ando'
__date__ = '8/2/2017 11:56 PM'

from flask import Flask
from _datetime import datetime
from app import  db

# 会员
class User(db.Model):
    __tablename__ = "user"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 名称
    pwd = db.Column(db.String(100), )  # 密码
    email = db.Column(db.String(100), unique=True)  # 邮箱
    phone = db.Column(db.String(11), unique=True)  # 手机号
    intro = db.Column(db.Text)  # 简介
    portrait = db.Column(db.String(255), unique=True)  # 头像
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 增加时间
    uuid = db.Column(db.String(255), unique=True)  # 唯一标识
    userlog = db.relationship('UserLog', backref='user')  # 会员日志外键关系之关联
    comments = db.relationship('Comment', backref='user')  # 评论外键关系之关联
    enshrine = db.relationship('Enshrine', backref='user')  # 收藏外键关系之关联

    def __repr__(self):
        return "<User %r>" % self.name


# 会员登录日志
class UserLog(db.Model):
    __tablename__ = "userlog"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)  # 编号
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属会员
    ip = db.Column(db.String(100))  # ip
    logintime = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 登录时间

    def __repr__(self):
        return "<UserLog %r>" % self.id


# 标签
class Tag(db.Model):
    __tablename__ = "tag"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 名称
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 增加时间
    movie = db.relationship("Movie", backref='tag')

    def __repr__(self):
        return "<Tag %r>" % self.id


# 电影
class Movie(db.Model):
    __tablename__ = "movie"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 名称
    intro = db.Column(db.Text)  # 简介
    url = db.Column(db.String(255))  # 地址
    cover = db.Column(db.String(255), unique=True)  # 封面
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))  # 所属标签
    star = db.Column(db.BigInteger)  # 星级
    playnum = db.Column(db.BigInteger)  # 播放量
    commentnum = db.Column(db.BigInteger)  # 评论量
    area = db.Column(db.String(255))  # 地区
    realse_time = db.Column(db.Date)  # 上映时间
    mins = db.Column(db.String(100))  # 时长
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 增加时间
    comments = db.relationship('Comment', backref='movie')  # 评论外键关系之关联
    enshrine = db.relationship('Enshrine', backref='movie')  # 收藏外键关系之关联

    def __repr__(self):
        return "<Movie %r>" % self.name


# 预告
class Preview(db.Model):
    __tablename__ = "preview"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 名称
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 增加时间

    def __repr__(self):
        return "<Preview %r>" % self.name


# 评论
class Comment(db.Model):
    __tablename__ = "comment"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)  # 编号
    content = db.Column(db.Text)  # 评论
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 用户ID
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))  # 电影ID
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 增加时间

    def __repr__(self):
        return "<Comment %r>" % self.id


# 电影之收藏
class Enshrine(db.Model):
    __tablename__ = "enshrine"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)  # 编号
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 用户ID
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))  # 电影ID
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 增加时间

    def __repr__(self):
        return "<Enshrine %r>" % self.id


# 权限
class Auth(db.Model):
    __tablename__ = "auth"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 名称
    url = db.Column(db.String(255), unique=True)  # 地址
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 增加时间

    def __repr__(self):
        return "<Auth %r>" % self.id


# 角色
class Role(db.Model):
    __tablename__ = "role"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 名称
    auths = db.Column(db.String(800))  # 权限
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 增加时间
    admin = db.relationship("Admin", backref='role')  # 管理员外键

    def __repr__(self):
        return "<Role %r>" % self.id


# 管理员
class Admin(db.Model):
    __tablename__ = "admin"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 名称
    pwd = db.Column(db.String(100), )  # 密码
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))  # 所属角色
    is_super = db.Column(db.SmallInteger)  # 是否是超级管理员
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 增加时间
    # adminlog = db.relationship(db.ForeignKey('AdminLog', backref='admin'))  #管理员日志
    # operlog = db.relationship(db.ForeignKey('OperLog', backref='admin'))  #操作日志
    adminlogs = db.relationship("AdminLog", backref='admin')  # 管理员登录日志外键关系关联
    oplogs = db.relationship("OperLog", backref='admin')  # 管理员操作日志外键关系关联

    def __repr__(self):
        return "<Admin %r>" % self.id

    def check_pwd(self, pwd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd, pwd)


# 管理员登录日志
class AdminLog(db.Model):
    __tablename__ = "adminlog"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)  # 编号
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属管理员
    ip = db.Column(db.String(100))  # 登录IP
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 增加时间

    def __repr__(self):
        return "<AdminLog %r>" % self.id


# 操作日志
class OperLog(db.Model):
    __tablename__ = "OperLog"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)  # 编号
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属管理员
    ip = db.Column(db.String(100))  # IP
    reason = db.Column(db.String(600))  # 原因
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 增加时间

    def __repr__(self):
        return "<OperLog %r>" % self.id


if __name__ == "__main__":
    db.create_all()



#生成管理员密码
# from werkzeug.security import generate_password_hash
# admin = Admin(
#    name="dushao",
#    pwd=generate_password_hash("dushao")
# )
# db.session.add(admin)
# db.session.commit()