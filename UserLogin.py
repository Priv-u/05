'''Модуль описывает класс для работы с авторизаций пользователей'''

class UserLogin():
    '''Класс описывающий работу с авторизацией пользователей'''
    def fromDB(self, user_id, db):
        '''Метод получает данные о пользователе из базы данных'''
        self.__user = db.get_user(user_id)
        return self

    def create(self, user):
        '''Метод создает экземпляр класса и добавляет в него данные о пользователе'''
        self.__user = user
        return self

    def is_authenticated(self):
        '''Метод проверяет авторизован ли пользователь'''
        return True

    def is_active(self):
        '''Метод проверяет активен ли пользователь'''
        return True

    def is_anonymous(self):
        '''Метод проверяет использует ли пользователь анонимный вход'''
        return False

    def get_id(self):
        '''Метод возвращает строковое значение id пользователя'''
        return str(self.__user['id'])
