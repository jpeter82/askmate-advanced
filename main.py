from flask import Flask, request, render_template, url_for, redirect
import config
import logic
import sys

app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.do')


@app.route('/', methods=['GET', 'POST'])
@app.route('/list', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        type = 'question' if int(request.form['typeID']) == 0 else 'answer'
        if int(request.form['modID']) == -1:
            # INSERT
            logic.new_q_a(request.form, type)
        elif int(request.form['modID']) == -2:
            logic.new_comment(request.form)
        elif int(request.form['modID']) == -3:
            logic.edit_comment(request.form)
        else:
            # UPDATE
            logic.edit_q_a(request.form, type)
    return render_template('index.html', display=logic.all_questions())


@app.route('/question/<int:question_id>')
def question(question_id):
    try:
        logic.update_view_number(question_id)
    except IndexError:
        pass
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
    return render_template('form.html', data=data, theme=theme, question_id=question_id)


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
    return render_template('form.html', theme=theme, data=data, question_id=question_id, answer_id=answer_id)


@app.route('/comment/<comment_id>/edit')
def show_comment_form(comment_id=None):
    theme = 'comment'
    data = logic.single_dict(comment_id, 'comment')
    return render_template('form.html', theme=theme, comment_id=comment_id, data=data)


@app.route("/answer/<int:answer_id>/delete")
@app.route("/question/<int:question_id>/delete")
@app.route("/comments/<int:comment_id>/delete")
def delete(comment_id=None, answer_id=None, question_id=None):
    if comment_id:
        id_to_delete = comment_id
        mode = 'comment'
    elif answer_id:
        id_to_delete = answer_id
        mode = 'answer'
    else:
        id_to_delete = question_id
        mode = 'question'
    logic.delete(id_to_delete, mode)
    return redirect(url_for('index'))


@app.route("/search", methods=['GET'])
def search_questions():
    data = None
    search_phrase = request.args.get('q', None)
    if search_phrase is not None:
        data = logic.user_search(search_phrase)
    return render_template('search.html', search_phrase=search_phrase, data=data)


@app.route("/answer/<answer_id>/vote-<direction>")
@app.route("/question/<question_id>/vote-<direction>")
def vote(direction, question_id=None, answer_id=None):
    if question_id:
        logic.process_votes(question_id, questions=True, direction=direction)
    elif answer_id:
        logic.process_votes(answer_id, questions=False, direction=direction)
        question_id = logic.get_question_by_answer_id(answer_id)['question_id']
    return redirect(url_for('question', question_id=question_id))


@app.errorhandler(404)
def page_not_found(error):
    return 'Oops, page not found!', 404


if __name__ == '__main__':
    app.run(debug=True)
