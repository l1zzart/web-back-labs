from flask import Flask, url_for, request, redirect, abort, render_template
import datetime
app = Flask(__name__)

@app.errorhandler(404)
def not_found(err):
    return redirect("/lab1/404")

@app.route("/lab1")
def lab1():
    return """<!doctype html>
        <html>
            <head>
                <title>Лабораторная 1</title>
            </head> 
            <body>
                Flask – фреймворк для создания веб-приложений на языке программирования Python, 
                использующий набор инструментов Werkzeug, а также шаблонизатор Jinja2. 
                Относится к категории так называемых микрофреймворков – минималистичных каркасов веб-приложений, 
                сознательно предоставляющих лишь самые базовые возможности.
                <br>
                <a href="/">На главную</a>
                <h2>Список роутов</h2>
                <ul>
                    <li><a href="/lab1/index">/labl/index</a></li>
                    <li><a href="/lab1/web">/labl/web</a></li>
                    <li><a href="/lab1/author">/labl/author</a></li>
                    <li><a href="/lab1/image">/labl/image</a></li>
                    <li><a href="/lab1/counter">/labl/counter</a></li>
                    <li><a href="/lab1/reset_counter">/labl/reset_counter</a></li>
                    <li><a href="/lab1/info">/labl/info</a></li>
                    <li><a href="/lab1/created">/labl/created</a></li>
                    <li><a href="/lab1/400">/labl/400</a></li>
                    <li><a href="/lab1/401">/labl/401</a></li>
                    <li><a href="/lab1/402">/labl/402</a></li>
                    <li><a href="/lab1/403">/labl/403</a></li>
                    <li><a href="/lab1/404">/labl/404</a></li>
                    <li><a href="/lab1/405">/labl/405</a></li>
                    <li><a href="/lab1/418">/labl/418</a></li>
                    <li><a href="/lab1/500">/labl/500</a></li>
                </ul>
            </body>
        </html>"""

@app.route("/")
@app.route("/lab1/index")
def index():
    return """<!doctype html>
        <html>
            <head>
                <title>НГТУ, ФБ, Лабораторные работы</title>
            </head>
            <body>
                <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
                <ul>
                    <li><a href='/lab1'>Первая лабораторная</a></li>
                </ul>
                <hr>
                <footer>
                    Артемченко Елизавета Сергеевна, ФБИ-33, 3 курс, 2025 год
                </footer>
            </body" 
        </html>"""

@app.route("/lab1/web")
def web():
    return """<!doctype html>
        <html>
            <body>
                <h1>web-сервер на flask</h1>
                <a href="/lab1/author">author</a>
            </body" 
        </html>""", 200, {
            'X-Server': 'sample',
            'Content-Type': 'text/plain; charset=utf-8'
            }

@app.route("/lab1/author")
def author():
    name = "Артемченко Елизавета Сергеевна"
    group = "ФБИ-33"
    faculty = "ФБ"

    return """<!doctype html>
        <html>
            <body>
                <p>Студент: """ + name + """</p>
                <p>Группа: """ + group + """</p>
                <p>Факультет: """ + faculty + """</p>
                <a href="/lab1/web">web</a>
            </body>
        </html>"""

@app.route("/lab1/image")
def image():
    path = url_for("static", filename="oak.jpg")
    css = url_for("static", filename="lab1.css")
    return f"""<!doctype html>
        <html>
            <head>
                <link rel="stylesheet" href="{css}">
            </head>
            <body>
                <h1>Дуб</h1>
                <img src="{path}">
            </body>
        </html>""", 200, {
            "Content-Type": "text/html; charset=utf-8",
            "Content-Language": "ru-Ru",
            "X-My-Header-1": "Lab 1",
            "X-My-Header-2": "Artemchenko E.S."
            }

count = 0

@app.route('/lab1/counter')
def counter():
    global count
    count += 1
    time = datetime.datetime.today()
    url = request.url
    client_ip = request.remote_addr

    return '''
    <!doctype html>
    <html>
        <body>
            Сколько раз вы сюда заходили: ''' + str(count) + '''
            <hr>
            Дата и время: ''' + str(time) + '''<br>
            Запрошенный адрес: ''' + str(url) + '''<br>
            Ваш IP-адрес: ''' + str(client_ip) + '''<br>
            <a href='/lab1/reset_counter'>Сбросить счётчик</a>
        </body>
    </html>
    '''
@app.route('/lab1/reset_counter')
def reset_counter():
    global count 
    count = 0
    return redirect("/lab1/counter")

@app.route('/lab1/info')
def info():
    return redirect("/lab1/author")

@app.route('/lab1/created')
def created():
    return '''
    <!doctype html>
    <html>
        <body>
            <h1>Создано успешно</h1>
            <div><i>что-то создано...</i></div>
        </body>
    </html>
    '''
@app.route("/lab1/400")
def error_400():
    return "<h1>400 Bad Request</h1><p>Неверный запрос</p>", 400

@app.route("/lab1/401")
def error_401():
    return "<h1>401 Unauthorized</h1><p>Требуется авторизация</p>", 401

@app.route("/lab1/402")
def error_402():
    return "<h1>402 Payment Required</h1><p>Требуется оплата</p>", 402

@app.route("/lab1/403")
def error_403():
    return "<h1>403 Forbidden</h1><p>Доступ запрещен</p>", 403

access_log = []

@app.route("/lab1/404")
def error_404():
    global access_log
    ip_address = request.remote_addr
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    requested_url = request.url
    root_url = url_for('index', _external=True) 
    
    log_entry = f"IP: {ip_address}, Дата/Время: {current_time}, URL: {requested_url}"
    access_log.append(log_entry)
    
    css = url_for("static", filename="error.css")
    img_path = url_for("static", filename="UFO.png")

    log_html = "<h2>Лог посещений:</h2><ul>"
    for log in access_log:
        log_html += f"<li>{log}</li>"
    log_html += "</ul>"

    html = f"""<!doctype html>
        <html>
            <head>
                <link rel="stylesheet" href="{css}">
                <title>404 Not Found</title>
            </head>
            <body>
                <div class="container">
                    <h1>404</h1>
                    <p>LOOKS LIKE YOURE LOST!</p>
                    <p>Ваш IP-адрес: {ip_address}</p>
                    <p>Дата доступа: {current_time}</p>
                    <p><a href="{root_url}">GO BACK TO THE HOME PAGE</a></p>
                    <img src="{img_path}" alt="UFO" class="ufo-image">
                </div>
                <hr>
                {log_html}
            </body>
        </html>"""
    return html

@app.route("/lab1/405")
def error_405():
    return "<h1>405 Method Not Allowed</h1><p>Метод не разрешен</p>", 405

@app.route("/lab1/418")
def error_418():
    return "<h1>418 I'M A TEAPOT</h1><p>Я ЧАЙНИК</p>", 418

@app.route("/lab1/500")
def error_500():
    x = 1 / 0
    return f"Ответ: {x}"

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

@app.route('/lab2/a')
def a():
    return 'без слэша'

@app.route('/lab2/a/')
def a2():
    return 'со слэшем'

flower_list = ['роза', 'тюльпан', 'незабудка', 'ромашка']

@app.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        abort(404)
    else:
        return f'''
<!doctype html>
<html>
    <head>
        <title>Цветок #{flower_id}</title>
    </head>
    <body>
        <h1>Информация о цветке</h1>
        <p>Цветок: <strong>{flower_list[flower_id]}</strong></p>
        <p>ID: {flower_id}</p>
        <a href="/lab2/all_flowers">Посмотреть все цветы</a>
    </body>
</html>
'''

@app.route('/lab2/add_flower/', defaults={'name': None})
@app.route('/lab2/add_flower/<name>')
def add_flower(name):
    if name is None:
        abort(400, "вы не задали имя цветка")
    
    flower_list.append(name)
    return f'''
<!doctype html>
<html>
    <head>
        <title>Цветок добавлен</title>
    </head>
    <body>
        <h1>Добавлен новый цветок</h1>
        <p>Название нового цветка: {name}</p>
        <p>Всего цветов: {len(flower_list)}</p>
        <p>Полный список: {flower_list}</p>
        <a href="/lab2/all_flowers">Посмотреть все цветы</a>
    </body>
</html>
'''

@app.route('/lab2/all_flowers')
def all_flowers():
    return f'''
<!doctype html>
<html>
    <head>
        <title>Все цветы</title>
    </head>
    <body>
        <h1>Список всех цветов</h1>
        <p>Всего цветов: {len(flower_list)}</p>
        <ul>
            {"".join(f'<li>{i}: {flower}</li>' for i, flower in enumerate(flower_list))}
        </ul>
        <a href="/lab2/clear_flowers">Очистить список цветов</a>
    </body>
</html>
'''

@app.route('/lab2/clear_flowers')
def clear_flowers():
    flower_list.clear()
    return '''
<!doctype html>
<html>
    <head>
        <title>Список очищен</title>
    </head>
    <body>
        <h1>Список цветов очищен</h1>
        <p>Все цветы были удалены из списка.</p>
        <a href="/lab2/all_flowers">Посмотреть все цветы</a>
    </body>
</html>
'''

@app.route('/lab2/example')
def example():
    name = 'Елизавета Артемченко'
    number = '2'
    group = 'ФБИ-33'
    course = '3'
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'груши', 'price': 120}, 
        {'name': 'апельсины', 'price': 80}, 
        {'name': 'мандарины', 'price': 95}, 
        {'name': 'манго', 'price': 321}
    ]
    return render_template('example.html', 
                           name=name, 
                           number=number, 
                           group=group, 
                           course=course,
                           fruits=fruits)

@app.route('/lab2/')
def lab2():
    return render_template('lab2.html')

@app.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase = phrase)

@app.route('/lab2/calc/')
def calc_default():
    return redirect('/lab2/calc/1/1')

@app.route('/lab2/calc/<int:a>')
def calc_single(a):
    return redirect(f'/lab2/calc/{a}/1')

@app.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    return f'''
<!doctype html>
<html>
    <head>
        <title>Калькулятор</title>
    </head>
    <body>
        <h1>Расчёт с параметрами:</h1>
        <p>{a} + {b} = <strong>{a + b}</strong></p>
        <p>{a} - {b} = <strong>{a - b}</strong></p>
        <p>{a} × {b} = <strong>{a * b}</strong></p>
        <p>{a} / {b} = <strong>{a / b if b != 0 else 'Ошибка: деление на ноль!'}</strong></p>
        <p>{a}<sup>{b}</sup> = <strong>{a ** b}</strong></p>
        
        <h2>Попробуйте другие числа:</h2>
        <ul>
            <li><a href="/lab2/calc/5/2">5 и 2</a></li>
            <li><a href="/lab2/calc/10/3">10 и 3</a></li>
            <li><a href="/lab2/calc/8/8">8 и 8</a></li>
        </ul>
    </body>
</html>
'''
books_list = [
    {'id': 1, 'author': 'Фёдор Достоевский', 'title': 'Преступление и наказание', 'genre': 'Роман', 'pages': 671},
    {'id': 2, 'author': 'Лев Толстой', 'title': 'Война и мир', 'genre': 'Роман-эпопея', 'pages': 1225},
    {'id': 3, 'author': 'Антон Чехов', 'title': 'Рассказы', 'genre': 'Рассказы', 'pages': 350},
    {'id': 4, 'author': 'Михаил Булгаков', 'title': 'Мастер и Маргарита', 'genre': 'Роман', 'pages': 480},
    {'id': 5, 'author': 'Александр Пушкин', 'title': 'Евгений Онегин', 'genre': 'Роман в стихах', 'pages': 240},
    {'id': 6, 'author': 'Николай Гоголь', 'title': 'Мёртвые души', 'genre': 'Поэма', 'pages': 352},
    {'id': 7, 'author': 'Иван Тургенев', 'title': 'Отцы и дети', 'genre': 'Роман', 'pages': 283},
    {'id': 8, 'author': 'Александр Островский', 'title': 'Гроза', 'genre': 'Драма', 'pages': 120},
    {'id': 9, 'author': 'Михаил Лермонтов', 'title': 'Герой нашего времени', 'genre': 'Роман', 'pages': 224},
    {'id': 10, 'author': 'Иван Гончаров', 'title': 'Обломов', 'genre': 'Роман', 'pages': 400},
    {'id': 11, 'author': 'Александр Грибоедов', 'title': 'Горе от ума', 'genre': 'Комедия', 'pages': 160},
    {'id': 12, 'author': 'Николай Лесков', 'title': 'Левша', 'genre': 'Повесть', 'pages': 96}
]

@app.route('/lab2/books')
def books():
    return render_template('books.html', books=books_list)
