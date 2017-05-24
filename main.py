from flask import Flask, request, render_template, url_for, redirect
import config
import logic
import sys
# Here comes the Flask part

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
@app.route('/list', methods=['GET', 'POST'])
def index():
    error = None
    if request.method == 'POST':
        if len(request.form.get('description', 0)) < 10 and int(request.form.get('typeID')) == 0:
            return redirect(url_for('show_question_form'))
        if len(request.form.get('description', 0)) < 10 and int(request.form.get('typeID')) == 1:
            return redirect(url_for('show_answer_form', question_id=request.form.get('questionID')))
        if not logic.process_insert_update(request.form):
            error = 'An error occured while updating the database!'
    display = logic.all_questions()
    return render_template('index.html', display=display, error=error)


@app.route('/question/<int:question_id>')
def question(question_id):
    """
    try:
        logic.update_view_number(question_id)
    except IndexError:
        pass"""
    questions = logic.single_question(question_id)
    return render_template("question.html", questions=questions)


@app.route('/new-question', methods=['GET', 'POST'])
@app.route('/question/<int:question_id>/edit', methods=['GET', 'POST'])
def show_question_form(question_id=None):
    if question_id:
        theme = 'question'
        data = logic.single_question(question_id, answers=False)
    else:
        data = None
        theme = 'new-question'
    return render_template('form.html', question=data)


@app.route('/question/<int:question_id>/new-answer', methods=['GET', 'POST'])
@app.route('/answer/<int:answer_id>/edit', methods=['GET', 'POST'])
def show_answer_form(answer_id=None, question_id=None):
    if answer_id:
        theme = 'answer'
        data = logic.get_question_by_answer_id(answer_id)
    else:
        data = None
        theme = 'new-answer'
    return render_template('form.html', theme=theme, question=data, question_id=question_id)


@app.route("/answer/<int:answer_id>/delete")
def delete_answer(answer_id):
    logic.process_delete(answer_id, questions=False)
    return redirect(url_for('index'))


@app.route("/question/<int:question_id>/delete")
def delete_question(question_id):
    logic.process_delete(question_id, questions=True)
    return redirect(url_for('index'))

"""
@app.route("/answer/<answer_id>/vote-<direction>")
@app.route("/question/<question_id>/vote-<direction>")
def vote(direction, question_id=None, answer_id=None):
    if question_id:
        logic.process_votes(question_id, questions=True, direction=direction)
    elif answer_id:
        logic.process_votes(answer_id, questions=False, direction=direction)
        question_id = logic.get_question_by_answer_id(answer_id)['question'][0][0]
    return redirect(url_for('question', question_id=question_id))
"""


@app.errorhandler(404)
def page_not_found(error):
    return 'Oops, page not found!', 404


if __name__ == '__main__':
    app.run(debug=True)