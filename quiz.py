from flask import Flask, session, url_for, redirect, request, render_template
from db_scripts import get_question_after, get_quizes, check_answer
from random import shuffle
import os

def index():
    if request.method == 'GET':
        result = get_quizes()
        return render_template('start.html', quizes=result)
    elif request.method == 'POST':
        session['quiz_id'] = request.form.get('quiz')
        session['last_question_id'] = 0
        session['total'] = 0
        session['correct'] = 0
        return redirect(url_for('test'))
    
def save_answers():
    answer = request.form.get('answer_text')
    question_id = request.form.get('question_id')
    session['last_question_id'] = question_id
    session['total'] += 1
    if check_answer(question_id, answer):
        session['correct'] += 1

def question_form(next_question):
    question_id = next_question[0]
    question = next_question[1]
    answers = list(next_question[2:])
    shuffle(answers)
    return render_template(
        'test.html', question_id=question_id,
        question=question, answers=answers
    )

def test():
    if not('quiz_id' in session) and int(session['last_question_id']) < 0:
        return redirect(url_for('index'))
    else:
        if request.method == 'POST':
            save_answers()
        result = get_question_after(session['last_question_id'], 
                                session['quiz_id'])
        if result is None or not len(result):
            return redirect(url_for('result'))
        else:
            return question_form(result)

def result():
    return render_template('result.html', correct=session['correct'], total=session['total'])


app = Flask(__name__)
app.config['SECRET_KEY'] = 'VeRyStRoNg'
app.add_url_rule('/', 'index', index, methods=['POST', 'GET'])
app.add_url_rule('/test', 'test', test, methods=['POST', 'GET'])
app.add_url_rule('/result', 'result', result)

app.run()



























# Питон ПТ 19:30
# from random import randint
# from flask import Flask, redirect, url_for, session
# from db_scripts import get_question_after


# def index():
#     session['quiz_id'] = randint(1, 3)
#     session['last_question_id'] = 0
#     return '<a href="/test">Перейти к викторине</a>'

# def test():
#     result = get_question_after(session['last_question_id'], session['quiz_id'])
#     if result is None or len(result) == 0:
#         return redirect(url_for('result'))
#     else:
#         session['last_question_id'] = result[0]
#         return f'<h1>{result}</h1>'

# def result():
#     return 'Well done!'

# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'MYVERYSTRONGKEY'
# app.add_url_rule('/', 'index', index)
# app.add_url_rule('/test', 'test', test)
# app.add_url_rule('/result', 'result', result)

# if __name__ == '__main__':
#     app.run()