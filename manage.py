#!/usr/bin/env python
#coding:utf-8
from flask_script import Manager, Server
from app import app
from app.models import db, User, Post, Comment, Tag, tags

manager = Manager(app)
manager.add_command("server", Server())

@manager.shell
def make_shell_context():
    return dict(app=app, db=db, User=User, Post=Post, Comment=Comment, Tag=Tag, tags=tags)

if __name__ == "__main__":
    manager.run()