# coding=utf-8
from werkzeug.security import generate_password_hash,check_password_hash
from flask.ext.login import UserMixin,AnonymousUserMixin
from flask import current_app
from .. import login_manager,db


class Permission:
    ADMINISTER = 0x01 
    NORMAL = 0x02


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy = 'dynamic')


    def __repr__(self):
        return '<Role %r> ' % self.name



    @staticmethod
    def insert_roles():
        roles = {
            'User':Permission.NORMAL,
            'Administrator':0xff
        }
        for r in roles:
            role = Role.query.filter_by(name = r).first()
            if role is None:
                role = Role(name = r)
            role.permissions = roles[r]
            db.session.add(role)
        db.session.commit()

class User(UserMixin,db.Model):
    print "into class User..............."
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    # 密码为128的hash值
    password_hash = db.Column(db.String(128))
    # 增加一列判断是否为管理员
    is_admin = db.Column(db.Boolean,default = False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))


    def __repr__(self):
        return '<User %r>' % self.username

    # password设置property使密码不可直接读，verify_password()判断密码是否正确。
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash, password)


    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.is_admin:
                self.role = Role.query.filter_by(name="Administrator").first()
            if self.role is None:
                self.role = Role.query.filter_by(name="User").first()

    # 用户权限验证
    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        print "is_admin starting...."
        return self.can(Permission.ADMINISTER)

class AnonymousUser(AnonymousUserMixin):
    def can(self,permissions):
        return False

    def is_administrator(self):
        return False


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

