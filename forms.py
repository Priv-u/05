'''Модуль содержит описания классов для форм приложения'''
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):
    '''Класс описывает структуру формы Login'''
    email = StringField("Email: ", validators=[Email("Некорректный email")])
    psw = PasswordField("Пароль: ", validators=[DataRequired(),
        Length(min=6, max=100, message="Пароль должен быть от 6 до 100 символов")])
    remember_me = BooleanField("Запомнить меня", default=False)
    submit = SubmitField("Войти", )

#TODO Написать отдельный класс для формы регистрации на сайте по аналогу с логином
class RegisterForm(FlaskForm):
    '''Класс описывает поля формы регистрации пользователей на сайте'''
    email = StringField("Email: ", validators=[Email("Некорректный email")])
    psw = PasswordField("Пароль: ", validators=[DataRequired(),
        Length(min=6, max=100, message="Пароль должен быть от 6 до 100 символов")])
    psw2 = PasswordField("Повтор пароля: ",
            validators=[DataRequired(),
                        EqualTo ('psw', message="Пароли не совпадают")])
    register = SubmitField("Регистрация", )
