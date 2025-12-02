from flask import Blueprint, render_template, request, session, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path

lab6 = Blueprint('lab6', __name__)

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

@lab6.route('/lab6/')
def lab():
    login = session.get('login', '')
    return render_template('lab6/lab6.html', current_user=login)

@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def api():
    data = request.json
    id = data['id']
    
    if data['method'] == 'info':
        conn, cur = db_connect()
        
        cur.execute("SELECT * FROM offices ORDER BY number;")
            
        offices_data = cur.fetchall()
        db_close(conn, cur)
        
        offices_list = []
        for office in offices_data:
            offices_list.append({
                'number': office['number'],
                'tenant': office['tenant'] if office['tenant'] else '',
                'price': office['price']
            })
        
        return {
            'jsonrpc': '2.0',
            'result': offices_list,
            'id': id
        }
    
    if data['method'] == 'getCurrentUser':
        login = session.get('login', '')
        return {
            'jsonrpc': '2.0',
            'result': login,
            'id': id
        }
    
    login = session.get('login')
    if not login:
        return {
            'jsonrpc': '2.0',
            'error': {
                'code': 1,
                'message': 'Unauthorized'
            },
            'id': id
        }
    
    if data['method'] == 'booking':
        office_number = data['params']
        conn, cur = db_connect()
        
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT tenant FROM offices WHERE number = %s;", (office_number,))
        else:
            cur.execute("SELECT tenant FROM offices WHERE number = ?;", (office_number,))
        
        office = cur.fetchone()
        
        if not office:
            db_close(conn, cur)
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 3,
                    'message': 'Office not found'
                },
                'id': id
            }
        
        if office['tenant']:
            db_close(conn, cur)
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 2,
                    'message': 'Already booked'
                },
                'id': id
            }
        
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("UPDATE offices SET tenant = %s WHERE number = %s;", (login, office_number))
        else:
            cur.execute("UPDATE offices SET tenant = ? WHERE number = ?;", (login, office_number))
        
        conn.commit()
        db_close(conn, cur)
        
        return {
            'jsonrpc': '2.0',
            'result': 'success',
            'id': id
        }
    
    if data['method'] == 'cancellation':
        office_number = data['params']
        conn, cur = db_connect()
        
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT tenant FROM offices WHERE number = %s;", (office_number,))
        else:
            cur.execute("SELECT tenant FROM offices WHERE number = ?;", (office_number,))
        
        office = cur.fetchone()
        
        if not office:
            db_close(conn, cur)
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 3,
                    'message': 'Office not found'
                },
                'id': id
            }
        
        if not office['tenant']:
            db_close(conn, cur)
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 4,
                    'message': 'Office is not booked'
                },
                'id': id
            }
        
        if office['tenant'] != login:
            db_close(conn, cur)
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 5,
                    'message': 'Cannot cancel someone else\'s booking'
                },
                'id': id
            }
        
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("UPDATE offices SET tenant = %s WHERE number = %s;", ('', office_number))
        else:
            cur.execute("UPDATE offices SET tenant = ? WHERE number = ?;", ('', office_number))
        
        conn.commit()
        db_close(conn, cur)
        
        return {
            'jsonrpc': '2.0',
            'result': 'success',
            'id': id
        }

    return {
        'jsonrpc': '2.0',
        'error': {
            'code': -32601,
            'message': 'Method not found'
        },
        'id': id
    }
