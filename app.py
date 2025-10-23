from flask import Flask, request, redirect
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
import datetime

app = Flask(__name__)
app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)

@app.route("/")
def start():
       return """<!doctype html>
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
                </ul>
                <hr>
                <footer>
                    Артемченко Елизавета Сергеевна, ФБИ-33, 3 курс, 2025 год
                </footer>
            </body" 
        </html>"""


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
