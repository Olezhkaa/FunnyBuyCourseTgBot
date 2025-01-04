import sqlite3
from config import DATABASE

def create_table_user(cursor):
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS users (id integer primary key , id_user_tg varchar(50),name varchar(50), surname varchar(50))')

def insert_user(id_user_tg, name, surname):
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = lambda cursor, row: row[0]
    cursor = connection.cursor()

    params = (id_user_tg, name, surname)

    user_me = cursor.execute('SELECT * FROM users WHERE id_user_tg=(?)', (id_user_tg,)).fetchall()
    if user_me.__len__() == 0:
        cursor.execute('INSERT INTO users (id, id_user_tg, name, surname) VALUES (NULL, ?, ?, ?)',params)

    connection.commit()
    cursor.close()
    connection.close()

def get_all_users():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    users_list = cursor.execute('SELECT * FROM users').fetchall()

    connection.commit()
    cursor.close()
    connection.close()

    return users_list

def delete_user_by_id_user_tg(id_user_tg):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute('DELETE FROM users WHERE id_user_tg=(?)', (id_user_tg, ))

    connection.commit()
    cursor.close()
    connection.close()