import config
import psycopg2
from psycopg2 import extras
from psycopg2.pool import SimpleConnectionPool
from contextlib import contextmanager


DB = SimpleConnectionPool(1,
                          1,
                          host=config.HOST,
                          database=config.DB_NAME,
                          user=config.USER,
                          password=config.PASSWORD
                          )


@contextmanager
def get_cursor():
    conn = DB.getconn()
    try:
        yield conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        conn.commit()
    except Exception as e:
        conn.rollback()
        print('An SQL error occured:', e)
    finally:
        DB.putconn(conn)


def perform_query(sql, data=None):
    records = None
    if sql:
        with get_cursor() as cursor:
            cursor.execute(sql, data)
            records = cursor.fetchall()
    return records


def perform_proc(proc_name, data=[]):
    result = None
    if proc_name:
        with get_cursor() as cursor:
            cursor.callproc(proc_name, data)
            result = cursor.fetchall()
    return result
