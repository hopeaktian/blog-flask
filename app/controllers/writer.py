#!/usr/bin/env python
#coding:utf-8
"""
file:.py
date:2018/12/10 15:58
author:    peak
description:
"""

from flask import Flask, Blueprint, render_template, request, flash, session, redirect, url_for, g
import datetime, os
from app.models import db, User, Comment, Post, Tag, tags
from app.sm import mail_admin
from werkzeug.utils import secure_filename

writer = Blueprint(
    'writer',
    __name__
)

@writer.route('/writer/<int:uid>', methods=['GET', 'POST'])
def write(uid):
    if g.current_user == None:
        return render_template('error.html')
    elif g.current_user.Id != uid:
        return render_template('error.html')
    else:
        if request.method == 'POST':
            new_title = request.form.get("title")
            new_cover = request.files['cover']
            new_markdown = request.files['markdown']
            new_tag = request.form.get("tag")
            # 查询是否title重名
            if Post.query.filter(Post.Title == new_title and Post.User_Id == uid).first() is not None:
                flash(u"文章标题已经存在，换个标题吧！ -_-", category="warning")
                return render_template('writer.html')
            # 第一次提交数据库
            post_forsql = Post()
            post_forsql.Title = new_title
            post_forsql.User_Id = uid
            # 处理tag
            tag_list = new_tag.split()
            tag_object = []
            for i in tag_list:
                if Tag.query.filter(Tag.Title == i).first() is None:
                    # 若是新的tag首先创建新的tag
                    tag_forsql = Tag()
                    tag_forsql.Title = i
                    db.session.add(tag_forsql)
                    db.session.commit()
                tag_object.append(Tag.query.filter(Tag.Title == i).first())
            post_forsql.tags = tag_object
            db.session.add(post_forsql)
            db.session.commit()

            # 获取初始文件名
            new_cover_name = new_cover.filename
            new_cover_point = new_cover_name.rindex(".")
            new_markdown_name = new_markdown.filename
            new_markdown_point = new_markdown_name.rindex(".")

            # 查询ID并改文件名
            post_checksql = Post.query.filter(Post.Title == new_title and Post.User_Id == uid).first()
            pid = post_checksql.Id
            new_cover_name = str(pid) + new_cover_name[new_cover_point:]
            new_markdown_name = str(pid) + new_markdown_name[new_markdown_point:]

            # 保存文件
            basepath = os.path.abspath(os.path.dirname(__file__))       # 当前文件所在目录
            parentdir = os.path.dirname(basepath)                       # 父级目录
            upload_path = os.path.join(parentdir, 'static/Upload_Files/img', secure_filename(new_cover_name))
            new_cover.save(upload_path)
            upload_path = os.path.join(parentdir, 'static/Upload_Files/markdown', secure_filename(new_markdown_name))
            new_cover.save(upload_path)




            # 第二次提交数据库
            post_checksql.Cover_Picture_Name = new_cover_name
            post_checksql.Content_Name = new_markdown_name
            db.session.add(post_checksql)
            db.session.commit()

            flash(u"提交成功！ -_-", category="success")

        return render_template('writer.html')

@writer.route('/addurl', methods=['GET', 'POST'])
def addurl():
    if request.method == 'POST':
        urls = request.form.get("urls")
        emails = request.form.get("emails")
        leavemes = request.form.get("leavemessage")
        leavemes = leavemes.encode('utf-8')
        try:
            mail_admin(urls, emails, leavemes)
        except:
            flash(u"提交失败，请重试！ -_-||", category="warning")
            # return render_template('addurl.html')
        else:
            flash(u"提交成功啦，主人已经收到你的请求了哦！ ^_^", category="success")
            # return render_template('addurl.html')
    return render_template('addurl.html')

@writer.route('/login/', methods=['GET', 'POST'])
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
            return redirect('/')
        else:
            flash(u"登陆失败，请重试！ -_-||", category="warning")
    return render_template('login.html')

@writer.route("/logout", methods=['GET'])
def logout():
    session.pop('user_name', None)
    g.current_user = None
    return redirect('/')
