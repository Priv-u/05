'''Модуль содержит класс описывающий инструменты для работы
    с базой данных
'''
import sqlite3
import math
import time
import re
from flask import url_for


class FDataBase:
    '''Класс для работы с БД'''
    def __init__(self, data_base):
        self.__db = data_base
        self.__cur = data_base.cursor()


    def get_menu(self):
        '''Метод получает из БД все пункты меню'''
        sql = '''SELECT * FROM mainmenu'''
        try:
            self.__cur.execute(sql)
            result = self.__cur.fetchall()
            if result:
                return result
        except sqlite3.Error as sql_error:
            print(f"Ошибка чтения из БД: {sql_error}")
        return []


    def add_post(self, title, url, text ):
        '''Метод добавляет статью в базу данных'''
        try:
            self.__cur.execute(f"SELECT COUNT() as `count` FROM posts WHERE url LIKE '{url}'")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print('Статья с таким url уже существует')
                return False

            base = url_for('static', filename='images_html')

            text = re.sub(r"(?P<tag><img\s+[^>]*src=)(?P<quote>[\"'])(?P<url>.+?)(?P=quote)>",
                    "\\g<tag>" + base + "/\\g<url>>", text)

            actual_time = math.floor(time.time())
            self.__cur.execute("INSERT INTO posts VALUES(NULL,?,?,?,?)",
                                (title, text, url, actual_time))
            self.__db.commit()
        except sqlite3.Error as sql_error:
            print('Ошибка добавления статьи в БД '+str(sql_error))
            return False
        return True


    def get_post(self, alias):
        '''Метод получает статью из базы данных по id'''
        try:
            self.__cur.execute(f"SELECT title, text FROM posts WHERE url LIKE '{alias}' LIMIT 1")
            res = self.__cur.fetchone()
            if res:
                return res

        except sqlite3.Error as sql_error:
            print(f"Ошибка получения статьи из БД: {str(sql_error)}")
        return (False, False)


    def get_post_anons(self):
        '''Метод получает анонс по всем статьям из базы данных'''
        try:
            self.__cur.execute("SELECT id, title, text, url FROM posts ORDER BY time DESC")
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as sql_error:
            print(f"Ошибка получения статьи из БД: {str(sql_error)}")
            # print('Ошибка получения статьи из БД '+str(sql_error))
        return []

    def add_user(self, name, email, psw):
        '''Метод описывает добавление нового пользователя в базу данных'''
        try:
            self.__cur.execute(f"SELECT COUNT() as `count` FROM users WHERE email LIKE '{email}'")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print("Пользователь с таким email уже существует")
                return False
            add_user_time = math.floor(time.time())
            self.__cur.execute("INSERT INTO users VALUES (NULL, ?, ?, ?, NULL, ?)",
                                                (name, email, psw, add_user_time))
            self.__db.commit()
        except sqlite3.Error as sql_err:
            print("Ошибка добавления пользователя в БД" + str(sql_err))
            return False
        return True

    def get_user(self, user_id):
        '''Метод получает данные пользователя из БД по его id'''
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print('Пользователь не найден')
                return False
            return res
        except sqlite3.Error as sql_error:
            print("Ошибка получения данных из БД" + str(sql_error))
        return False

    def get_user_by_email(self, email):
        '''Проверяет пользователя по наличию указанного email в базе данных'''
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE email = '{email}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False
            return res
        except sqlite3.Error as sql_error:
            print("Ошибка получения данных из БД" + str(sql_error))
        return False

    def update_user_avatar(self, avatar, user_id):
        '''Метод добавляет аватар пользователя в базу данных'''
        if not avatar:
            return False
        try:
            binary = sqlite3.Binary(avatar)
            # self.__cur.execute(f"UPDATE users SET avatar = {binary} WHERE id = {user_id}")
            self.__cur.execute("UPDATE users SET avatar = ? WHERE id = ?", (binary, user_id))
            self.__db.commit()
        except sqlite3.Error as sql_error:
            print(f"Ошибка обновления аватара пользователя в БД: {sql_error}")
            return False
        return True
