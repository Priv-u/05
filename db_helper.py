'''В этом модуле будут содержаться функции для работы с базой данных
   обработки запросов и т.п.
'''
import sqlite3
# import config

def connect_db(data_base):
   '''функция создает соединение с базой данных'''
   conn = sqlite3.connect(data_base)
   conn.row_factory=sqlite3.Row
   return conn


def create_db(data_base):
   '''Функция создает базу данных'''
   db = connect_db(data_base)
   