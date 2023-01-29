'''Главный модуль приложения
'''
# TODO улучшение авторизации https://youtu.be/L_o0wRaZJdg?list=PLA0M1Bcd0w8yrxtwgqBvT6OM4HkOU3xYn
import sqlite3
import os
from flask import Flask, render_template, url_for, request,\
                    flash, redirect, session, abort, g
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import config # Импортируем настройки из отдельного файла
from f_data_base import FDataBase
from UserLogin import UserLogin


app = Flask(__name__)
app.config.from_object(config)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'site.db')))


login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Страница доступна только для авторизованных пользователей'
login_manager.login_message_category = 'success'


@login_manager.user_loader
def load_user(user_id):
    '''функция получает данные о пользователе по его id в базе данных'''
    print("load_user")
    return UserLogin().fromDB(user_id, d_base)

def connect_db():
    '''функция создает соединение с базой данных'''
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory=sqlite3.Row
    return conn


def create_db():
    '''Функция создает базу данных'''
    data_base = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f_sql:
        data_base.cursor().executescript(f_sql.read())
    data_base.commit()
    data_base.close()


def get_db():
    '''Функция устанавливает соединение с базой данных,
     если оно еще не установлено'''
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


d_base = None


@app.before_request
def before_request():
    '''Устанавливаем соединение с БД перед выполнением запроса'''
    global d_base
    db = get_db()
    d_base = FDataBase(db)


@app.teardown_appcontext
def close_db(error):
    '''Функция закрывает соединение с БД, если оно было установлено'''
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route('/')
def index():
    '''Обработчик главной страницы'''
    return render_template('index.html', menu=d_base.get_menu(), posts = d_base.get_post_anons())

@app.route('/add_post', methods=['POST', 'GET'])
@login_required
def add_post():
    '''Обработчик добавления новой статьи в базу данных'''
    if request.method == 'POST':
        if len(request.form['name']) > 4 and len(request.form['post']) > 10:
            res = d_base.add_post(request.form['name'], request.form['url'], request.form['post'])
            if not res:
                flash('Ошибка добавления статьи', category='error')
            else:
                flash('Статья успешно добавлена', category='success')
        else:
            flash('Ошибка добавления статьи', category='error')
    return render_template('add_post.html', menu=d_base.get_menu(), title='Добавление статьи')


@app.route('/post/<alias>')
@login_required
def show_post(alias):
    '''Обработчик отдельной выбранной статьи'''
    title, post = d_base.get_post(alias)
    if not title:
        abort(404)
    return render_template('post.html', menu=d_base.get_menu(), title=title, post=post)


@app.route('/logout')
@login_required
def logout():
    '''Обработчик обеспечивает выход из аккаунта для авторизованного пользователя'''
    logout_user()
    flash("Вы вышли из аккаунта", "success")
    return redirect(url_for('login'))

@app.route('/profile')
@login_required
def profile():
    '''Обработчик для страницы профайла пользователя'''
    return f"""<h2><a href="{url_for('logout')}">Выйти из профиля</a></h2>
            <p>Информация о пользователе. ID:{current_user.get_id()}</p>"""


@app.route('/login', methods=['POST', 'GET'])
def login():
    '''Обработчик формы Логин'''
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    if request.method == "POST":
        user = d_base.get_user_by_email(request.form['email'])
        if user and check_password_hash(user['psw'], request.form['psw']):
            user_login = UserLogin().create(user)
            remember_me = True if request.form.get('remainme') else False
            login_user(user_login, remember = remember_me)
            return redirect(request.args.get('next') or url_for('profile'))
        flash("Неверная пара логин/пароль", "error")
    return render_template('login.html', title='Авторизация', menu=d_base.get_menu())


@app.route('/register', methods=['POST', 'GET'])
def register():
    '''Обработчик формы регистрации пользователя'''
    if request.method == "POST":
        if len(request.form['name']) > 4 and len(request.form['email']) > 4 \
            and len(request.form['psw']) > 4 and request.form['psw2'] ==  request.form['psw']:

            psw_hash = generate_password_hash(request.form['psw'])
            res = d_base.add_user(request.form['name'], request.form['email'], psw_hash)
            if res:
                flash("Вы успешно зарегистрированы", "success")
                return redirect(url_for('login'))
            else:
                flash("Ошибка при добавлении в базу данных", "error")
        else:
            flash("Неверно заполнены поля формы", "error")
    return render_template('register.html', title='Регистрация', menu=d_base.get_menu())


@app.errorhandler(404)
def page_not_found(error):
    '''Обработчик ошибки открытия несуществующей страницы'''
    return render_template('page404.html', title='Страница не найдена',
                                            menu=d_base.get_menu()), 404


#Тестовый контекст для проверки
# with app.test_request_context():
#     print(url_for('index'))
#     print(url_for('about'))
#     print(url_for('contact'))


if __name__ == '__main__':
    app.run(debug=True)
