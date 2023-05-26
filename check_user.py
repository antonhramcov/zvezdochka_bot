import psycopg2
from psycopg2 import Error

def search_user (id:int):
    try:
        connection = psycopg2.connect(dbname="telegram_bot_1", user="bot", password="11111111", host="127.0.0.1", port="5432")
        cursor = connection.cursor()
        postgresql_select_query = "select * from users where id = %s"
        cursor.execute(postgresql_select_query, (id,))
        records = cursor.fetchone()
    except (Exception, Error) as error:
        return ("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            if records == None:
                return False
            else:
                return True

def add_user(id:int, s1:str, s2:str, counts:int):
    try:
        connection = psycopg2.connect(dbname="telegram_bot_1", user="bot", password="11111111", host="127.0.0.1", port="5432")
        cursor = connection.cursor()
        postgres_insert_query = """ INSERT INTO users (ID, FIRST_NAME, USERNAME, COUNTS)
                                           VALUES (%s,%s,%s,%s)"""
        record_to_insert = (id, s1, s2, counts)
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()
        count = cursor.rowcount
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            return "Хорошо, теперь я запомню тебя!)"
