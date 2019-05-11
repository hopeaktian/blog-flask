#!/usr/bin/env python
#coding:utf-8
"""
file:.py
date:2018/12/30 12:45
author:    peak
description:
"""

from flask import Flask, Blueprint, render_template, request, flash, session, redirect, url_for, g
import datetime, os
from app.models import db, User, Comment, Post, Tag, tags

from werkzeug.utils import secure_filename

loginout = Blueprint(
    'loginout',
    __name__
)


@loginout.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        Name = request.form.get("name")
        Name = Name.encode("utf-8")
        Password = request.form.get("password")
        user = User.query.filter(User.Email == Name, User.Password == Password).first()
        if user:
            session['user_name'] = user.Name
            g.current_user = user
            flash(u"登陆成功啦！ ^_^", category="success")
            return redirect('/root')
        else:
            flash(u"登陆失败，请重试！ -_-||", category="warning")
    return render_template('login.html')

@loginout.route("/logout", methods=['GET'])
def logout():
    session.pop('user_name', None)
    g.current_user = None
    return redirect('/')