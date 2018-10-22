from flask import Blueprint, render_template, request, redirect, session

from ..utils.md5 import md5
from ..utils import sql_exe

ac = Blueprint('ac', __name__)


@ac.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    username = request.form.get('user')
    password = request.form.get('pwd')

    pwd_md5 = md5(password)

    data = sql_exe.fetch_one("select id,nickname from userinfo where user=%s and pwd=%s", (username, pwd_md5))
    if not data:
        return render_template('login.html', error='用户名密码错误')
    session['user_info'] = data
    return redirect('/index')


@ac.route('/logout')
def logout():
    if 'user_info' in session:
        del session['user_info']
    return redirect('/login')
