#_*_ coding:utf-8 _*_
import os
from inventory import app

dev_db = 'sqlite:///' + os.path.join(app.instance_path, 'inventory.sqlite')

SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', dev_db)
SECRET_KEY = os.getenv('SECRET_KEY', 'BBSSRRDD')
SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', False)