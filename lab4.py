from flask import Blueprint, render_template, request, redirect, session
lab4 = Blueprint('lab4', __name__)

@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')


@lab4.route('/lab4/div-form')
def div_form():
    return render_template('lab4/div-form.html')


@lab4.route('/lab4/div', methods = ['POST'])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/div.html', error='Оба поля должны быть заполнены!')

    x1 = int(x1)
    x2 = int(x2)
    
    if x2 == 0:
        return render_template('lab4/div.html', error='Деление на ноль невозможно!')
    
    result = x1 / x2
    return render_template('lab4/div.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/sum-form')
def sum_form():
    return render_template('lab4/sum-form.html')


@lab4.route('/lab4/sum', methods=['POST'])
def sum_numbers():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    x1 = int(x1) if x1 != '' else 0
    x2 = int(x2) if x2 != '' else 0
    
    result = x1 + x2
    return render_template('lab4/sum.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/mult-form')
def mult_form():
    return render_template('lab4/mult-form.html')


@lab4.route('/lab4/mult', methods=['POST'])
def mult_numbers():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    x1 = int(x1) if x1 != '' else 1
    x2 = int(x2) if x2 != '' else 1
    
    result = x1 * x2
    return render_template('lab4/mult.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/sub-form')
def sub_form():
    return render_template('lab4/sub-form.html')

@lab4.route('/lab4/sub', methods=['POST'])
def sub_numbers():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if x1 == '' or x2 == '':
        return render_template('lab4/sub.html', error='Оба поля должны быть заполнены!')

    x1 = int(x1)
    x2 = int(x2)
    
    result = x1 - x2
    return render_template('lab4/sub.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/pow-form')
def pow_form():
    return render_template('lab4/pow-form.html')


@lab4.route('/lab4/pow', methods=['POST'])
def pow_numbers():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if x1 == '' or x2 == '':
        return render_template('lab4/pow.html', error='Оба поля должны быть заполнены!')

    x1 = int(x1)
    x2 = int(x2)
    
    if x1 == 0 and x2 == 0:
        return render_template('lab4/pow.html', error='Оба числа не могут быть равны нулю!')
    
    result = x1 ** x2
    return render_template('lab4/pow.html', x1=x1, x2=x2, result=result)

tree_count = 0 
MAX_TREES = 10 

@lab4.route('/lab4/tree', methods=['GET', 'POST'])
def tree():
    global tree_count
    
    if request.method == 'POST':
        operation = request.form.get('operation')

        if operation == 'cut':

            if tree_count > 0:
                tree_count -= 1
        elif operation == 'plant':

            if tree_count < MAX_TREES:
                tree_count += 1

        return redirect('/lab4/tree')
    
    return render_template('lab4/tree.html', tree_count=tree_count, max_trees=MAX_TREES)


users = [
    {'login': 'alex', 'password': '123', 'name': 'Александр Петров', 'gender': 'male'},
    {'login': 'bob', 'password': '555', 'name': 'Robert Janson', 'gender': 'male'},
    {'login': 'liza', 'password': '321', 'name': 'Елизавета Артемченко', 'gender': 'female'},
]

@lab4.route('/lab4/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'login' in session:
            authorized = True
            user_name = session.get('name', '')
            return render_template('lab4/login.html', authorized=authorized, user_name=user_name)
        else:
            return render_template('lab4/login.html', authorized=False)

    login = request.form.get('login')
    password = request.form.get('password')
    entered_login = login

    if not login:
        error = 'Не введён логин'
        return render_template('lab4/login.html', error=error, authorized=False, entered_login=entered_login)
    
    if not password:
        error = 'Не введён пароль'
        return render_template('lab4/login.html', error=error, authorized=False, entered_login=entered_login)

    user_found = None
    for user in users:
        if login == user['login'] and password == user['password']:
            user_found = user
            break

    if user_found:
        session['login'] = login
        session['name'] = user_found['name'] 
        return redirect('/lab4/login')
    else:
        error = 'Неверные логин и/или пароль'
        return render_template('lab4/login.html', error=error, authorized=False, entered_login=entered_login)

@lab4.route('/lab4/logout', methods=['POST'])
def logout():
    session.pop('login', None)
    session.pop('name', None)
    return redirect('/lab4/login')


@lab4.route('/lab4/fridge', methods=['GET', 'POST'])
def fridge():
    if request.method == 'GET':
        return render_template('lab4/fridge.html')
    
    temperature = request.form.get('temperature')
    
    if not temperature:
        return render_template('lab4/fridge.html', error='Ошибка: не задана температура')
    
    try:
        temp = int(temperature)
    except ValueError:
        return render_template('lab4/fridge.html', error='Ошибка: температура должна быть числом')
    
    if temp < -12:
        return render_template('lab4/fridge.html', error='Не удалось установить температуру — слишком низкое значение')
    elif temp > -1:
        return render_template('lab4/fridge.html', error='Не удалось установить температуру — слишком высокое значение')
    elif -12 <= temp <= -9:
        snowflakes = 3
        message = f'Установлена температура: {temp}°С'
    elif -8 <= temp <= -5:
        snowflakes = 2
        message = f'Установлена температура: {temp}°С'
    elif -4 <= temp <= -1:
        snowflakes = 1
        message = f'Установлена температура: {temp}°С'
    else:
        snowflakes = 0
        message = f'Установлена температура: {temp}°С'
    
    return render_template('lab4/fridge.html', 
                         message=message, 
                         snowflakes=snowflakes, 
                         temperature=temp)


@lab4.route('/lab4/grain_order', methods=['GET', 'POST'])
def grain_order():
    if request.method == 'GET':
        return render_template('lab4/grain_order.html')
    
    grain_type = request.form.get('grain_type')
    weight = request.form.get('weight')
    
    if not grain_type:
        return render_template('lab4/grain_order.html', error='Выберите тип зерна')
    
    if not weight:
        return render_template('lab4/grain_order.html', error='Укажите вес заказа')
    
    try:
        weight = float(weight)
    except ValueError:
        return render_template('lab4/grain_order.html', error='Вес должен быть числом')
    
    if weight <= 0:
        return render_template('lab4/grain_order.html', error='Вес должен быть больше 0')
    
    if weight > 100:
        return render_template('lab4/grain_order.html', error='Такого объёма сейчас нет в наличии')
    
    prices = {
        'barley': 12000,  
        'oats': 8500,     
        'wheat': 9000,   
        'rye': 15000     
    }
    
    grain_names = {
        'barley': 'ячмень',
        'oats': 'овёс', 
        'wheat': 'пшеница',
        'rye': 'рожь'
    }
    
    price_per_ton = prices[grain_type]
    total_cost = weight * price_per_ton
    
    discount = 0
    if weight > 10:
        discount = total_cost * 0.10  
        total_cost -= discount
    
    return render_template('lab4/grain_order.html',
                         success=True,
                         grain_name=grain_names[grain_type],
                         weight=weight,
                         total_cost=total_cost,
                         discount=discount,
                         selected_grain=grain_type)


@lab4.route('/lab4/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab4/register.html')
    
    login = request.form.get('login')
    password = request.form.get('password')
    password_confirm = request.form.get('password_confirm')
    name = request.form.get('name')
    
    if not login or not password or not name:
        return render_template('lab4/register.html', error='Все поля обязательны для заполнения')
    
    if password != password_confirm:
        return render_template('lab4/register.html', error='Пароли не совпадают')
    
    for user in users:
        if user['login'] == login:
            return render_template('lab4/register.html', error='Пользователь с таким логином уже существует')
    
    new_user = {
        'login': login,
        'password': password,
        'name': name,
        'gender': request.form.get('gender', 'male')
    }
    users.append(new_user)
    
    return render_template('lab4/register.html', success='Регистрация прошла успешно! Теперь вы можете войти.')


@lab4.route('/lab4/users')
def users_list():
    if 'login' not in session:
        return redirect('/lab4/login')
    
    users_safe = []
    for user in users:
        user_safe = {
            'login': user['login'],
            'name': user['name'],
            'gender': user['gender'],
            'is_current': (user['login'] == session['login'])
        }
        users_safe.append(user_safe)
    
    return render_template('lab4/users.html', users=users_safe, current_user=session['login'])


@lab4.route('/lab4/users/delete', methods=['POST'])
def delete_user():
    if 'login' not in session:
        return redirect('/lab4/login')
    
    login_to_delete = request.form.get('login')
    
    if login_to_delete != session['login']:
        return redirect('/lab4/users')
    
    global users
    users = [user for user in users if user['login'] != login_to_delete]
    
    session.pop('login', None)
    session.pop('name', None)
    
    return redirect('/lab4/login')


@lab4.route('/lab4/users/edit', methods=['GET', 'POST'])
def edit_user():
    if 'login' not in session:
        return redirect('/lab4/login')
    
    current_login = session['login']
    
    if request.method == 'GET':
        current_user = None
        for user in users:
            if user['login'] == current_login:
                current_user = user
                break
        
        if not current_user:
            return redirect('/lab4/login')
        
        user_safe = {
            'login': current_user['login'],
            'name': current_user['name'],
            'gender': current_user['gender']
        }
        
        return render_template('lab4/edit_user.html', user=user_safe)
    
    new_login = request.form.get('login')
    new_name = request.form.get('name')
    new_password = request.form.get('password')
    password_confirm = request.form.get('password_confirm')
    gender = request.form.get('gender', 'male')
    
    if not new_login or not new_name:
        current_user = next((user for user in users if user['login'] == current_login), None)
        user_safe = {
            'login': current_user['login'],
            'name': current_user['name'],
            'gender': current_user['gender']
        } if current_user else {}
        return render_template('lab4/edit_user.html', user=user_safe, error='Логин и имя обязательны для заполнения')
    
    if new_login != current_login:
        for user in users:
            if user['login'] == new_login:
                current_user = next((user for user in users if user['login'] == current_login), None)
                user_safe = {
                    'login': current_user['login'],
                    'name': current_user['name'],
                    'gender': current_user['gender']
                } if current_user else {}
                return render_template('lab4/edit_user.html', user=user_safe, error='Пользователь с таким логином уже существует')
    
    if new_password:
        if new_password != password_confirm:
            current_user = next((user for user in users if user['login'] == current_login), None)
            user_safe = {
                'login': current_user['login'],
                'name': current_user['name'],
                'gender': current_user['gender']
            } if current_user else {}
            return render_template('lab4/edit_user.html', user=user_safe, error='Пароли не совпадают')
    
    for user in users:
        if user['login'] == current_login:
            user['login'] = new_login
            user['name'] = new_name
            user['gender'] = gender
            if new_password:
                user['password'] = new_password
            break
    
    session['login'] = new_login
    session['name'] = new_name
    
    return redirect('/lab4/users')
