from flask import Blueprint, render_template, session, jsonify, request, url_for
from flask_login import login_required, current_user
import random
import json

lab9 = Blueprint('lab9', __name__)

congratulations = [
    "С Новым Годом! Пусть предстоящий год будет полон радости и счастья!",
    "Желаю здоровья, удачи и исполнения всех желаний!",
    "Пусть новый год принесёт много улыбок и тепла!",
    "Желаю процветания, успехов во всех начинаниях!",
    "Пусть каждый день нового года будет ярким и интересным!",
    "Желаю любви, гармонии и семейного благополучия!",
    "Пусть сбудутся все самые заветные мечты!",
    "Желаем финансового благополучия и карьерного роста!",
    "Пусть новый год будет щедрым на добрые события!",
    "Желаю крепкого здоровья и бодрости духа!"
]

gifts = [
    "wow1.png",  
    "wow2.png",  
    "wow3.png",  
    "wow4.png",  
    "wow5.png",  
    "wow6.png",  
    "wow7.png",  
    "wow8.png", 
    "wow9.png",  
    "wow10.png"  
]

boxes = [
    "gif1.png",   
    "gif2.png",   
    "gif3.png",  
    "gif4.png",   
    "gif5.png",  
    "gif6.png",  
    "gif7.png",   
    "gif8.png",   
    "gif9.png",   
    "gif10.png"   
]

# Подарки только для авторизованных пользователей (последние 3)
PREMIUM_GIFT_IDS = [7, 8, 9]

def init_session():
    if 'lab9_opened_boxes' not in session:
        session['lab9_opened_boxes'] = []
    
    if 'lab9_boxes_positions' not in session:
        positions = []
        for i in range(10):
            positions.append({
                'top': random.randint(10, 70),
                'left': random.randint(5, 85)
            })
        session['lab9_boxes_positions'] = json.dumps(positions)

@lab9.route('/lab9/')
def main():
    init_session()
    
    opened_count = len(session.get('lab9_opened_boxes', []))
    remaining_count = 10 - opened_count
    positions = json.loads(session.get('lab9_boxes_positions', '[]'))
    opened_boxes = session.get('lab9_opened_boxes', [])
    
    is_authenticated = hasattr(current_user, 'is_authenticated') and current_user.is_authenticated
    
    return render_template('lab9/index.html',
                         opened_count=opened_count,
                         remaining_count=remaining_count,
                         positions=positions,
                         opened_boxes=opened_boxes,
                         boxes=boxes,
                         is_authenticated=is_authenticated)

@lab9.route('/lab9/open_box', methods=['POST'])
def open_box():
    init_session()
    
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': 'Некорректные данные'})
    
    try:
        box_id = int(data.get('box_id', -1))
        if box_id < 0 or box_id >= 10:
            raise ValueError
    except:
        return jsonify({'success': False, 'message': 'Некорректный ID коробки'})
    
    opened_boxes = session.get('lab9_opened_boxes', [])
    
    if len(opened_boxes) >= 3:
        return jsonify({
            'success': False,
            'message': 'Вы уже открыли максимальное количество коробок (3)!'
        })
    
    if box_id in opened_boxes:
        return jsonify({
            'success': False,
            'message': 'Эта коробка уже открыта!'
        })
    
    is_authenticated = hasattr(current_user, 'is_authenticated') and current_user.is_authenticated
    if box_id in PREMIUM_GIFT_IDS and not is_authenticated:
        return jsonify({
            'success': False,
            'message': 'Этот подарок только для авторизованных пользователей!'
        })
    
    opened_boxes.append(box_id)
    session['lab9_opened_boxes'] = opened_boxes
    
    congrat = congratulations[box_id]
    gift_url = url_for('static', filename=f'lab9/{gifts[box_id]}')
    
    opened_count = len(opened_boxes)
    remaining_count = 10 - opened_count
    
    return jsonify({
        'success': True,
        'congratulation': congrat,
        'gift_image': gift_url,
        'box_id': box_id,
        'opened_count': opened_count,
        'remaining_count': remaining_count,
        'message': f'Открыто коробок: {opened_count} из 3'
    })

@lab9.route('/lab9/reset', methods=['POST'])
@login_required
def reset_boxes():
    """Сброс всех коробок (только для авторизованных)"""
    init_session()
    
    session['lab9_opened_boxes'] = []
    
    positions = []
    for i in range(10):
        positions.append({
            'top': random.randint(10, 70),
            'left': random.randint(5, 85)
        })
    session['lab9_boxes_positions'] = json.dumps(positions)
    
    return jsonify({
        'success': True,
        'message': 'Дед Мороз наполнил все коробки заново!'
    })

@lab9.route('/lab9/state')
def get_state():
    init_session()
    
    opened_boxes = session.get('lab9_opened_boxes', [])
    opened_count = len(opened_boxes)
    remaining_count = 10 - opened_count
    
    is_authenticated = hasattr(current_user, 'is_authenticated') and current_user.is_authenticated
    
    return jsonify({
        'opened_count': opened_count,
        'remaining_count': remaining_count,
        'opened_boxes': opened_boxes,
        'is_authenticated': is_authenticated
    })
