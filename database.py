import sqlite3
from config import DATABASE
from databaseData.usersRepository import *
from databaseData.courseRepository import *
from databaseData.paymentsRepository import *

def init_db():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    create_table(cursor)

    connection.commit()
    cursor.close()
    connection.close()

def create_table(cursor):
    create_table_user(cursor)
    create_table_course(cursor)
    create_table_payments(cursor)

def add_user(id_user_tg, name, surname): insert_user(id_user_tg, name, surname)
def all_users(): return get_all_users()
def delete_user(id_user_tg) : delete_user_by_id_user_tg(id_user_tg)

def save_payment(id_user_tg, payment_id, amount, currency): insert_payment(id_user_tg, payment_id, amount, currency)
