from flask import Flask, url_for, request, redirect, abort, render_template
from lab1 import lab1
import datetime

app = Flask(__name__)
app.register_blueprint(lab1)

@app.errorhandler(404)
def not_found(err):
    return redirect("/lab1/404")


@app.route("/")
def start():
       return """<!doctype html>
        <html>
            <head>
                <title>WEB-программирование, часть 2. Главное меню</title>
            </head> 
            <body>
                <h2>Список лабораторных работ</h2>
                <ul>
                    <li><a href="/lab1">Лабораторная работа 1</a></li>
                    <li><a href="/lab2/">Лабораторная работа 2</a></li>
                    <li><a href="/lab3/">Лабораторная работа 3</a></li>
                </ul>
            </body>
        </html>"""


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


flower_list = [
    {'id': 0, 'name': 'роза', 'price': 300},
    {'id': 1, 'name': 'тюльпан', 'price': 310},
    {'id': 2, 'name': 'незабудка', 'price': 320},
    {'id': 3, 'name': 'ромашка', 'price': 330}
]

next_flower_id = len(flower_list)


@app.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    flower = next((f for f in flower_list if f['id'] == flower_id), None)
    if flower is None:
        abort(404)
    return render_template('flower_detail.html', flower=flower)


@app.route('/lab2/all_flowers', methods=['GET', 'POST'])
def all_flowers():
    global next_flower_id
    
    if request.method == 'POST':
        flower_name = request.form.get('flower_name')
        flower_price = request.form.get('flower_price')
        
        if flower_name and flower_price:
            new_flower = {
                'id': next_flower_id,
                'name': flower_name,
                'price': int(flower_price)
            }
            flower_list.append(new_flower)
            next_flower_id += 1
        
        return redirect(url_for('all_flowers'))
    
    return render_template('all_flowers.html', flower_list=flower_list)


@app.route('/lab2/del_flower/<int:flower_id>')
def delete_flower(flower_id):
    global flower_list
    flower_list = [f for f in flower_list if f['id'] != flower_id]
    return redirect(url_for('all_flowers'))


@app.route('/lab2/clear_flowers')
def clear_flowers():
    global flower_list, next_flower_id
    flower_list.clear()
    next_flower_id = 0
    return redirect(url_for('all_flowers'))


@app.route('/lab2/add_flower/', defaults={'name': None})
@app.route('/lab2/add_flower/<name>')
def add_flower(name):
    global next_flower_id
    
    if name is None:
        abort(400, "вы не задали имя цветка")
    
    new_flower = {
        'id': next_flower_id,
        'name': name,
        'price': 300
    }
    flower_list.append(new_flower)
    next_flower_id += 1
    
    return render_template('add_flower.html', name=name, flower_list=flower_list)


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


fl = [
    {
        'name': 'Роза',
        'description': 'Королева цветов, символ любви и красоты',
        'image': 'rose.jpg'
    },
    {
        'name': 'Тюльпан', 
        'description': 'Весенний цветок, символ Голландии',
        'image': 'tulip.jpg'
    },
    {
        'name': 'Орхидея',
        'description': 'Экзотический цветок с уникальной формой',
        'image': 'orchid.jpg'
    },
    {
        'name': 'Подсолнух',
        'description': 'Солнечный цветок, который поворачивается за солнцем',
        'image': 'sunflower.jpg'
    },
    {
        'name': 'Ландыш',
        'description': 'Нежный ароматный цветок в форме колокольчиков',
        'image': 'lily_of_the_valley.jpg'
    },
    {
        'name': 'Лаванда',
        'description': 'Ароматное растение с успокаивающим запахом',
        'image': 'lavender.jpg'
    },
    {
        'name': 'Хризантема',
        'description': 'Осенний цветок, символ долголетия',
        'image': 'chrysanthemum.jpg'
    },
    {
        'name': 'Пион',
        'description': 'Пышный цветок с богатыми лепестками',
        'image': 'peony.jpg'
    },
    {
        'name': 'Нарцисс',
        'description': 'Весенний цветок с легким ароматом',
        'image': 'daffodil.jpg'
    },
    {
        'name': 'Ирис',
        'description': 'Цветок с необычной формой, назван в честь богини радуги',
        'image': 'iris.jpg'
    },
    {
        'name': 'Георгин',
        'description': 'Яркий цветок с множеством лепестков',
        'image': 'dahlia.jpg'
    },
    {
        'name': 'Гладиолус',
        'description': 'Высокий цветок с соцветиями вдоль стебля',
        'image': 'gladiolus.jpg'
    },
    {
        'name': 'Фиалка',
        'description': 'Небольшой скромный цветок с приятным ароматом',
        'image': 'violet.jpg'
    },
    {
        'name': 'Лотос',
        'description': 'Священный цветок в Азии, растет в воде',
        'image': 'lotus.jpg'
    },
    {
        'name': 'Мак',
        'description': 'Яркий цветок с нежными лепестками',
        'image': 'poppy.jpg'
    },
    {
        'name': 'Гвоздика',
        'description': 'Цветок с зубчатыми лепестками',
        'image': 'carnation.jpg'
    },
    {
        'name': 'Фрезия',
        'description': 'Изящный ароматный цветок для букетов',
        'image': 'freesia.jpg'
    },
    {
        'name': 'Астра',
        'description': 'Осенний цветок в форме звезды',
        'image': 'aster.jpg'
    },
    {
        'name': 'Гортензия',
        'description': 'Пышный цветок с крупными соцветиями',
        'image': 'hydrangea.jpg'
    },
    {
        'name': 'Калла',
        'description': 'Элегантный цветок для свадебных букетов',
        'image': 'calla_lily.jpg'
    }
]


@app.route('/lab2/fl_catalog')
def show_fl():
    return render_template('fl.html', fl=fl)
