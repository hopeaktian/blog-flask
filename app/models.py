#!/usr/bin/env python
#coding:utf-8
"""
file:.py
date:2018/12/1 12:09
author:    peak
description:
"""
from flask_sqlalchemy import SQLAlchemy
import datetime, os, time

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'User'  #表名字默认是类名字的小写版本(如果没有此语句)

    Id = db.Column(db.Integer(), primary_key=True)
    Name = db.Column(db.String(255))
    Password = db.Column(db.String(255))
    Email = db.Column(db.String(255))
    Register_Date = db.Column(db.DateTime, default=datetime.datetime.now)

tags = db.Table('Post_Tags',
                db.Column('Id', db.Integer, primary_key=True),
                db.Column('post_id', db.Integer, db.ForeignKey('Post.Id'), ),
                db.Column('tag_id', db.Integer, db.ForeignKey('Tag.Id'))

                )

class Post(db.Model):
    __tablename__ = 'Post'

    Id = db.Column(db.Integer(), primary_key=True)
    Title = db.Column(db.String(255), nullable=False)                                           # 文章标题
    Publish_Date = db.Column(db.DateTime, default=datetime.datetime.now, nullable=False)        # 文章日期
    Cover_Picture_Name = db.Column(db.String(255))                              # 封面图片名字
    Content_Name = db.Column(db.String(255))                                    # 内容markdown文件名字
    Music_Name = db.Column(db.String(255))                                      # 音乐名，可为空
    Dir_Name = db.Column(db.String(255))                                        # 文章目录

    User_Id = db.Column(db.Integer(), db.ForeignKey('User.Id'))                 # 作者
    user = db.relationship('User', foreign_keys='Post.User_Id')

    tags = db.relationship(
        'Tag',
        secondary=tags,
        backref=db.backref('posts', lazy='dynamic')
    )

    # Comments = db.Column(db.Integer(), db.ForeignKey('Comments.Id'))            # 评论
    # comment = db.relationship('Comments', foreign_keys='Comments.Id')

    def to_json(self):
        Publish_date = str(self.Publish_Date.year)+"-"+str(self.Publish_Date.month)+"-"+str(self.Publish_Date.day)+" "+str(self.Publish_Date.hour)+":"+str(self.Publish_Date.minute)+":"+str(self.Publish_Date.second)
        Publish_year = str(self.Publish_Date.year)
        Publish_month = str(self.Publish_Date.month)
        return {
            'Title': self.Title,
            'Publish_Date': Publish_date,
            'Publish_year': Publish_year,
            'Publish_month': Publish_month,
            'Dir_Name': self.Dir_Name,
            'Cover_Picture_Name': self.Cover_Picture_Name,
            'Id': self.Id
        }

class Comment(db.Model):
    __tablename__ = 'Comment'

    Id = db.Column(db.Integer(), primary_key=True)
    Name = db.Column(db.String(255), nullable=False)
    Email = db.Column(db.String(255), nullable=False)
    text = db.Column(db.Text())
    Date = db.Column(db.DateTime, default=datetime.datetime.now, nullable=False)                # 日期
    Post_Id = db.Column(db.Integer(), db.ForeignKey('Post.Id'))

class Tag(db.Model):
    __tablename__ = 'Tag'

    Id = db.Column(db.Integer(), primary_key=True)
    Title = db.Column(db.String(255), nullable=False)

class Access(db.Model):
    __tablename__ = 'Access'  # 表名字默认是类名字的小写版本(如果没有此语句)

    Id = db.Column(db.Integer(), primary_key=True)
    Access_Date = db.Column(db.DateTime, default=datetime.datetime.now, nullable=False)
    Ip = db.Column(db.String(255))

class Like(db.Model):
    __tablename__ = 'Like'
    Id = db.Column(db.Integer(), primary_key=True)
    Like_Date = db.Column(db.DateTime, default=datetime.datetime.now, nullable=False)
    Like_Type = db.Column(db.Integer())             # 0为取消点赞，1为点赞
