from psycopg2 import connect, extras
import db
from datetime import datetime


def single_question(question_id, answers=False):
    """Returns a single question and corresponding anwers with comments in dict"""
    answer = None
    with db.get_cursor() as cursor:
        data = (question_id,)

        sql = """SELECT q.title,
                        q.message AS question_body,
                        q.id,
                        to_char(q.submission_time, 'YYYY-MM-DD HH24:MI') AS question_date,
                        q.view_number,
                        q.vote_number,
                        c.message AS comment_body,
                        to_char(c.submission_time, 'YYYY-MM-DD HH24:MI') AS comment_date
                 FROM question q
                 LEFT OUTER JOIN comment c ON q.id = c.question_id
                 WHERE q.id = %s
                 ORDER BY c.submission_time DESC;"""
        cursor.execute(sql, data)
        question = cursor.fetchall()

        if answers:
            sql2 = """SELECT a.message AS answer_body,
                             a.id,
                             to_char(a.submission_time, 'YYYY-MM-DD HH24:MI') AS answer_date,
                             a.vote_number,
                             c.message AS comment_body,
                             to_char(c.submission_time, 'YYYY-MM-DD HH24:MI') AS comment_date
                      FROM answer a
                      LEFT OUTER JOIN comment c ON a.id = c.answer_id
                      WHERE a.question_id = %s
                      ORDER BY a.vote_number DESC, a.submission_time DESC, c.submission_time DESC;"""
            cursor.execute(sql2, data)
            answer = cursor.fetchall()

        result = {'question': question, 'answer': answer}
        return result


def single_dict(id_to_get, mode):
    with db.get_cursor() as cursor:
        try:
            if mode == 'answer':
                sql = """SELECT * FROM answer WHERE id = %s;"""
            elif mode == 'question':
                sql = """SELECT * FROM question WHERE id = %s;"""
            else:
                sql = """SELECT * FROM comment WHERE id = %s;"""
            data = (id_to_get,)
            cursor.execute(sql, data)
            result = cursor.fetchone()
            return result
        except:
            print("Something went wrong: SINGLE answer")


def all_questions():
    """Returns all the questions list of dicts"""
    with db.get_cursor() as cursor:
        sql = """SELECT id,
                        title,
                        message,
                        view_number,
                        vote_number,
                        to_char(submission_time, 'YYYY-MM-DD HH24:MI') AS submission_time
                 FROM question
                 ORDER BY submission_time DESC"""
        cursor.execute(sql)
        questions = cursor.fetchall()
    return questions


def new_q_a(info_dict, mode):
    print(info_dict)
    """Reqs a dict, key is 'message' if mode is answer, else /mode is question/ 'title' and 'message'"""
    with db.get_cursor() as cursor:
        try:
            if mode == "answer":
                sql = """INSERT INTO answer (message, question_id) VALUES(%s, %s);"""
                data = (info_dict['message'], info_dict['questionID'])
            elif mode == "question":
                sql = """INSERT INTO question (title, message) VALUES(%s, %s);"""
                data = (info_dict['title'], info_dict['message'])
            cursor.execute(sql, data)
        except:
            print("Something went wrong: newQA")


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
            print('Something went wrong NEW comment')


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
            print("Something went wrong EDIT COMMENT")


def edit_q_a(info_dict, mode=None):
    """Updates a question or answer. the mode can be question or answer. Requires a dictionary. keys: message and id"""
    with db.get_cursor() as cursor:
        try:
            if mode == 'answer':
                sql = """UPDATE answer SET message = %s WHERE id = %s;"""
                data = (info_dict['message'], info_dict[mode+'ID'])
            else:
                sql = """UPDATE question SET message = %s, title = %s WHERE id = %s;"""
                data = (info_dict['message'], info_dict['title'], info_dict[mode+'ID'])
            cursor.execute(sql, data)
        except:
            print("Something went wrong EDIT QA")


def delete(id_for_delete, mode):
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
            print("Something went wrong DELETE")


def user_search(search_phrase):
    """Returns search results for user query"""
    with db.get_cursor() as cursor:
        data = {'phrase': search_phrase}
        sql = """SELECT q.id AS question_id,
                        REPLACE(q.title, %(phrase)s, CONCAT('<span class="special-format">', %(phrase)s, '</span>')) AS title,
                        q.message AS question_body,
                        q.view_number,
                        q.vote_number AS question_vote,
                        to_char(q.submission_time, 'YYYY-MM-DD HH24:MI') AS submission_time,
                        NULL AS answer_id,
                        NULL AS answer_body,
                        NULL AS answer_date,
                        NULL AS answer_vote
                 FROM question q
                 WHERE LOWER(q.title) LIKE CONCAT('%', LOWER(%(phrase)s), '%')

                 UNION ALL

                 SELECT q.id AS question_id,
                        REPLACE(q.title, %(phrase)s, CONCAT('<span class="special-format">', %(phrase)s, '</span>')) AS title,
                        q.message AS question_body,
                        q.view_number,
                        q.vote_number AS question_vote,
                        to_char(q.submission_time, 'YYYY-MM-DD HH24:MI') AS submission_time,
                        a.id AS answer_id,
                        REPLACE(a.message, %(phrase)s, CONCAT('<span class="special-format">', %(phrase)s, '</span>')) AS answer_body,
                        to_char(a.submission_time, 'YYYY-MM-DD HH24:MI') AS answer_date,
                        a.vote_number AS answer_vote
                 FROM question q
                 LEFT OUTER JOIN answer a ON q.id = a.question_id
                 WHERE LOWER(a.message) LIKE CONCAT('%', LOWER(%(phrase)s), '%')
                 ORDER BY question_id DESC, answer_id DESC;"""
        cursor.execute(sql, data)
        records = cursor.fetchall()
    return records

if __name__ == '__main__':
    pass
