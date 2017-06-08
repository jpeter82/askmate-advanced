from flask import Flask, request, render_template, url_for, redirect
import logic


app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.do')


@app.route('/', methods=["GET", "POST"])
@app.route('/list', strict_slashes=False, methods=["GET", "POST"])
def index():
    error = False
    if request.path == '/':
        five = True
        link = None
        questions = logic.get_questions(None, five=True)
    else:
        five = False
        link = logic.generate_links(logic.url_helper(request.url))
        questions = logic.get_questions(logic.url_helper(request.url))
    if request.method == "POST":
        user_name = request.form['register']
        new_user = logic.new_user(user_name)
        if new_user is None:
            error = 'Choose another username please.'
    if error:
        template = registration(error)
    else:
        template = render_template('index.html', questions=questions, five=five, link=link)
    return template


@app.route('/search')
def search_questions():
    search_phrase = request.args.get('q', None)
    if search_phrase is not None and len(str(search_phrase)) > 2:
        data = logic.user_search(search_phrase)
        return render_template('search.html', search_phrase=search_phrase, data=data)
    return redirect(request.referrer)


@app.route('/new-question', methods=['GET', 'POST'])
def show_form():
    '''
    modID   -1 in case of insert, otherwise the id of the question to be edited
    typeID  what will be changed: question, answer, comment
    '''
    modID = -1
    typeID = 'question'
    data = None
    users = logic.list_users()
    return render_template('form.html', data=data, typeID=typeID, modID=modID, users=users)


@app.route('/add-edit', methods=['POST'])
def handle_form():
    if request.method == 'POST':
        if request.form.get('modID', 0) and request.form.get('typeID', ''):
            result = logic.process_form(request.form)
            if result['status']:
                question_id = result['question_id']
                return render_template("question.html", data=logic.get_one_question(question_id, answers=True))
    return internal_error(500)


@app.route('/question/<int:question_id>', methods=['GET', 'POST'])
def question(question_id):
    '''
    try:
        logic.update_view_number(question_id)
    except IndexError:
        pass
    '''
    if request.method == 'POST':
        answer_id = request.form['answer_id']
        logic.accepted_answer(answer_id)
    users = logic.list_users()
    return render_template("question.html", data=logic.get_one_question(question_id, answers=True),
                           question_id=question_id, users=users)


@app.route('/user/list')
def list_all_users():
    users = logic.list_users()
    print(users)
    return render_template('users.html', users=users)


@app.errorhandler(404)
def page_not_found(error):
    return 'Oops, page not found!', 404


@app.errorhandler(500)
def internal_error(error):
    return 'Internal server error!', 500


@app.route('/registration', methods=['GET', 'POST'])
def registration(error=None):
    return render_template("reg.html", error=error)


if __name__ == '__main__':
    app.run(debug=True)
