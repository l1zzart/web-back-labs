from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from db.models import users, articles

lab8 = Blueprint('lab8', __name__)

@lab8.route('/lab8/')
def main():
    return render_template('lab8/lab8.html')


@lab8.route('/lab8/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')

    if not login_form or login_form.strip() == '':
        return render_template('lab8/register.html',
                            error='Имя пользователя не может быть пустым')
    
    if not password_form or password_form.strip() == '':
        return render_template('lab8/register.html',
                            error='Пароль не может быть пустым')

    login_exists = users.query.filter_by(login=login_form).first()
    if login_exists:
        return render_template('lab8/register.html',
                            error='Такой пользователь уже существует')

    password_hash = generate_password_hash(password_form)
    new_user = users(login=login_form, password=password_hash)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/lab8/')


@lab8.route('/lab8/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')

    if not login_form or login_form.strip() == '':
        return render_template('lab8/login.html',
                            error='Логин не может быть пустым')
    
    if not password_form or password_form.strip() == '':
        return render_template('lab8/login.html',
                            error='Пароль не может быть пустым')

    user = users.query.filter_by(login=login_form).first()

    if user:
        if check_password_hash(user.password, password_form):
            login_user(user, remember = False)
            return redirect('/lab8/')

    return render_template('lab8/login.html',
                        error='Ошибка входа: логин и/или пароль неверны')


@lab8.route('/lab8/articles/')
@login_required
def article_list():
    show_public = request.args.get('public') == 'true'
    
    if show_public:
        articles_list = articles.query.filter_by(is_public=True).order_by(articles.created_at.desc()).all()
    else:
        articles_list = articles.query.filter_by(login_id=current_user.id).order_by(articles.created_at.desc()).all()
    
    return render_template('lab8/articles.html', 
                         articles=articles_list,
                         show_public=show_public)


@lab8.route('/lab8/logout')
@login_required
def logout():
    logout_user()
    return redirect('/lab8/')


@lab8.route('/lab8/create', methods=['GET', 'POST'])
@login_required
def create_article():
    if request.method == 'GET':
        return render_template('lab8/create.html')
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_public = True if request.form.get('is_public') else False
    is_favorite = True if request.form.get('is_favorite') else False
    
    if not title or not article_text:
        return render_template('lab8/create.html',
                            error='Заголовок и текст статьи обязательны')
    
    new_article = articles(
        login_id=current_user.id,
        title=title,
        article_text=article_text,
        is_public=is_public,
        is_favorite=is_favorite,
        likes=0
    )
    
    db.session.add(new_article)
    db.session.commit()
    
    return redirect('/lab8/articles')


@lab8.route('/lab8/edit/<int:article_id>', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    article = articles.query.get_or_404(article_id)
    
    if article.login_id != current_user.id:
        return "У вас нет прав для редактирования этой статьи", 403
    
    if request.method == 'GET':
        return render_template('lab8/edit.html', article=article)
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_public = True if request.form.get('is_public') else False
    is_favorite = True if request.form.get('is_favorite') else False
    
    if not title or not article_text:
        return render_template('lab8/edit.html',
                             article=article,
                             error='Заголовок и текст статьи обязательны')
    
    article.title = title
    article.article_text = article_text
    article.is_public = is_public
    article.is_favorite = is_favorite
    
    db.session.commit()
    
    return redirect('/lab8/articles')


@lab8.route('/lab8/delete/<int:article_id>')
@login_required
def delete_article(article_id):
    article = articles.query.get_or_404(article_id)
    
    if article.login_id != current_user.id:
        return "У вас нет прав для удаления этой статьи", 403
    
    db.session.delete(article)
    db.session.commit()
    
    return redirect('/lab8/articles')
