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
from app.models import db, User, Comment, Post, Tag, tags, Access
from controllers.post import post
from controllers.writer import writer

app = Flask(__name__)
app.config.from_object(DevConfig)

db.init_app(app)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        page = request.form.get('page')
        page = int(page)
        pagination = Post.query.filter(Post.User_Id == 1).order_by(Post.Id.desc()).paginate(page, per_page=6, error_out=False)
        user_Post = pagination.items
        lenth = len(user_Post)
        tem = []
        for x in user_Post:
            tem.append(x.to_json())
        print jsonify(tem)
        return jsonify(objects = tem)

    if request.method == 'GET':
        # 记录访问信息
        ip = request.remote_addr
        access_forsql = Access()
        access_forsql.Ip = ip
        db.session.add(access_forsql)
        db.session.commit()

        # 查询截至当前访问量
        all_access = len(Access.query.all())

        page = request.form.get('page', 1)
        page = int(page)
        pagination = Post.query.filter(Post.User_Id == 1).order_by(Post.Id.desc()).paginate(page, per_page=6, error_out=False)
        user_Post = pagination.items
        lenth = len(user_Post)
        return render_template('index.html', user_Post=user_Post, lenth=lenth, pagination=pagination, all_access=all_access, title="TF'S BLOG")


app.register_blueprint(post)
app.register_blueprint(writer)

if __name__ == '__main__':
    app.run(host='192.168.3.5', port=80)
