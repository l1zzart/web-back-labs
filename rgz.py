from flask import Blueprint, render_template, request, session, redirect, url_for, flash, g
import sqlite3
from os import path
from werkzeug.security import generate_password_hash, check_password_hash
import re

rgz = Blueprint('rgz', __name__)

STUDENT_NAME = "Артемченко Елизавета Сергеевна"
STUDENT_GROUP = "ФБИ-33"

def get_db_path():
    dir_path = path.dirname(path.realpath(__file__))
    return path.join(dir_path, "rgz.db")

def db_connect():
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  
    return conn

def db_close(conn):
    conn.close()

def init_db():
    conn = db_connect()
    cur = conn.cursor()
    
    # Пользователи
    cur.execute('''
        CREATE TABLE IF NOT EXISTS rgz_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Товары (30 позиций)
    cur.execute('''
        CREATE TABLE IF NOT EXISTS rgz_products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL CHECK(price > 0),
            category TEXT,
            stock INTEGER DEFAULT 0 CHECK(stock >= 0)
        )
    ''')
    
    # Корзина
    cur.execute('''
        CREATE TABLE IF NOT EXISTS rgz_cart (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER DEFAULT 1,
            FOREIGN KEY (user_id) REFERENCES rgz_users(id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES rgz_products(id) ON DELETE CASCADE
        )
    ''')
    
    # Заказы
    cur.execute('''
        CREATE TABLE IF NOT EXISTS rgz_orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            total_amount REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES rgz_users(id) ON DELETE CASCADE
        )
    ''')
    
    # Товары в заказе
    cur.execute('''
        CREATE TABLE IF NOT EXISTS rgz_order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            FOREIGN KEY (order_id) REFERENCES rgz_orders(id) ON DELETE CASCADE
        )
    ''')
    
    # 30 товароd
    cur.execute("SELECT COUNT(*) as count FROM rgz_products")
    if cur.fetchone()['count'] == 0:
        products = [
            ('Диван "Модерн"', 29999.99, 'Диваны', 10),
            ('Кресло офисное', 15999.99, 'Кресла', 20),
            ('Стол обеденный', 18999.99, 'Столы', 12),
            ('Стул "Икеа"', 2999.99, 'Стулья', 50),
            ('Шкаф-купе', 69999.99, 'Шкафы', 4),
            ('Кровать двуспальная', 38999.99, 'Кровати', 6),
            ('Комод 4-х ящичный', 12999.99, 'Комоды', 22),
            ('Тумба прикроватная', 4999.99, 'Тумбы', 35),
            ('Полка настенная', 6999.99, 'Полки', 42),
            ('Люстра "Хрусталь"', 28999.99, 'Светильники', 14),
            ('Диван угловой', 45999.99, 'Диваны', 5),
            ('Кресло-качалка', 12999.99, 'Кресла', 8),
            ('Стол журнальный', 8999.99, 'Столы', 25),
            ('Стул барный', 4999.99, 'Стулья', 30),
            ('Шкаф книжный', 28999.99, 'Шкафы', 9),
            ('Кровать односпальная', 15999.99, 'Кровати', 18),
            ('Комод с зеркалом', 21999.99, 'Комоды', 8),
            ('Тумба ТВ', 17999.99, 'Тумбы', 13),
            ('Полка книжная', 12999.99, 'Полки', 19),
            ('Торшер', 14999.99, 'Светильники', 27),
            ('Диван-кровать', 22999.99, 'Диваны', 15),
            ('Кресло кожаное', 34999.99, 'Кресла', 3),
            ('Стол компьютерный', 24999.99, 'Столы', 7),
            ('Стул детский', 1999.99, 'Стулья', 40),
            ('Шкаф-гардероб', 17999.99, 'Шкафы', 15),
            ('Кровать детская', 24999.99, 'Кровати', 11),
            ('Комод узкий', 9999.99, 'Комоды', 17),
            ('Тумба обувная', 8999.99, 'Тумбы', 26),
            ('Полка угловая', 3999.99, 'Полки', 31),
            ('Настольная лампа', 5999.99, 'Светильники', 38),
        ]
        
        for name, price, category, stock in products:
            cur.execute('''
                INSERT INTO rgz_products (name, price, category, stock)
                VALUES (?, ?, ?, ?)
            ''', (name, price, category, stock))
    
    # Тестовый пользователь
    cur.execute("SELECT COUNT(*) as count FROM rgz_users WHERE username = 'test_user'")
    if cur.fetchone()['count'] == 0:
        password_hash = generate_password_hash('test123')
        cur.execute('''
            INSERT INTO rgz_users (username, password_hash)
            VALUES (?, ?)
        ''', ('test_user', password_hash))
    
    conn.commit()
    db_close(conn)

def validate_username(username):
    pattern = r'^[A-Za-z0-9!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>\/?]*$'
    return bool(re.match(pattern, username)) and len(username) >= 3

def get_current_user():
    if 'rgz_user_id' in session:
        conn = db_connect()
        cur = conn.cursor()
        cur.execute("SELECT * FROM rgz_users WHERE id = ?", (session['rgz_user_id'],))
        user = cur.fetchone()
        db_close(conn)
        return user
    return None

@rgz.route('/')
def index():
    init_db()
    user = get_current_user()
    
    conn = db_connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM rgz_products ORDER BY name")
    products = cur.fetchall()
    db_close(conn)
    
    return render_template('rgz/index.html',
                         products=products,
                         user=user,
                         student_name=STUDENT_NAME,
                         student_group=STUDENT_GROUP)

@rgz.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('rgz/register.html',
                             student_name=STUDENT_NAME,
                             student_group=STUDENT_GROUP)
    
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')
    password_confirm = request.form.get('password_confirm', '')
    
    errors = []
    if not username:
        errors.append('Введите логин')
    elif not validate_username(username):
        errors.append('Логин должен содержать только латинские буквы, цифры и знаки препинания')
    
    if not password:
        errors.append('Введите пароль')
    elif len(password) < 6:
        errors.append('Пароль должен быть не менее 6 символов')
    elif password != password_confirm:
        errors.append('Пароли не совпадают')
    
    if errors:
        return render_template('rgz/register.html',
                             errors=errors,
                             username=username,
                             student_name=STUDENT_NAME,
                             student_group=STUDENT_GROUP)
    
    conn = db_connect()
    cur = conn.cursor()
    cur.execute("SELECT id FROM rgz_users WHERE username = ?", (username,))
    if cur.fetchone():
        db_close(conn)
        errors.append('Пользователь с таким логином уже существует')
        return render_template('rgz/register.html',
                             errors=errors,
                             username=username,
                             student_name=STUDENT_NAME,
                             student_group=STUDENT_GROUP)
    
    password_hash = generate_password_hash(password)
    cur.execute('''
        INSERT INTO rgz_users (username, password_hash)
        VALUES (?, ?)
    ''', (username, password_hash))
    
    conn.commit()
    db_close(conn)
    
    conn = db_connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM rgz_users WHERE username = ?", (username,))
    new_user = cur.fetchone()
    db_close(conn)
    
    if new_user:
        session['rgz_user_id'] = new_user['id']
        session['rgz_username'] = new_user['username']
        flash('Регистрация и вход выполнены успешно!', 'success')
        return redirect(url_for('rgz.index'))
    else:
        flash('Регистрация успешна! Теперь войдите.', 'success')
        return redirect(url_for('rgz.login'))

@rgz.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('rgz/login.html',
                             student_name=STUDENT_NAME,
                             student_group=STUDENT_GROUP)
    
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')
    
    conn = db_connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM rgz_users WHERE username = ?", (username,))
    user = cur.fetchone()
    db_close(conn)
    
    if not user or not check_password_hash(user['password_hash'], password):
        return render_template('rgz/login.html',
                             error='Неверный логин или пароль',
                             username=username,
                             student_name=STUDENT_NAME,
                             student_group=STUDENT_GROUP)
    
    session['rgz_user_id'] = user['id']
    session['rgz_username'] = user['username']
    
    flash('Вход выполнен успешно!', 'success')
    return redirect(url_for('rgz.index'))

@rgz.route('/logout')
def logout():
    session.pop('rgz_user_id', None)
    session.pop('rgz_username', None)
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('rgz.index'))

@rgz.route('/cart')
def cart():
    user = get_current_user()
    if not user:
        flash('Для доступа к корзине необходимо авторизоваться', 'warning')
        return redirect(url_for('rgz.login'))
    
    conn = db_connect()
    cur = conn.cursor()
    
    # Получение товаров из корзины
    cur.execute('''
        SELECT c.*, p.name, p.price 
        FROM rgz_cart c
        JOIN rgz_products p ON c.product_id = p.id
        WHERE c.user_id = ?
    ''', (user['id'],))
    cart_items = cur.fetchall()
    
    total = sum(item['price'] * item['quantity'] for item in cart_items)
    
    # Получение последних заказов для истории
    cur.execute('''
        SELECT * FROM rgz_orders 
        WHERE user_id = ? 
        ORDER BY created_at DESC
        LIMIT 3
    ''', (user['id'],))
    orders = cur.fetchall()
    
    db_close(conn)
    
    return render_template('rgz/cart.html',
                         cart_items=cart_items,
                         total=total,
                         orders=orders,
                         user=user,
                         student_name=STUDENT_NAME,
                         student_group=STUDENT_GROUP)

@rgz.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    user = get_current_user()
    if not user:
        flash('Для добавления в корзину необходимо авторизоваться', 'warning')
        return redirect(url_for('rgz.login'))
    
    conn = db_connect()
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM rgz_products WHERE id = ?", (product_id,))
    product = cur.fetchone()
    
    if not product:
        db_close(conn)
        flash('Товар не найден', 'danger')
        return redirect(url_for('rgz.index'))
    
    if product['stock'] <= 0:
        db_close(conn)
        flash('Товар временно отсутствует', 'danger')
        return redirect(url_for('rgz.index'))
    
    # Проверка есть ли уже в корзине
    cur.execute('''
        SELECT * FROM rgz_cart 
        WHERE user_id = ? AND product_id = ?
    ''', (user['id'], product_id))
    
    existing_item = cur.fetchone()
    
    if existing_item:
        cur.execute('''
            UPDATE rgz_cart 
            SET quantity = quantity + 1 
            WHERE id = ?
        ''', (existing_item['id'],))
    else:
        cur.execute('''
            INSERT INTO rgz_cart (user_id, product_id, quantity)
            VALUES (?, ?, 1)
        ''', (user['id'], product_id))
    
    conn.commit()
    db_close(conn)
    
    flash(f'Товар "{product["name"]}" добавлен в корзину', 'success')
    return redirect(url_for('rgz.index'))

@rgz.route('/update_cart/<int:cart_id>', methods=['POST'])
def update_cart(cart_id):
    user = get_current_user()
    if not user:
        return redirect(url_for('rgz.login'))
    
    action = request.form.get('action')
    
    conn = db_connect()
    cur = conn.cursor()
    
    cur.execute('''
        SELECT * FROM rgz_cart 
        WHERE id = ? AND user_id = ?
    ''', (cart_id, user['id']))
    
    cart_item = cur.fetchone()
    
    if not cart_item:
        db_close(conn)
        flash('Товар не найден в корзине', 'danger')
        return redirect(url_for('rgz.cart'))
    
    if action == 'increase':
        cur.execute('''
            UPDATE rgz_cart 
            SET quantity = quantity + 1 
            WHERE id = ?
        ''', (cart_id,))
    elif action == 'decrease':
        if cart_item['quantity'] > 1:
            cur.execute('''
                UPDATE rgz_cart 
                SET quantity = quantity - 1 
                WHERE id = ?
            ''', (cart_id,))
        else:
            cur.execute("DELETE FROM rgz_cart WHERE id = ?", (cart_id,))
    elif action == 'remove':
        cur.execute("DELETE FROM rgz_cart WHERE id = ?", (cart_id,))
    
    conn.commit()
    db_close(conn)
    
    return redirect(url_for('rgz.cart'))

@rgz.route('/checkout', methods=['POST'])
def checkout():
    user = get_current_user()
    if not user:
        return redirect(url_for('rgz.login'))
    
    conn = db_connect()
    cur = conn.cursor()
    
    try:
        # Получение товаров из корзины
        cur.execute('''
            SELECT c.*, p.name, p.price, p.stock 
            FROM rgz_cart c
            JOIN rgz_products p ON c.product_id = p.id
            WHERE c.user_id = ?
        ''', (user['id'],))
        
        cart_items = cur.fetchall()
        
        if not cart_items:
            db_close(conn)
            flash('Корзина пуста', 'warning')
            return redirect(url_for('rgz.cart'))
        
        # Проверка на наличие
        for item in cart_items:
            if item['stock'] < item['quantity']:
                raise Exception(f'Товара "{item["name"]}" недостаточно на складе')
        
        # Создание заказа
        total_amount = sum(item['price'] * item['quantity'] for item in cart_items)
        cur.execute('''
            INSERT INTO rgz_orders (user_id, total_amount)
            VALUES (?, ?)
        ''', (user['id'], total_amount))
        
        order_id = cur.lastrowid
        
        # Добавление товаров в заказ и обновление остатков
        for item in cart_items:
            cur.execute('''
                INSERT INTO rgz_order_items (order_id, product_id, quantity)
                VALUES (?, ?, ?)
            ''', (order_id, item['product_id'], item['quantity']))
            
            cur.execute('''
                UPDATE rgz_products 
                SET stock = stock - ? 
                WHERE id = ?
            ''', (item['quantity'], item['product_id']))
        
        # Очищение корзины
        cur.execute("DELETE FROM rgz_cart WHERE user_id = ?", (user['id'],))
        
        # Фиксирование транзакции
        conn.commit()
        db_close(conn)
        
        flash('Заказ успешно оформлен! Корзина очищена.', 'success')
        
    except Exception as e:
        # Откатываю транзакцию при ошибке
        conn.rollback()
        db_close(conn)
        flash(f'Ошибка при оформлении заказа: {str(e)}', 'danger')
        return redirect(url_for('rgz.cart'))
    
    return redirect(url_for('rgz.index'))

@rgz.route('/profile')
def profile():
    user = get_current_user()
    if not user:
        return redirect(url_for('rgz.login'))
    
    conn = db_connect()
    cur = conn.cursor()
    cur.execute('''
        SELECT * FROM rgz_orders 
        WHERE user_id = ? 
        ORDER BY created_at DESC
    ''', (user['id'],))
    orders = cur.fetchall()
    db_close(conn)
    
    return render_template('rgz/profile.html',
                         user=user,
                         orders=orders,
                         student_name=STUDENT_NAME,
                         student_group=STUDENT_GROUP)

@rgz.route('/delete_account', methods=['POST'])
def delete_account():
    user = get_current_user()
    if not user:
        return redirect(url_for('rgz.login'))
    
    password = request.form.get('password', '')
    
    if not check_password_hash(user['password_hash'], password):
        flash('Неверный пароль', 'danger')
        return redirect(url_for('rgz.profile'))
    
    conn = db_connect()
    cur = conn.cursor()
    
    try:
        cur.execute('BEGIN TRANSACTION')
        cur.execute("DELETE FROM rgz_users WHERE id = ?", (user['id'],))
        conn.commit()
        db_close(conn)
        
        session.clear()
        flash('Ваш аккаунт удален', 'info')
        
    except Exception as e:
        conn.rollback()
        db_close(conn)
        flash(f'Ошибка при удалении аккаунта: {str(e)}', 'danger')
    
    return redirect(url_for('rgz.index'))
