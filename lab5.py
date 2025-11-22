from flask import Blueprint, render_template, request, session, redirect, current_app, url_for
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path

lab5 = Blueprint('lab5', __name__)

@lab5.route('/lab5/')
def lab():
    login = session.get('login') 
    return render_template('lab5/lab5.html', login=login)

@lab5.route('/lab5/logout')
def logout():
    session.pop('login', None)
    return redirect('/lab5/')

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='elizaveta_artemchenko_knowledge_base',
            user='elizaveta_artemchenko_knowledge_base',
            password='695'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

    return conn, cur

def db_close(conn, cur):
    cur.close()
    conn.close()

@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')

    login = request.form.get('login')
    password = request.form.get('password')
    full_name = request.form.get('full_name', '').strip()

    if not login or not password:
        return render_template('lab5/register.html', error='Заполните логин и пароль')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login FROM users WHERE login=%s;", (login, ))
    else:
        cur.execute("SELECT login FROM users WHERE login=?;", (login, ))

    if cur.fetchone():
        db_close(conn, cur)
        return render_template('lab5/register.html', error="Такой пользователь уже существует")

    password_hash = generate_password_hash(password)
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO users (login, password, full_name) VALUES (%s, %s, %s);", 
                    (login, password_hash, full_name))
    else:
        cur.execute("INSERT INTO users (login, password, full_name) VALUES (?, ?, ?);", 
                    (login, password_hash, full_name))
    
    conn.commit()
    db_close(conn, cur)
    return render_template('lab5/success.html', login=login)

@lab5.route('/lab5/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not login or not password:
        return render_template('lab5/login.html', error="Заполните поля")

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login, ))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login, ))

    user = cur.fetchone()

    if not user:
        db_close(conn, cur)
        return render_template('lab5/login.html', error='Логин и/или пароль неверны')

    if not check_password_hash(user['password'], password):
        db_close(conn, cur)
        return render_template('lab5/login.html', error='Логин и/или пароль неверны')

    session['login'] = login
    db_close(conn, cur)
    return render_template('lab5/success_login.html', login=login)

@lab5.route('/lab5/create', methods=['GET', 'POST'])
def create():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    if request.method == 'GET':
        return render_template('lab5/create_article.html')
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_favorite = bool(request.form.get('is_favorite'))
    is_public = bool(request.form.get('is_public'))
    
    if not title or not article_text or not title.strip() or not article_text.strip():
        return render_template('lab5/create_article.html', 
                             error='Заполните название и текст статьи')
    
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login, ))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login, ))

    user = cur.fetchone()
    if not user:
        db_close(conn, cur)
        return redirect('/lab5/login')
    
    login_id = user["id"]

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("""
            INSERT INTO articles (login_id, title, article_text, is_favorite, is_public) 
            VALUES (%s, %s, %s, %s, %s)
        """, (login_id, title.strip(), article_text.strip(), is_favorite, is_public))
    else:
        cur.execute("""
            INSERT INTO articles (login_id, title, article_text, is_favorite, is_public) 
            VALUES (?, ?, ?, ?, ?)
        """, (login_id, title.strip(), article_text.strip(), is_favorite, is_public))
    
    conn.commit()
    db_close(conn, cur)
    return redirect('/lab5/list')

@lab5.route('/lab5/list')
def list_articles():
    login = session.get('login')
    
    conn, cur = db_connect()
    
    if login:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
        else:
            cur.execute("SELECT id FROM users WHERE login=?;", (login,))

        user = cur.fetchone()
        if user:
            login_id = user["id"]
            
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("""
                    SELECT a.*, u.login as author_login 
                    FROM articles a 
                    JOIN users u ON a.login_id = u.id 
                    WHERE a.login_id = %s OR a.is_public = true 
                    ORDER BY a.is_favorite DESC, a.id DESC;
                """, (login_id,))
            else:
                cur.execute("""
                    SELECT a.*, u.login as author_login 
                    FROM articles a 
                    JOIN users u ON a.login_id = u.id 
                    WHERE a.login_id = ? OR a.is_public = true 
                    ORDER BY a.is_favorite DESC, a.id DESC;
                """, (login_id,))
        else:
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("""
                    SELECT a.*, u.login as author_login 
                    FROM articles a 
                    JOIN users u ON a.login_id = u.id 
                    WHERE a.is_public = true 
                    ORDER BY a.is_favorite DESC, a.id DESC;
                """)
            else:
                cur.execute("""
                    SELECT a.*, u.login as author_login 
                    FROM articles a 
                    JOIN users u ON a.login_id = u.id 
                    WHERE a.is_public = true 
                    ORDER BY a.is_favorite DESC, a.id DESC;
                """)
    else:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("""
                SELECT a.*, u.login as author_login 
                FROM articles a 
                JOIN users u ON a.login_id = u.id 
                WHERE a.is_public = true 
                ORDER BY a.is_favorite DESC, a.id DESC;
            """)
        else:
            cur.execute("""
                SELECT a.*, u.login as author_login 
                FROM articles a 
                JOIN users u ON a.login_id = u.id 
                WHERE a.is_public = true 
                ORDER BY a.is_favorite DESC, a.id DESC;
            """)

    articles = cur.fetchall()
    db_close(conn, cur)
    
    return render_template('lab5/articles.html', articles=articles, login=login)

@lab5.route('/lab5/edit/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("""
            SELECT a.* FROM articles a 
            JOIN users u ON a.login_id = u.id 
            WHERE a.id = %s AND u.login = %s;
        """, (article_id, login))
    else:
        cur.execute("""
            SELECT a.* FROM articles a 
            JOIN users u ON a.login_id = u.id 
            WHERE a.id = ? AND u.login = ?;
        """, (article_id, login))
    
    article = cur.fetchone()
    
    if not article:
        db_close(conn, cur)
        return "Статья не найдена или у вас нет прав для редактирования", 404
    
    if request.method == 'GET':
        db_close(conn, cur)
        return render_template('lab5/edit_article.html', article=article)
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_favorite = bool(request.form.get('is_favorite'))
    is_public = bool(request.form.get('is_public'))
    
    if not title or not article_text or not title.strip() or not article_text.strip():
        db_close(conn, cur)
        return render_template('lab5/edit_article.html', 
                             article=article, 
                             error='Заполните название и текст статьи')
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("""
            UPDATE articles SET title = %s, article_text = %s, is_favorite = %s, is_public = %s
            WHERE id = %s;
        """, (title.strip(), article_text.strip(), is_favorite, is_public, article_id))
    else:
        cur.execute("""
            UPDATE articles SET title = ?, article_text = ?, is_favorite = ?, is_public = ?
            WHERE id = ?;
        """, (title.strip(), article_text.strip(), is_favorite, is_public, article_id))
    
    conn.commit()
    db_close(conn, cur)
    return redirect('/lab5/list')

@lab5.route('/lab5/delete/<int:article_id>')
def delete_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("""
            SELECT a.* FROM articles a 
            JOIN users u ON a.login_id = u.id 
            WHERE a.id = %s AND u.login = %s;
        """, (article_id, login))
    else:
        cur.execute("""
            SELECT a.* FROM articles a 
            JOIN users u ON a.login_id = u.id 
            WHERE a.id = ? AND u.login = ?;
        """, (article_id, login))
    
    article = cur.fetchone()
    
    if not article:
        db_close(conn, cur)
        return "Статья не найдена или у вас нет прав для удаления", 404
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("DELETE FROM articles WHERE id = %s;", (article_id,))
    else:
        cur.execute("DELETE FROM articles WHERE id = ?;", (article_id,))
    
    conn.commit()
    db_close(conn, cur)
    return redirect('/lab5/list')

@lab5.route('/lab5/users')
def users_list():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login, full_name FROM users ORDER BY login;")
    else:
        cur.execute("SELECT login, full_name FROM users ORDER BY login;")
    
    users = cur.fetchall()
    db_close(conn, cur)
    
    return render_template('lab5/users.html', users=users, login=login)

@lab5.route('/lab5/profile', methods=['GET', 'POST'])
def profile():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()
    
    if request.method == 'GET':
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT login, full_name FROM users WHERE login=%s;", (login,))
        else:
            cur.execute("SELECT login, full_name FROM users WHERE login=?;", (login,))
        
        user = cur.fetchone()
        db_close(conn, cur)
        return render_template('lab5/profile.html', user=user)
    
    new_full_name = request.form.get('full_name', '').strip()
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login,))
    
    user = cur.fetchone()
    
    errors = []
    
    if new_password:
        if not current_password:
            errors.append('Введите текущий пароль для смены пароля')
        elif not check_password_hash(user['password'], current_password):
            errors.append('Текущий пароль неверен')
        elif new_password != confirm_password:
            errors.append('Новый пароль и подтверждение не совпадают')
        elif len(new_password) < 3:
            errors.append('Новый пароль должен быть не менее 3 символов')
    
    if errors:
        db_close(conn, cur)
        return render_template('lab5/profile.html', user=user, errors=errors)
    
    if new_password:
        password_hash = generate_password_hash(new_password)
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("""
                UPDATE users SET full_name = %s, password = %s WHERE login = %s;
            """, (new_full_name, password_hash, login))
        else:
            cur.execute("""
                UPDATE users SET full_name = ?, password = ? WHERE login = ?;
            """, (new_full_name, password_hash, login))
    else:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("UPDATE users SET full_name = %s WHERE login = %s;", (new_full_name, login))
        else:
            cur.execute("UPDATE users SET full_name = ? WHERE login = ?;", (new_full_name, login))
    
    conn.commit()
    db_close(conn, cur)
    
    return redirect('/lab5/profile')
