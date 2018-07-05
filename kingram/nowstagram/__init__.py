"""
初始化定义
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_pyfile('app.conf')
db = SQLAlchemy(app)
app.secret_key = 'james'

login_manager = LoginManager(app)

login_manager.login_view = '/reloginpage'

from nowstagram import views, models
