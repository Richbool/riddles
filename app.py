# app.py
import os
import json
import random
from flask import Flask, render_template, request, session, redirect, url_for

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
        json.dump(riddles, f, ensure_ascii=False, indent=2)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        riddle = request.form.get('riddle', '').strip()
        answer = request.form.get('answer', '').strip()
        if len(riddle) > 3 and len(answer) > 1:
            save_riddle(riddle, answer)
        return redirect(url_for('index'))

    riddles = load_riddles()
    current = session.get('current', {}).get('text') if 'current' in session else None
    result = session.pop('result', None) if 'result' in session else None
    return render_template('index.html',
                         riddles=riddles,
                         current=current,
                         result=result)

@app.route('/new')
def new_riddle():
    riddles = load_riddles()
    if not riddles:
        return redirect(url_for('index'))

    previous_id = session.get('current', {}).get('id', -1)
    available = [i for i in range(len(riddles)) if i != previous_id]
    selected_id = random.choice(available) if available else 0

    session['current'] = {
        'id': selected_id,
        'text': riddles[selected_id]['riddle'],
        'answer': riddles[selected_id]['answer'].lower()
    }
    return redirect(url_for('index'))

@app.route('/submit', methods=['POST'])
def submit_answer():
    if 'current' not in session:
        return redirect(url_for('index'))

    user_answer = request.form.get('answer', '').strip().lower()
    correct_answer = session['current']['answer']

    result = {
        'is_correct': user_answer == correct_answer,
        'user_answer': user_answer,
        'correct_answer': correct_answer,
        'question': session['current']['text']
    }

    session['result'] = result
    if result['is_correct']:
        session.pop('current', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
