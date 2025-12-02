from flask import Flask, request, redirect
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6

import datetime
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'секретно-секретный-секрет')
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'sqlite')

app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)

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
