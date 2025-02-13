import os
import json
import random
from flask import Flask, render_template, session, redirect, url_for
from urllib.parse import unquote

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['JSON_AS_ASCII'] = False

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RIDDLE_FILE = os.path.join(BASE_DIR, 'riddles.json')

def load_riddles():
    try:
        with open(RIDDLE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"题库加载失败: {str(e)}")
        return []

@app.before_request
def check_session():
    excluded = ['home', 'start_game', 'static']
    if request.endpoint not in excluded:
        if 'current_riddle' not in session and request.endpoint != 'next_riddle':
            return redirect(url_for('start_game'))

@app.route('/')
def home():
    session.clear()
    return render_template('index.html')

@app.route('/start')
def start_game():
    riddles = load_riddles()
    if not riddles:
        return redirect(url_for('home'))

    used_ids = session.get('used_ids', [])
    available_ids = [i for i in range(len(riddles)) if i not in used_ids]

    if not available_ids:
        session['used_ids'] = []
        available_ids = list(range(len(riddles)))

    selected_id = random.choice(available_ids)
    session.setdefault('used_ids', []).append(selected_id)

    session['current_riddle'] = {
        'id': selected_id,
        'text': riddles[selected_id]['riddle'],
        'answer': riddles[selected_id]['answer'].lower()
    }
    return redirect(url_for('play'))

@app.route('/play')
def play():
    result = session.pop('result', None)
    current = session.get('current_riddle')
    return render_template('index.html',
                         riddle_text=current['text'] if current else None,
                         result=result)

@app.route('/check/<path:user_answer>')
def check_answer(user_answer):
    try:
        # 单次解码修复乱码
        decoded_answer = unquote(user_answer).lower().strip()
    except:
        decoded_answer = ""

    correct_answer = session['current_riddle']['answer']
    result = {
        'is_correct': decoded_answer == correct_answer,
        'user_answer': decoded_answer,
        'correct_answer': correct_answer
    }
    session['result'] = result
    return redirect(url_for('play'))

@app.route('/next')
def next_riddle():
    session.pop('current_riddle', None)
    session.pop('result', None)
    return redirect(url_for('start_game'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
