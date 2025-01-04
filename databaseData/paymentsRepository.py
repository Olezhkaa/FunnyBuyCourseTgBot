import sqlite3
from database import get_all_users
from config import DATABASE

def create_table_payments(cursor):
    cursor.execute('CREATE TABLE IF NOT EXISTS payments (user_id varchar(50), payment_id varchar(50),amount varchar(50), currency varchar(50))')

def insert_payment(id_user_tg, payment_id, amount, currency):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute('INSERT INTO payments (user_id, payment_id, amount, currency) VALUES (?, ?, ?, ?)',(id_user_tg, payment_id, amount/100, currency))

    connection.commit()
    cursor.close()
    connection.close()