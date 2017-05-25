from flask import Flask, request, render_template, url_for, redirect
import config
import logic
import sys

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
@app.route('/list', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print(request.form)
        if len(request.form.get('message', '')) < 10 and int(request.form.get('typeID')) == 0:
            return redirect(url_for('show_question_form'))

        if len(request.form.get('message', '')) < 10 and int(request.form.get('typeID')) == 1:
            return redirect(url_for('show_answer_form', question_id=request.form.get('questionID')))

        type = 'question' if int(request.form['typeID']) == 0 else 'answer'
        if int(request.form['modID']) == -1:
            # INSERT
            logic.new_q_a(request.form, type)
        elif int(request.form['modID']) == -2:
            logic.new_comment(request.form)
        elif int(request.form['modID']) == -3:
            logic.edit_comment(request.form)                        # form if theme == comment commentID
        else:
            # UPDATE
            logic.edit_q_a(request.form, type)
    return render_template('index.html', display=logic.all_questions())


@app.route('/question/<int:question_id>')
def question(question_id):
    """
    try:
        logic.update_view_number(question_id)
    except IndexError:
        pass"""
    return render_template("question.html", data=logic.single_question(question_id, answers=True))


@app.route('/new-question', methods=['GET', 'POST'])
@app.route('/question/<int:question_id>/<action>', methods=['GET', 'POST'])
def show_question_form(question_id=None, action=None):
    if question_id:
        if action == "edit":
            theme = 'question'
            data = logic.single_dict(question_id, 'question')
        else:
            theme = "new-comment"
            data = None
    else:
        theme = 'new-question'
        data = None
    return render_template('form.html', question=data, theme=theme, question_id=question_id)


@app.route('/question/<int:question_id>/new-answer', methods=['GET', 'POST'])
@app.route('/answer/<int:answer_id>/<action>', methods=['GET', 'POST'])
def show_answer_form(answer_id=None, question_id=None, action=None):
    if answer_id:
        if action == "edit":
            theme = 'answer'
            data = logic.single_dict(answer_id, 'answer')
        else:
            theme = "new-comment"
            data = None
    else:
        data = None
        theme = 'new-answer'
    return render_template('form.html', theme=theme, question=data, question_id=question_id, answer_id=answer_id)


@app.route("/answer/<int:answer_id>/delete")
def delete_answer(answer_id):
    logic.delete(answer_id, 'answer')
    return redirect(url_for('index'))


@app.route("/question/<int:question_id>/delete")
def delete_question(question_id):
    logic.delete(question_id, 'question')
    return redirect(url_for('index'))


@app.route("/search", methods=['GET'])
def search_questions():
    data = None
    search_phrase = request.args.get('q', None)
    if search_phrase is not None:
        data = logic.user_search(search_phrase)
    return render_template('search.html', search_phrase=search_phrase, data=data)


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
