#_*_ coding:utf-8 _*_
import os
from flask import Flask
import click
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_pyfile('settings.py')
db = SQLAlchemy(app)

@click.command('say') #这里的字符串就是配合flask命令行要用到字符
#@with_appcontext
def say_hello():
    click.echo('Initialized the database.')

@app.shell_context_processor
def make_shell_context():
    return dict(db=db)

from inventory import views


