from flask import Flask, render_template, request, session
import os
import json
import random

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

RIDDLE_FILE = 'riddles.json'

def load_riddles():
    try:
        with open(RIDDLE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_riddle(riddle, answer):
    riddles = load_riddles()
    riddles.append({'riddle': riddle, 'answer': answer.lower()})
    with open(RIDDLE_FILE, 'w', encoding='utf-8') as f:
        json.dump(riddles, f, ensure_ascii=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        riddle = request.form['riddle'].strip()
        answer = request.form['answer'].strip()
        if riddle and answer:
            save_riddle(riddle, answer)
        return render_template('index.html', riddles=load_riddles())

    return render_template('index.html', riddles=load_riddles())

@app.route('/guess', methods=['GET', 'POST'])
def guess():
    riddles = load_riddles()
    
    if request.method == 'GET':
        if not riddles:
            return render_template('index.html', error="❌ 题库为空！")
        idx = random.randrange(len(riddles))
        session['current'] = {
            'id': idx,
            'answer': riddles[idx]['answer'].lower(),
            'text': riddles[idx]['riddle']
        }
        return render_template('index.html', 
                             current=session['current']['text'],
                             riddles=riddles)

    if 'current' not in session:
        return redirect('/guess')
    
    user_ans = request.form['answer'].strip().lower()
    correct = session['current']['answer']
    result = {
        'is_correct': user_ans == correct,
        'user_answer': user_ans,
        'correct_answer': correct,
        'current_riddle': session['current']['text']
    }
    session.pop('current', None)
    
    return render_template('index.html',
                         result=result,
                         riddles=riddles,
                         current=result['current_riddle'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
