#!/usr/bin/env python
#coding:utf-8
"""
file:.py
date:2018/12/1 12:07
author:    peak
description:
"""
from flask import Flask, redirect, url_for, render_template, session, g, jsonify, request
from config import DevConfig
from app.models import db, User, Comment, Post, Tag, tags, Access, Like
from controllers.post import post
from controllers.writer import writer
from controllers.loginout import loginout
from controllers.search import search
from controllers.guest_feedback import guest_feedback
from sqlalchemy import not_
import json

app = Flask(__name__)
app.config.from_object(DevConfig)

db.init_app(app)

@app.route('/', methods=['POST', 'GET'])
def index():
    secret = Tag.query.filter(Tag.Title == "私密").first()        # 查询私密tag对象
    index_tag = Tag.query.filter(Tag.Title != "私密").all()
    if request.method == 'POST':
        page = request.form.get('page')
        page = int(page)
        pagination = Post.query.filter(Post.User_Id == 1, not_(Post.tags.contains(secret))).order_by(Post.Id.desc()).paginate(page, per_page=6, error_out=False)
        user_Post = pagination.items
        lenth = len(user_Post)
        tem = []
        for x in user_Post:
            tem.append(x.to_json())
        print jsonify(tem)
        return jsonify(objects=tem)

    if request.method == 'GET':
        # 记录访问信息
        ip = request.remote_addr
        access_forsql = Access()
        access_forsql.Ip = ip
        db.session.add(access_forsql)
        db.session.commit()

        # 查询首页文章列表

        page = request.form.get('page', 1)
        page = int(page)
        pagination = Post.query.filter(Post.User_Id == 1, not_(Post.tags.contains(secret))).order_by(Post.Id.desc()).paginate(page, per_page=6, error_out=False)
        user_Post = pagination.items
        lenth = len(user_Post)

        # 站点信息
        website_info = {}                               # 创建空站点信息字典
        all_access = Access.query.count()               # 查询截至当前访问量
        articles_count = Post.query.count()             # 查询文章总量
        like_count = Like.query.filter(Like.Like_Type == 1).count()     # 查询点赞总数
        cancellike = Like.query.filter(Like.Like_Type == 0).count()
        like_count = like_count - cancellike
        website_info['all_access'] = all_access
        website_info['articles_count'] = articles_count
        website_info['like_count'] = like_count

        return render_template('index.html', user_Post=user_Post, lenth=lenth, pagination=pagination, website_info=website_info, index_tag=index_tag, title="TF'S BLOG")

@app.before_request
def check_user():
    if 'user_name' in session:
        g.current_user_name = session['user_name']
        user = User.query.filter(User.Name == session['user_name']).first()
        g.current_user = user

    else:
        g.current_user_name = json.dumps(None)
        g.current_user = None

app.register_blueprint(post)
app.register_blueprint(writer)
app.register_blueprint(loginout)
app.register_blueprint(search)
app.register_blueprint(guest_feedback)

if __name__ == '__main__':
    app.run(host='localhost', port=80)
