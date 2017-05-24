from psycopg2 import connect, extras
import db
from datetime import datetime
# business logic comes here


def new_comment(info_dict, mode=False):
    """information, dict or list?
    mode is false => question comment, if True => answer comment"""
    new_id = new_id_generator('comment')
    dt = datetime.now()
    with db.get_cursor() as cursor:
        try:
            if mode is False:
                sql = """INSERT INTO comment (id, question_id, message, submission_time)
                VALUES(%s, %s, %s, %s);"""
            else:
                sql = """INSERT INTO comment (id, answer_id, message, submission_time)
                VALUES(%s, %s, %s, %s);"""
            data = (
                new_id,
                info_dict['group_id'],
                info_dict['message'],
                dt)
            cursor.execute(sql, data)
        except:
            print('Something went wrong')


def new_id_generator(where):
    with db.get_cursor() as cursor:
        try:
            cursor.execute("""SELECT id FROM %s ORDER BY id DESC LIMIT 1""" % where)
            result = cursor.fetchone()
            result = int(result[0])+1
            return result
        except:
            print("Something went wrong")


def edit_comment(info_dict):
    dt = datetime.now()
    with db.get_cursor() as cursor:
        try:
            cursor.execute("""SELECT edited_count FROM comment WHERE id = %s""" % info_dict['comment_id'])
            result = cursor.fetchone()
            if result[0] is None:
                result = 1
            else:
                result = result[0] + 1
            sql = """UPDATE comment SET message = %s, submission_time = %s, edited_count = %s WHERE id = %s;"""
            data = (info_dict['message'], dt, result, info_dict['comment_id'])
            cursor.execute(sql, data)
        except:
            print("Something went wrong")


def delete_comment(comment_id):
    with db.get_cursor() as cursor:
        try:
            cursor.execute("""DELETE FROM comment WHERE id = %s""" % comment_id)
        except:
            print("Something went wrong")

