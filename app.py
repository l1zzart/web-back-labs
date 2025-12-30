from flask import Flask, request, redirect
from flask_sqlalchemy import SQLAlchemy
from db import db
from db.models import users
from flask_login import LoginManager

from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab7 import lab7
from lab8 import lab8
from lab9 import lab9
from rgz import rgz

import datetime
import os
from os import path

app = Flask(__name__)

login_manager = LoginManager()
login_manager.login_view = 'lab8.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_users(login_id):
    return users.query.get(int(login_id))

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'секретно-секретный-секрет')
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'sqlite')

if app.config['DB_TYPE'] == 'postgres':
    db_name = 'elizaveta_artemchenko_orm'
    db_user = 'elizaveta_artemchenko_orm'
    db_password = '123'
    host_ip = '127.0.0.1'
    host_port = 5432

    app.config['SQLALCHEMY_DATABASE_URI'] = \
        f'postgresql://{db_user}:{db_password}@{host_ip}:{host_port}/{db_name}'
else:
    dir_path = path.dirname(path.realpath(__file__))
    db_path = path.join(dir_path, "elizaveta_artemchenko_orm.db")
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

db.init_app(app)

app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(lab7)
app.register_blueprint(lab8)
app.register_blueprint(lab9)
app.register_blueprint(rgz, url_prefix='/rgz')

@app.route("/")
def index():
    html = f"""<!doctype html>
    <html>
        <head>
            <title>НГТУ, ФБ, Лабораторные работы</title>
        </head>
        <body>
            <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
            <ul>
                <li><a href='/lab1/'>Лабораторная работа 1</a></li>
                <li><a href='/lab2/'>Лабораторная работа 2</a></li>
                <li><a href='/lab3/'>Лабораторная работа 3</a></li>
                <li><a href='/lab4/'>Лабораторная работа 4</a></li>
                <li><a href='/lab5/'>Лабораторная работа 5</a></li>
                <li><a href='/lab6/'>Лабораторная работа 6</a></li>
                <li><a href='/lab7/'>Лабораторная работа 7</a></li>
                <li><a href='/lab8/'>Лабораторная работа 8</a></li>
                <li><a href='/lab9/'>Лабораторная работа 9</a></li>
                <li><a href='/rgz/'><strong>РГЗ: Магазин мебели (вариант 0)</strong></a></li>
            </ul>
            <hr>
            <footer>
                Артемченко Елизавета Сергеевна, ФБИ-33, 3 курс, 2025 год
            </footer>
        </body> 
    </html>"""
    return html


@app.errorhandler(404)
def not_found(err):
    return redirect("/lab1/404")


@app.errorhandler(500)
def internal_error(err):
    return f"""<!doctype html>
        <html>
            <head>
                <title>Ошибка сервера</title>
            </head>
            <body>
                <h1 style="color: red;">500 - ВНУТРЕННЯЯ ОШИБКА СЕРВЕРА</h1>
                <p style="font-size: 20px;">Упс, на сервере произошла непредвиденная ошибка. Попробуйте позже...</p>
            </body>
        </html>"""
