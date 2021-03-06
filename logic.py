import db


def get_questions(sort_order, five=False):
    """
    Returns all the questions.
        @param     sort_order    string     The request path
        @param     five          bool       True if you want only 5 questions, otherwise False
        @return                  list       List of dictionaries for each question.
    """
    sql = """SELECT id,
                    title,
                    message,
                    view_number,
                    vote_number,
                    to_char(submission_time, 'YYYY-MM-DD HH24:MI') AS submission_time
             FROM question"""

    if sort_order:
        fields = {'time': 'submission_time', 'view': 'view_number', 'vote': 'vote_number',
                  'title': 'title', 'message': 'message'}
        order_by = ', '.join(fields[item[0]] + ' ' + item[1] for item in sort_order)
        sql = sql + """ ORDER BY """ + order_by
    else:
        sql = sql + """ ORDER BY submission_time DESC"""

    if five:
        sql = sql + """ LIMIT 5"""

    questions = db.perform_query(sql)
    return questions


def user_search(search_phrase):
    """
    Returns search results for user query \n
        @param      search_phrase   string          Phrase providid by the user \n
        @return                     list of dicts   Records that match the search phrase
    """
    data = {'phrase': search_phrase}
    sql = """SELECT q.id AS question_id,
                    REPLACE(q.title, %(phrase)s, CONCAT('<span class="special-format">',
                                                                            %(phrase)s, '</span>')) AS title,
                    REPLACE(q.message, %(phrase)s, CONCAT('<span class="special-format">', %(phrase)s, '</span>'))
                    AS question_body,
                    q.view_number,
                    q.vote_number AS question_vote,
                    to_char(q.submission_time, 'YYYY-MM-DD HH24:MI') AS submission_time,
                    NULL AS answer_id,
                    NULL AS answer_body,
                    NULL AS answer_date,
                    NULL AS answer_vote
                FROM question q
                WHERE q.title ILIKE CONCAT('%%', %(phrase)s, '%%') OR q.message ILIKE CONCAT('%%', %(phrase)s, '%%')

                UNION ALL

                SELECT q.id AS question_id,
                    REPLACE(q.title, %(phrase)s, CONCAT('<span class="special-format">',
                                                                            %(phrase)s, '</span>')) AS title,
                    q.message AS question_body,
                    q.view_number,
                    q.vote_number AS question_vote,
                    to_char(q.submission_time, 'YYYY-MM-DD HH24:MI') AS submission_time,
                    a.id AS answer_id,
                    REPLACE(a.message, %(phrase)s, CONCAT('<span class="special-format">',
                                                                            %(phrase)s, '</span>')) AS answer_body,
                    to_char(a.submission_time, 'YYYY-MM-DD HH24:MI') AS answer_date,
                    a.vote_number AS answer_vote
                FROM question q
                LEFT OUTER JOIN answer a ON q.id = a.question_id
                WHERE a.message ILIKE CONCAT('%%', %(phrase)s, '%%')
                ORDER BY question_id DESC, answer_id DESC;"""
    records = db.perform_query(sql, data)
    return records


def generate_links(sort_order):
    '''
    Generate links for ordering the table for all 5 columns.
        @param    sort_order    list      List of tuples containing the request path parameters
        @return                 list      List of tuples containing the links as (column, order)
    '''
    links = {}
    columns = ('time', 'view', 'vote', 'title', 'message')

    if sort_order:
        sorted_columns = [item[0] for item in sort_order]

        for column in columns:
            if len(sort_order) == 1:
                if column in sorted_columns:
                    links[column] = '{}={}'.format(column, 'asc' if sort_order[0][1] == 'desc' else 'desc')
                else:
                    links[column] = '{}={}&{}=asc'.format(sort_order[0][0], sort_order[0][1], column)
            else:
                if column in sorted_columns:
                    filtered_sort_order = [item for item in sort_order if column != item[0]]
                    request_params = '&'.join(list(map(lambda x: '='.join(x), filtered_sort_order)))
                    column_order = [item for item in sort_order if column == item[0]][0][1]
                    links[column] = request_params + '&{}={}'.format(column,
                                                                     'asc' if column_order == 'desc' else 'desc')
                else:
                    request_params = '&'.join(list(map(lambda x: '='.join(x), sort_order)))
                    links[column] = request_params + '&{}=asc'.format(column)
    else:
        for column in columns:
            links[column] = '{}=asc'.format(column)
    return links


def url_helper(url):
    '''
    Convert URL parameters to list of tuples
        @param    url    string    The request URL
        @return          list      List of tuples, i.e (column, order)
    '''
    params_start = url.find('?')
    if params_start == -1:
        params = False
    else:
        params = url[params_start + 1:].split('&')
        params = list(map(lambda x: tuple(x.split('=')), params))
    return params


def new_user(username):
    """
    Insert the new user into the users table
        @param  username    string      The chosen name by the user
        @return             int or None If the insert is done, returns with the new user's id.
                                        If the username is already taken, returns None
    """
    sql = """INSERT INTO users (user_name) VALUES (%s) RETURNING id;"""
    data = (username,)
    return db.perform_query(sql, data)


def list_users():
    '''
    List all the registered users with all their attributes except their id.
    '''
    users_data = db.perform_query("""SELECT id, user_name, reputation, reg_time FROM users;""")
    return users_data


def user_data(user_id):
    '''
    List all the data added by a user (comments, answers, questions) by their id.
        @param      user_id     int     ID of the user
        @return                 dict    keys: question, answer, comments. values: messages
    '''
    sql = """SELECT id,
                    title,
                    submission_time
             FROM question
             WHERE user_id = %s
             ORDER BY id DESC;"""

    sql2 = """SELECT q.id,
                     q.title,
                     a.message,
                     a.submission_time,
                     a.answered_by,
                     CASE WHEN a.accepted_by IS NULL THEN 0 ELSE 1 END AS accepted
              FROM answer a
              INNER JOIN question q ON a.question_id = q.id
              WHERE a.answered_by = %s
              ORDER BY a.id DESC;"""

    sql3 = """SELECT q.id,
                     q.title,
                     a.message as answer_message,
                     c.message as comment_message,
                     c.submission_time
              FROM comment c
              LEFT OUTER JOIN answer a ON a.id = c.answer_id
              LEFT OUTER JOIN question q ON q.id = c.question_id
              WHERE c.user_id = %s
              ORDER BY c.id DESC;"""
    data = (user_id,)
    user_question = db.perform_query(sql, data)
    user_answer = db.perform_query(sql2, data)
    user_comment = db.perform_query(sql3, data)
    result = {"questions": user_question, 'answers': user_answer, 'comments': user_comment}
    return result


def user_by_id(id):
    '''
    Get the user by it's ID.
        @param      id     int     ID of the user
        @return     string         The username with the chosen id.
    '''
    sql = """SELECT user_name FROM users WHERE id = %s"""
    data = (id,)
    user = db.perform_query(sql, data)
    return user


def get_user_by_name(user_name):
    '''
    Get the user by it's name.
        @param      user_name     sting     Name of the user
        @return     id            int       The chosen user's id
    '''
    user_id = db.perform_query("""SELECT id FROM users WHERE user_name = %s LIMIT 1;""", (user_name,))
    return user_id[0]['id']


def get_one_question(question_id, answers=False):
    """
    Returns a single question and corresponding anwers with comments in dict
        @param    question_id   int       The id of the question to be displayed
        @param    answers       boolean   True if you need only the question, False if you need both
        @return                 dict      The result set of questions and answers
    """
    answer = None
    data = (question_id,)

    sql = """SELECT q.title,
                    q.message AS question_body,
                    q.id,
                    to_char(q.submission_time, 'YYYY-MM-DD HH24:MI') AS question_date,
                    q.view_number,
                    q.vote_number,
                    q.user_id AS question_user_id,
                    u.user_name AS question_user_name,
                    c.message AS comment_body,
                    to_char(c.submission_time, 'YYYY-MM-DD HH24:MI') AS comment_date,
                    c.id as comment_id,
                    c.user_id as question_comment_user_id,
                    us.user_name AS question_comment_user_name
             FROM question q
             LEFT OUTER JOIN comment c ON q.id = c.question_id
             LEFT OUTER JOIN users u ON q.user_id = u.id
             LEFT OUTER JOIN users us ON c.user_id = us.id
             WHERE q.id = %s
             ORDER BY c.submission_time DESC;"""
    question = db.perform_query(sql, data)

    if answers:
        sql2 = """SELECT a.message AS answer_body,
                         a.id AS answer_id,
                         to_char(a.submission_time, 'YYYY-MM-DD HH24:MI') AS answer_date,
                         a.vote_number,
                         a.answered_by,
                         COALESCE(a.accepted_by, 0) AS accepted_by,
                         u.user_name AS answer_user_name,
                         c.message AS comment_body,
                         to_char(c.submission_time, 'YYYY-MM-DD HH24:MI') AS comment_date,
                         c.id AS comment_id,
                         c.answer_id AS comment_answer_id,
                         c.user_id,
                         us.user_name AS answer_comment_user_name
                  FROM answer a
                  LEFT OUTER JOIN comment c ON a.id = c.answer_id
                  LEFT OUTER JOIN users u ON a.answered_by = u.id
                  LEFT OUTER JOIN users us ON c.user_id = us.id
                  WHERE a.question_id = %s
                  ORDER BY accepted_by DESC, a.vote_number DESC, a.submission_time DESC, c.submission_time DESC;"""
        answer = db.perform_query(sql2, data)

        result = {'question': question, 'answer': answer}
        return result


def get_question_by_answer_id(answer_id):
    """
    Get corresponding answer for given question id \n
        @param      answer_id          int      Which answer you need the corresponding question id to \n
        @return                        int      Get the corresponding question id
    """
    question_id = False
    if answer_id:
        sql = """SELECT question_id FROM answer WHERE id = %s;"""
        data = (answer_id,)
        question_id = db.perform_query(sql, data)[0]['question_id']
    return question_id


def process_form(form_data):
    """
    Handles Insert/Update Q/A/C \n
        @param      form_data      User input
        @return     dict            keys: status, question_id values:true/false, question's id
    """
    question_id = False
    try:
        modID = int(form_data['modID'])
        typeID = int(form_data['typeID'])
    except ValueError:
        status = False
        question_id = None
    else:
        if modID == -1:
            # insert
            if typeID == 1:
                # question
                sql = """INSERT INTO question (title, message, user_id)
                         VALUES (%s, %s, %s) RETURNING id AS question_id;"""
                data = (form_data['title'], form_data['message'], get_user_by_name(form_data['user']))
            elif typeID == 2:
                # answer
                sql = """INSERT INTO answer (question_id, message, answered_by)
                         VALUES (%s, %s, %s) RETURNING question_id;"""
                data = (form_data['question_id'], form_data['message'], get_user_by_name(form_data['user']))
            elif typeID == 3 and form_data.get('answer_id', -10) == -10:
                # comment to question
                sql = """INSERT INTO comment (question_id, message, user_id)
                         VALUES (%s, %s, %s) RETURNING question_id;"""
                data = (form_data['question_id'], form_data['message'], get_user_by_name(form_data['user']))
            elif typeID == 3 and form_data['answer_id']:
                # comment to answer
                sql = """INSERT INTO comment (answer_id, message, user_id) VALUES (%s, %s, %s) RETURNING id;"""
                data = (form_data['answer_id'], form_data['message'], get_user_by_name(form_data['user']))
                question_id = get_question_by_answer_id(form_data['answer_id'])
            else:
                raise ValueError
        else:
            # update
            if typeID == 1:
                # question
                sql = """UPDATE question SET title = %s, message = %s WHERE id = %s RETURNING id AS question_id"""
                data = (form_data['title'], form_data['message'], modID)
            elif typeID == 2:
                # answer
                sql = """UPDATE answer SET message = %s WHERE id = %s RETURNING question_id"""
                data = (form_data['message'], modID)
            elif typeID == 3:
                # comment
                sql = """UPDATE comment SET message = %s WHERE id = %s RETURNING id;"""
                data = (form_data['message'], modID)
                question_id = form_data['question_id'] if form_data.get(
                    'question_id', '') else get_question_by_answer_id(form_data['answer_id'])
            else:
                raise ValueError

        query_result = db.perform_query(sql, data)
        status = True if query_result else False
        question_id = question_id if question_id else query_result[0]['question_id']
        result = {'status': status, 'question_id': question_id}
        return result


def process_delete(id, table):
    """
    Delete a question, answer or comment
        @param    id       int       The id of the record to be deleted
        @param    table    string    The table from which the id will be deleted
        @return            bool      Status: True if successful, otherwise False
    """
    data = (id,)
    if table == "question":
        sql = """DELETE FROM question WHERE id = %s RETURNING id;"""
    elif table == 'answer':
        sql = """DELETE FROM answer WHERE id = %s RETURNING id;"""
    elif table == 'comment':
        sql = """DELETE FROM comment WHERE id = %s RETURNING id;"""
    else:
        raise ValueError

    status = True if db.perform_query(sql, data) else False
    return status


def select_edit_data(id, mode):
    """
    Returns a dict by ID from DB
        @param    id_to_get   int       The id of the needed table
        @param    mode        string    Which table
        @return               dict      Needed table in a dict
    """
    if mode == 'question':
        sql = """SELECT id,
                        title,
                        message
                 FROM question
                 WHERE id = %s;"""
    elif mode == 'answer':
        sql = """SELECT id,
                        message,
                        question_id
                 FROM answer
                 WHERE id = %s;"""
    elif mode == 'comment':
        sql = """SELECT c.id,
                        c.message,
                        CASE WHEN c.question_id IS NOT NULL THEN c.question_id ELSE a.question_id END AS question_id,
                        c.answer_id
                 FROM comment c
                 LEFT OUTER JOIN answer a ON a.id = c.answer_id
                 WHERE c.id = %s;"""
    else:
        raise ValueError
    data = (id,)
    result = db.perform_query(sql, data)
    return result


def accepted_answer(answer_id, user_id):
    """
    Updates in the answer table the accepted_by field with the user's id.
        @answer_id  int     answer's id
        @user_id    int     user's id
        @return     int     the updated answer's id
    """
    sql = """UPDATE answer SET accepted_by = %s WHERE id = %s RETURNING id;"""
    data = (user_id, answer_id)
    result = db.perform_query(sql, data)
    reputation = db.perform_proc('update_reputation', [user_id, 'accepted_answer'])
    return result


def process_votes(id, user_id, questions=True, direction='up'):
    """
    Handles the voting process.
        @param id           int     id                  Id of the chosen q/a for upvote
        @param user_id      int     user's id           Who owns the q/a
        @param questions    int     true/false          Question or answer
        @param direction    string  up/somethig else    Is that an upvote or not
    """
    status = False
    if id:
        if direction not in ('up', 'down'):
            raise ValueError

        if questions is True:
            if direction == 'up':
                sql = """UPDATE question SET vote_number = vote_number + 1 WHERE id = %s RETURNING id;"""
                reputation = db.perform_proc('update_reputation', [user_id, 'upvoted_question'])
            else:
                sql = """UPDATE question SET vote_number = vote_number - 1 WHERE id = %s RETURNING id;"""
                reputation = db.perform_proc('update_reputation', [user_id, 'downvoted_question'])
        elif questions is False:
            if direction == 'up':
                sql = """UPDATE answer SET vote_number = vote_number + 1 WHERE id = %s RETURNING id;"""
                reputation = db.perform_proc('update_reputation', [user_id, 'upvoted_answer'])
            else:
                sql = """UPDATE answer SET vote_number = vote_number - 1 WHERE id = %s RETURNING id;"""
                reputation = db.perform_proc('update_reputation', [user_id, 'downvoted_answer'])
        else:
            raise ValueError
        data = (id,)
        status = True if db.perform_query(sql, data) else False
    return status


def update_view_number(question_id):
    """
    Set the view numbers.
        @param question_id      int         Question's id
        @return                 bool        True, if the update is done else False
    """
    status = False
    if question_id:
        sql = """UPDATE question SET view_number = view_number + 1 WHERE id = %s RETURNING id;"""
        data = (question_id,)
        status = True if db.perform_query(sql, data) else False
    return status
