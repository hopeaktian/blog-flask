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

from werkzeug.utils import secure_filename

writer = Blueprint(
    'writer',
    __name__
)

@writer.before_request
def checklogin():
    if g.current_user == None:
        return redirect('/login')



@writer.route('/root', methods=['GET', 'POST'])
def root():
    return render_template('root.html')



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
            if request.files.has_key("music"):
                new_music = request.files['music']
            else:
                new_music = None
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


            # 获取目录
            basepath = os.path.abspath(os.path.dirname(__file__))       # 当前文件所在目录
            parentdir = os.path.dirname(basepath)                       # 父级目录
            #  新建目录
            datetimes = post_checksql.Publish_Date
            now = str(datetimes.year)+"-"+str(datetimes.month)+"-"+str(datetimes.day)
            newdirname = now + "_" + post_checksql.Title
            new_dirpath = os.path.join(parentdir, 'static/Upload_Files/article', newdirname)
            os.mkdir(new_dirpath)
            # 保存封面图
            upload_path1 = os.path.join(parentdir, 'static/Upload_Files/article', newdirname, secure_filename(new_cover_name))
            new_cover.save(upload_path1)
            # 保存markdown文件
            upload_path2 = os.path.join(parentdir, 'static/Upload_Files/article', newdirname, secure_filename(new_markdown_name))
            new_markdown.save(upload_path2)
            # 保存音乐
            if new_music is not None:
                upload_path3 = os.path.join(parentdir, 'static/Upload_Files/article', newdirname, secure_filename(new_music.filename))
                new_markdown.save(upload_path3)




            # 第二次提交数据库
            post_checksql.Cover_Picture_Name = new_cover_name
            post_checksql.Content_Name = new_markdown_name
            post_checksql.Dir_Name = newdirname
            if new_music is not None:
                post_checksql.Music_Name = new_music.filename
            db.session.add(post_checksql)
            db.session.commit()

            flash(u"提交成功！ -_-", category="success")

        return render_template('writer.html')

