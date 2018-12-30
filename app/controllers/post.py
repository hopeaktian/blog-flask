#!/usr/bin/env python
#coding:utf-8
"""
file:.py
date:2018/12/2 13:41
author:    peak
description:
"""
from flask import Flask, Blueprint, render_template, request, flash, session, redirect, url_for, g
import datetime, os
from app.models import db, User, Comment, Post, Tag, tags
from app.markdown_html import switch_html
from werkzeug.utils import secure_filename
from sqlalchemy import not_
from app.sm import mail_admin

post = Blueprint(
    'post',
    __name__
)

@post.route('/post/<int:year>/<int:month>/<int:id>', methods=['GET', 'POST'])
def postdetails(year,month,id):
    lenth = 0
    comments = Comment.query.filter(Comment.Post_Id == id).order_by(Comment.Id.desc()).all()
    lenth = len(comments)


    content = ""
    posts = Post.query.filter(Post.User_Id == 1, Post.Id == id).first()
    post_file = posts.Content_Name
    basepath = os.path.abspath(os.path.dirname(__file__))       # 当前文件所在目录
    parentdir = os.path.dirname(basepath)                       # 父级目录
    if post_file != None:
        post_file_url = os.path.join(parentdir, 'static/Upload_Files/markdown', secure_filename(post_file))
        content = switch_html(post_file_url)



    if request.method == "POST":
        # 判断称呼是否合法
        if request.form.get("nickname") == u"落风" and g.current_user_name != u"落风":
            flash(u"评论的称呼已被博主使用了哦，换个称呼重试吧！ -_-||", category="warning")
            return render_template('Post_Details.html', posts=posts, content=content, lenth=lenth, comments=comments, title=posts.Title)

        commentforsql = Comment()
        commentforsql.Name = request.form.get("nickname")
        commentforsql.Email = request.form.get("email")
        commentforsql.text = request.form.get("leavemessage")
        commentforsql.Post_Id = id



        db.session.add(commentforsql)
        db.session.commit()

        comments = Comment.query.filter(Comment.Post_Id == id).order_by(Comment.Id.desc()).all()
        lenth = len(comments)
        return render_template('Post_Details.html', posts=posts, content=content, lenth=lenth, comments=comments, title=posts.Title)

    return render_template('Post_Details.html', posts=posts, content=content, lenth=lenth, comments=comments, title=posts.Title)

@post.route('/tag/<int:tagid>', methods=['GET', 'POST'])
def tag(tagid):
    if request.method == 'POST':
        page = request.form.get('page')
        page = int(page)
        TAG = Tag.query.filter(Tag.Id == tagid).first()
        SecretTag = Tag.query.filter(Tag.Title == "私密").first()
        POST = TAG.posts
        pagination = POST.filter(not_(Post.tags.contains(SecretTag))).order_by(Post.Id.desc()).paginate(page, per_page=6, error_out=False)
        print len(pagination.items)
        user_Post = pagination.items
        lenth = len(user_Post)
        tem = []
        for x in user_Post:
            tem.append(x.to_json())
        print jsonify(tem)
        return jsonify(objects = tem)

    if request.method == 'GET':
        page = request.form.get('page', 1)
        page = int(page)
        TAG = Tag.query.filter(Tag.Id == tagid).first()
        SecretTag = Tag.query.filter(Tag.Title == "私密").first()
        POST = TAG.posts
        pagination = POST.filter(not_(Post.tags.contains(SecretTag))).order_by(Post.Id.desc()).paginate(page, per_page=6, error_out=False)
        user_Post = pagination.items
        lenth = len(user_Post)
        return render_template('tag_details.html', user_Post=user_Post, lenth=lenth, pagination=pagination, title=TAG.Title)

@post.route('/addurl', methods=['GET', 'POST'])
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