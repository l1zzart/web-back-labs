from flask import Blueprint, url_for, request, redirect, render_template
import datetime

lab8 = Blueprint('lab8', __name__)

@lab8.route('/lab8/')
def main():
    return render_template('lab8/lab8.html')
