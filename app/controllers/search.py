#!/usr/bin/env python
#coding:utf-8
"""
file:.py
date:2018/12/30 12:45
author:    peak
description:
"""

from flask import Blueprint, render_template, request, jsonify
from app.models import Post

search = Blueprint(
    'search',
    __name__
)


@search.route('/search/', methods=['GET', 'POST'])
def search_post():
    if request.method == 'POST':
        page = request.form.get('page')
        keyword = request.form.get('keyword')
        page = int(page)
        search_result = Post.query.filter(Post.Title.like('%' + keyword + '%')) \
            .order_by(Post.Id.desc()).paginate(page, per_page=2, error_out=False)
        articles = search_result.items
        lenth = len(articles)
        tem = []
        for x in articles:
            tem.append(x.to_json())
        print jsonify(tem)
        return jsonify(objects=tem)
    if request.method == 'GET':
        keyword = request.args.get("keyword")
        search_result = Post.query.filter(Post.Title.like('%' + keyword + '%'))\
            .order_by(Post.Id.desc()).paginate(1, per_page=2, error_out=False)
        articles = search_result.items
        tem = []
        lenth=0
        if articles is not None:
            lenth = len(articles)
            for x in articles:
                tem.append(x.to_json())
            print jsonify(tem)
        return render_template('search.html', articles=articles, search_result=search_result, lenth=lenth, keyword=keyword)
