from flask import Blueprint, render_template, request, make_response, redirect
import datetime
lab3 = Blueprint('lab3', __name__)


@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name')
    name_color = request.cookies.get('name_color')
    if not name:
        name = "Аноним"
    age = request.cookies.get('age')
    if not age:
        age = "Не указан"
    return render_template('lab3/lab3.html', name=name, name_color=name_color, age=age)


@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'magenta')
    return resp


@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp


@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    if user == '':
        errors['user'] = 'Заполните поле!'

    age = request.args.get('age')
    sex = request.args.get('sex')
    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)


@lab3.route('/lab3/order')
def order():
    return render_template('/lab3/order.html')


@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')

    if drink == 'cofee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70

    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10

    return render_template('lab3/pay.html', price=price)


@lab3.route('/lab3/success')
def success():
    price = request.args.get('price', 0)
    return render_template('/lab3/success.html', price=price)


@lab3.route('/lab3/settings')
def settings():
    color = request.args.get('color')
    bg_color = request.args.get('bg_color')
    font_size = request.args.get('font_size')
    font_style = request.args.get('font_style')
    if color or bg_color or font_size or font_style:
        resp = make_response(redirect('/lab3/settings'))
        if color:
            resp.set_cookie('color', color)
        if bg_color:
            resp.set_cookie('bg_color', bg_color)
        if font_size:
            resp.set_cookie('font_size', font_size)
        if font_style:
            resp.set_cookie('font_style', font_style)
        return resp

    color = request.cookies.get('color')
    bg_color = request.cookies.get('bg_color')
    font_size = request.cookies.get('font_size')
    font_style = request.cookies.get('font_style')

    resp = make_response(render_template('lab3/settings.html', color=color, bg_color=bg_color, font_size=font_size, font_style=font_style))
    return resp


@lab3.route('/lab3/ticket', methods=['GET', 'POST'])
def ticket():
    if request.method == 'GET':
        return render_template('lab3/ticket.html')
    
    fio = request.form.get('fio')
    shelf = request.form.get('shelf')
    linens = request.form.get('linens') == 'on'
    luggage = request.form.get('luggage') == 'on'
    age = request.form.get('age')
    departure = request.form.get('departure')
    destination = request.form.get('destination')
    date = request.form.get('date')
    insurance = request.form.get('insurance') == 'on'

    if not all([fio, shelf, age, departure, destination, date]):
        return "Все поля должны быть заполнены!", 400

    try:
        age = int(age)
        if not (1 <= age <= 120):
            return "Возраст должен быть от 1 до 120 лет!", 400
    except ValueError:
        return "Возраст должен быть числом!", 400

    if age < 18:
        price = 700  
    else:
        price = 1000  

    if shelf in ['lower', 'side-lower']:
        price += 100

    if linens:
        price += 75

    if luggage:
        price += 250

    if insurance:
        price += 150

    base_price = 700 if age < 18 else 1000
    shelf_price = 100 if shelf in ['lower', 'side-lower'] else 0

    return render_template('lab3/info.html',
                        fio=fio,
                        shelf=shelf,
                        linens=linens,
                        luggage=luggage,
                        age=age,
                        departure=departure,
                        destination=destination,
                        date=date,
                        insurance=insurance,
                        price=price,
                        base_price=base_price,
                        shelf_price=shelf_price)


@lab3.route('/lab3/clear')
def clear():
    response = make_response(redirect('/lab3/settings'))
    response.delete_cookie('color')
    response.delete_cookie('bg_color')
    response.delete_cookie('font_size')
    response.delete_cookie('font_style')
    return response


@lab3.route('/lab3/products')
def products():

    products_list = [
        {'name': 'Porsche 911 Carrera', 'price': 12500000, 'brand': 'Porsche', 'year': 2023, 'horsepower': 385},
        {'name': 'Chevrolet Corvette Stingray', 'price': 8500000, 'brand': 'Chevrolet', 'year': 2024, 'horsepower': 495},
        {'name': 'BMW M4 Competition', 'price': 9200000, 'brand': 'BMW', 'year': 2023, 'horsepower': 510},
        {'name': 'Audi R8', 'price': 15800000, 'brand': 'Audi', 'year': 2023, 'horsepower': 562},
        {'name': 'Mercedes-AMG GT', 'price': 13200000, 'brand': 'Mercedes-Benz', 'year': 2024, 'horsepower': 523},
        {'name': 'Nissan GT-R', 'price': 11500000, 'brand': 'Nissan', 'year': 2023, 'horsepower': 565},
        {'name': 'Ford Mustang Shelby GT500', 'price': 7800000, 'brand': 'Ford', 'year': 2024, 'horsepower': 760},
        {'name': 'Lamborghini Huracan', 'price': 28500000, 'brand': 'Lamborghini', 'year': 2023, 'horsepower': 640},
        {'name': 'Ferrari F8 Tributo', 'price': 32500000, 'brand': 'Ferrari', 'year': 2023, 'horsepower': 720},
        {'name': 'McLaren 720S', 'price': 29500000, 'brand': 'McLaren', 'year': 2024, 'horsepower': 720},
        {'name': 'Toyota GR Supra', 'price': 5200000, 'brand': 'Toyota', 'year': 2023, 'horsepower': 382},
        {'name': 'Honda Civic Type R', 'price': 4800000, 'brand': 'Honda', 'year': 2024, 'horsepower': 315},
        {'name': 'Subaru WRX STI', 'price': 4500000, 'brand': 'Subaru', 'year': 2023, 'horsepower': 310},
        {'name': 'Mazda MX-5 Miata', 'price': 3500000, 'brand': 'Mazda', 'year': 2024, 'horsepower': 181},
        {'name': 'Porsche 718 Cayman', 'price': 6800000, 'brand': 'Porsche', 'year': 2023, 'horsepower': 300},
        {'name': 'Aston Martin Vantage', 'price': 18500000, 'brand': 'Aston Martin', 'year': 2024, 'horsepower': 510},
        {'name': 'Lexus LC 500', 'price': 9500000, 'brand': 'Lexus', 'year': 2023, 'horsepower': 471},
        {'name': 'Jaguar F-Type', 'price': 8200000, 'brand': 'Jaguar', 'year': 2024, 'horsepower': 450},
        {'name': 'Alfa Romeo Giulia Quadrifoglio', 'price': 8900000, 'brand': 'Alfa Romeo', 'year': 2023, 'horsepower': 505},
        {'name': 'Dodge Challenger SRT Hellcat', 'price': 7200000, 'brand': 'Dodge', 'year': 2024, 'horsepower': 717}
    ]

    min_price_cookie = request.cookies.get('min_price', '')
    max_price_cookie = request.cookies.get('max_price', '')
    
    min_price = request.args.get('min_price', min_price_cookie)
    max_price = request.args.get('max_price', max_price_cookie)
    
    if 'reset' in request.args:
        min_price = ''
        max_price = ''
    
    all_prices = [p['price'] for p in products_list]
    min_all_price = min(all_prices)
    max_all_price = max(all_prices)
    
    filtered_products = products_list
    
    if min_price or max_price:
        try:
            min_val = float(min_price) if min_price else 0
            max_val = float(max_price) if max_price else float('inf')
            
            if min_val > max_val:
                min_val, max_val = max_val, min_val
                min_price, max_price = str(max_val), str(min_val)
            
            filtered_products = [
                p for p in products_list 
                if min_val <= p['price'] <= max_val
            ]
            
        except ValueError:
            filtered_products = products_list
    
    response = make_response(render_template(
        'lab3/products.html',
        products=filtered_products,
        min_price=min_price,
        max_price=max_price,
        min_all_price=min_all_price,
        max_all_price=max_all_price,
        products_count=len(filtered_products),
        total_count=len(products_list)
    ))
    
    if 'reset' not in request.args:
        response.set_cookie('min_price', min_price, max_age=30*24*60*60)
        response.set_cookie('max_price', max_price, max_age=30*24*60*60)
    else:
        response.delete_cookie('min_price')
        response.delete_cookie('max_price')
    
    return response
