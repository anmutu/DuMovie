from app import db
from app.models import Admin
from werkzeug.security import generate_password_hash

# _*_ coding:utf-8 _*_
__author__ = 'Ando'
__date__ = '8/28/2017 10:25 PM'


admin = Admin(
    name="mutou",
    pwd=generate_password_hash("mutou")
)
db.session.add(admin)
db.session.commit()
