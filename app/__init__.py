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
from app.models import db, User, Comment, Post, Tag, tags
from controllers.post import post

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
        page = request.form.get('page', 1)
        page = int(page)
        pagination = Post.query.filter(Post.User_Id == 1).order_by(Post.Id.desc()).paginate(page, per_page=6, error_out=False)
        user_Post = pagination.items
        lenth = len(user_Post)
        return render_template('index.html', user_Post=user_Post, lenth=lenth, pagination=pagination, title="TF'S BLOG")


app.register_blueprint(post)

if __name__ == '__main__':
    app.run(host='localhost', port=80)
