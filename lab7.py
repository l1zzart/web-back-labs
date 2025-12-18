from flask import Blueprint, render_template, request, abort, redirect
from datetime import datetime

lab7 = Blueprint('lab7', __name__)

@lab7.route('/lab7/')
def main():
    return render_template('lab7/lab7.html')


films = [
    {
        "title": "Вертикаль",
        "title_ru": "Вертикаль",
        "year": 1966,
        "description": "Группе альпинистов, идущих на штурм непокоренной кавказской вершины, пика Ор-Тау, "
        "послан сигнал о немедленном возвращении: надвигается грозовой циклон. Связист скрывает от товарищей это предупреждение, и они оказываются в критической ситуации. "
        "Трагедии удается избежать только благодаря мужеству спасателей и опыту самих спортсменов..."
    },
    {
        "title": "Requiem for a Dream",
        "title_ru": "Реквием по мечте",
        "year": 2000,
        "description": "Каждый стремится к своей заветной мечте. Сара Голдфарб мечтала сняться в известном телешоу, "
        "ее сын Гарольд с другом Тайроном — сказочно разбогатеть, подруга Гарольда Мэрион грезила о собственном модном магазине, "
        "но на их пути были всевозможные препятствия. Все они выбирают неочевидные пути достижения своих целей, "
        "и мечты по-прежнему остаются недостижимыми, а жизни героев рушатся безвозвратно."
    },
    {
        "title": "Spider-Man: Into the Spider-Verse",
        "title_ru": "Человек-паук:Через вселенные",
        "year": 2018,
        "description": "Мы всё знаем о Питере Паркере. Он спас город, влюбился, а потом спасал город снова и снова… "
        "Но все это – в нашем измерении. А что если в результате работы гигантского коллайдера откроется окно из одного измерения в другое? "
        "Найдется ли в нем свой Человек-паук? И как он будет выглядеть? Приготовьтесь к тому, что в разных вселенных могут быть разные Люди-пауки "
        "и однажды им придется собраться вместе для борьбы с почти непобедимым врагом."
    },
    {
        "title": "The Devil Wears Prada",
        "title_ru": "Дьявол носит Prada",
        "year": 2006,
        "description": "Мечтающая стать журналисткой провинциальная девушка Энди по окончании университета"
        "получает должность помощницы всесильной Миранды Пристли, деспотичного редактора одного из крупнейших нью-йоркских журналов мод."
        "Энди всегда мечтала о такой работе, не зная, с каким нервным напряжением это будет связано…"
    },
    {
        "title": "Shutter Island",
        "title_ru": "Остров проклятых",
        "year": 2009,
        "description": "Два американских судебных пристава отправляются на один из островов в штате Массачусетс, "
        "чтобы расследовать исчезновение пациентки клиники для умалишенных преступников. При проведении расследования им придется "
        "столкнуться с паутиной лжи, обрушившимся ураганом и смертельным бунтом обитателей клиники."
    }
]


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
    return films


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    if id < 0 or id >= len(films):
        abort(404)  
    
    return films[id]


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    if id < 0 or id >= len(films):
        abort(404)

    del films[id]
    return '', 204


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    if id < 0 or id >= len(films):
        response = redirect('/lab1/404')
        response.status_code = 404 
        return response

    film = request.get_json()
    
    if not film.get('title', '').strip() and film.get('title_ru', '').strip():
        film['title'] = film['title_ru']
    
    errors = validate_film(film)
    if errors:
        return errors, 400
    
    films[id] = film
    return films[id]


@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json()
    
    if not film.get('title', '').strip() and film.get('title_ru', '').strip():
        film['title'] = film['title_ru']
    
    errors = validate_film(film)
    if errors:
        return errors, 400

    films.append(film)
    return {"id": len(films) - 1}
