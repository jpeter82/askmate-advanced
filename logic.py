from psycopg2 import connect, extras
import db
from datetime import datetime
# business logic comes here


def single_question(question_id):
    """Returns a single question in dict"""
    with db.get_cursor() as cursor:
        try:
            sql = """SELECT * FROM question WHERE id = %s;"""
            data = (question_id,)
            cursor.execute(sql, data)
            question = cursor.fetchall()
            return question
        except:
            print("Something went wrong.")


def all_questions():
    """Returns all the questions list of dicts"""
    with db.get_cursor() as cursor:
        try:
            sql = """SELECT * FROM question"""
            cursor.execute(sql)
            questions = cursor.fetchall()
            return questions
        except:
            print("Something went wrong.")


def get_question_by_answer_id(answer_id):
    return


def new_q_a(info_dict, mode):
    """Reqs a dict, key is 'message' if mode is answer, else /mode is question/ 'title' and 'message'"""
    with db.get_cursor() as cursor:
        try:
            if mode == "answer":
                sql = """INSERT INTO answer (message) VALUES(%s);"""
                data = (info_dict['message'],)
            elif mode == "question":
                sql = """INSERT INTO question (title, message) VALUES(%s, %s);"""
                data = (info_dict['title'], info_dict['message'])
            cursor.execute(sql, data)
        except:
            print("Something went wrong")


def new_comment(info_dict, mode):
    """dict keys are id and message, mode answer or question """
    with db.get_cursor() as cursor:
        try:
            if mode == 'question':
                sql = """INSERT INTO comment (question_id, message)
                VALUES(%s, %s);"""
            elif mode == 'answer':
                sql = """INSERT INTO comment (answer_id, message)
                VALUES(%s, %s);"""
            data = (
                info_dict['id'],
                info_dict['message'])
            cursor.execute(sql, data)
        except:
            print('Something went wrong')


def edit_comment(info_dict):
    """Reqs a dict, where keys are message and id"""
    with db.get_cursor() as cursor:
        try:
            cursor.execute("""SELECT edited_count FROM comment WHERE id = %s""" % info_dict['id'])
            result = cursor.fetchone()
            if result['edited_count'] is None:
                result = 1
            else:
                result = result['edited_count'] + 1
            sql = """UPDATE comment SET message = %s, edited_count = %s WHERE id = %s;"""
            data = (info_dict['message'], result, info_dict['id'])
            cursor.execute(sql, data)
        except:
            print("Something went wrong")


def edit_q_or_a(info_dict, mode=None):
    """Updates a question or answer. the mode can be question or answer. Requires a dictionary. keys: message and id"""
    with db.get_cursor() as cursor:
        try:
            if mode == 'answer':
                sql = """UPDATE answer SET message = %s WHERE id = %s;"""
            else:
                sql = """UPDATE question SET message = %s WHERE id = %s;"""
            data = (info_dict['message'], info_dict['id'])
            cursor.execute(sql, data)
        except:
            print("Something went wrong")


def delete_comment(id_for_delete, mode):
    """Deletes a comment"""
    with db.get_cursor() as cursor:
        try:
            if mode == "question":
                sql = """DELETE FROM question WHERE id = %s;"""
            elif mode == 'answer':
                sql = """DELETE FROM answer WHERE id = %s;"""
            elif mode == 'comment':
                sql = """DELETE FROM comment WHERE id = %s;"""
            data = (id_for_delete,)
            cursor.execute(sql, data)
        except:
            print("Something went wrong")


if __name__ == '__main__':
    return
