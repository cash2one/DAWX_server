#coding=utf-8
from flask import render_template,redirect,request,url_for,flash
from flask.ext.login import login_required, login_user,logout_user
from . import auth
from .forms import LoginForm
from ..models import User,Permission
from ..decorators import admin_required,permission_required

@auth.route('/login.dawx', methods=['GET',"POST"])
@auth.route('/auth/login.dawx',  methods=['GET',"POST"])
@auth.route('/auth',  methods=['GET',"POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        print user
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash(u'登录成功')
            return redirect(request.args.get('next') or url_for('main.index'))
        flash(u'密码错误')

    return render_template('auth/login.html', form=form)

@auth.route('/secret')
@login_required
def secret():
    return "Only authenticated users are allowed!!"



@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return "you are logout!!!"

@auth.route('/test')
@login_required
@admin_required
def for_admins_only():
    return "admin_required"

