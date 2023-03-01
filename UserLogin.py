'''Модуль описывает класс для работы с авторизаций пользователей'''
from flask import url_for
from flask_login import UserMixin

class UserLogin(UserMixin):
    '''Класс описывающий работу с авторизацией пользователей'''
    def from_db(self, user_id, db):
        '''Метод получает данные о пользователе из базы данных'''
        self.__user = db.get_user(user_id)
        return self

    def create(self, user):
        '''Метод создает экземпляр класса и добавляет в него данные о пользователе'''
        self.__user = user
        return self

    def get_id(self):
        '''Метод возвращает строковое значение id пользователя'''
        return str(self.__user['id'])

    def get_name(self):
        '''Метод возвращает имя пользователя'''
        return self.__user['name'] if self.__user else "Без имени"

    def get_email(self):
        '''Метод возвращает email пользователя'''
        return self.__user['email'] if self.__user else "Без email"

    def get_avatar(self, app):
        '''Метод возвращает аватарку пользователя'''
        img = None
        if not self.__user['avatar']:
            try:
                with app.open_resource(app.root_path +
                url_for('static', filename='images/default.png'),
                "rb") as f:
                    img = f.read()
            except FileNotFoundError as error:
                print('Не найден аватар по умолчанию' + str(error))
        else:
            img = self.__user['avatar']
        return img

    def verify_ext(self, filename):
        '''Метод проверяет расширение выбранного файла и если оно png то возвращает True'''
        f_ext = filename.rsplit('.', 1)[1]
        if f_ext == "png" or f_ext == "PNG":
            return True
        return False
