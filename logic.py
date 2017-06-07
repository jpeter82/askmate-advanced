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


def list_users():
    '''
    List all the registered users with all their attributes except their id.
        @return
    '''
    users_data = db.perform_query("""SELECT user_name, reputation, reg_time FROM users;""")
    return users_data
