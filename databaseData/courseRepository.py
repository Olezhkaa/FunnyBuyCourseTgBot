import sqlite3
from config import DATABASE

def create_table_course(cursor):
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS courses (id integer primary key, id_user_tg varchar(100), title varchar(100), payment_id varchar(100))')

def insert_course(id_user_tg, title, payment_id):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute('INSERT INTO courses (id_user_tg, title, payment_id) VALUES (?, ?, ?)',(id_user_tg, title, payment_id))

    connection.commit()
    cursor.close()
    connection.close()

def get_all_courses():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    courses_list = cursor.execute('SELECT * FROM courses').fetchall()

    connection.commit()
    cursor.close()
    connection.close()

    return courses_list

def get_all_courses_by_user_id(id_user_tg):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    courses_list = cursor.execute('SELECT * FROM courses WHERE id_user_tg=(?)', (id_user_tg, )).fetchall()

    connection.commit()
    cursor.close()
    connection.close()

    return courses_list

def purchase_verification_by_user_id_and_title(user_id_tg, name_course):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    title = ""
    if name_course == "programingCourse": title = "Курс по программированию"
    elif name_course == "designerCourse": title = "Курс по дизайну"

    courses_list = None
    if title != "":
        courses_list = cursor.execute('SELECT * FROM courses WHERE id_user_tg=(?) AND title=(?)',(user_id_tg, title)).fetchall()

    connection.commit()
    cursor.close()
    connection.close()

    return courses_list