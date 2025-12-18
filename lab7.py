from flask import Blueprint, render_template, request, abort, redirect, current_app
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path

lab7 = Blueprint('lab7', __name__)

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

@lab7.route('/lab7/')
def main():
    return render_template('lab7/lab7.html')


def validate_film(film_data):
    errors = {}
    
    title_ru = film_data.get('title_ru', '').strip()
    if not title_ru:
        errors['title_ru'] = 'Русское название обязательно для заполнения'
    
    title = film_data.get('title', '').strip()
    if not title and not title_ru:
        errors['title'] = 'Хотя бы одно название должно быть заполнено'
    
    try:
        year = int(film_data.get('year', 0))
        current_year = datetime.now().year
        if year < 1895:
            errors['year'] = f'Год не может быть раньше 1895 (год создания первого фильма)'
        elif year > current_year:
            errors['year'] = f'Год не может быть больше {current_year} (текущего года)'
    except (ValueError, TypeError):
        errors['year'] = 'Год должен быть числом'
    
    description = film_data.get('description', '').strip()
    if not description:
        errors['description'] = 'Описание обязательно для заполнения'
    elif len(description) > 2000:
        errors['description'] = f'Описание слишком длинное ({len(description)} символов). Максимум 2000 символов'
    
    return errors


@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    conn, cur = db_connect()
    
    try:
        cur.execute("SELECT id, title, title_ru, year, description FROM films ORDER BY id")
        films_data = cur.fetchall()
        
        films_list = []
        for film in films_data:
            films_list.append({
                'id': film['id'],
                'title': film['title'],
                'title_ru': film['title_ru'],
                'year': film['year'],
                'description': film['description']
            })
        
        return films_list
    finally:
        db_close(conn, cur)


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    conn, cur = db_connect()
    
    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT id, title, title_ru, year, description FROM films WHERE id = %s", (id,))
        else:
            cur.execute("SELECT id, title, title_ru, year, description FROM films WHERE id = ?", (id,))
        
        film = cur.fetchone()
        
        if not film:
            abort(404)
        
        return {
            'id': film['id'],
            'title': film['title'],
            'title_ru': film['title_ru'],
            'year': film['year'],
            'description': film['description']
        }
    finally:
        db_close(conn, cur)


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    conn, cur = db_connect()
    
    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT id FROM films WHERE id = %s", (id,))
        else:
            cur.execute("SELECT id FROM films WHERE id = ?", (id,))
        
        film = cur.fetchone()
        
        if not film:
            abort(404)
        
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("DELETE FROM films WHERE id = %s", (id,))
        else:
            cur.execute("DELETE FROM films WHERE id = ?", (id,))
        
        conn.commit()
        return '', 204
    finally:
        db_close(conn, cur)


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    conn, cur = db_connect()
    
    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT id FROM films WHERE id = %s", (id,))
        else:
            cur.execute("SELECT id FROM films WHERE id = ?", (id,))
        
        film_exists = cur.fetchone()
        
        if not film_exists:
            response = redirect('/lab1/404')
            response.status_code = 404 
            return response

        film = request.get_json()
        
        if not film.get('title', '').strip() and film.get('title_ru', '').strip():
            film['title'] = film['title_ru']
        
        errors = validate_film(film)
        if errors:
            return errors, 400
        
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("""
                UPDATE films 
                SET title = %s, title_ru = %s, year = %s, description = %s 
                WHERE id = %s
            """, (film['title'], film['title_ru'], film['year'], film['description'], id))
        else:
            cur.execute("""
                UPDATE films 
                SET title = ?, title_ru = ?, year = ?, description = ? 
                WHERE id = ?
            """, (film['title'], film['title_ru'], film['year'], film['description'], id))
        
        conn.commit()
        
        return {
            'title': film['title'],
            'title_ru': film['title_ru'],
            'year': film['year'],
            'description': film['description']
        }
    finally:
        db_close(conn, cur)


@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    conn, cur = db_connect()
    
    try:
        film = request.get_json()
        
        if not film.get('title', '').strip() and film.get('title_ru', '').strip():
            film['title'] = film['title_ru']
        
        errors = validate_film(film)
        if errors:
            return errors, 400
        
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("""
                INSERT INTO films (title, title_ru, year, description) 
                VALUES (%s, %s, %s, %s) 
                RETURNING id
            """, (film['title'], film['title_ru'], film['year'], film['description']))
            
            new_id = cur.fetchone()['id']
        else:
            cur.execute("""
                INSERT INTO films (title, title_ru, year, description) 
                VALUES (?, ?, ?, ?)
            """, (film['title'], film['title_ru'], film['year'], film['description']))
            
            new_id = cur.lastrowid
        
        conn.commit()
        
        return {"id": new_id}
    finally:
        db_close(conn, cur)
