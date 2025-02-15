from flask import Flask, render_template, session, redirect, url_for
import json
import random
import os
from urllib.parse import unquote  # 新增解码库

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

# 修改路由和添加解码逻辑
@app.route('/check/<path:user_answer>')
def check_answer(user_answer):
    if 'current_riddle' not in session:
        return redirect(url_for('home'))

    correct = session['current_riddle']['answer']
    user_ans = unquote(user_answer).strip().lower()  # 添加解码处理
    result = {
        'is_correct': user_ans == correct,
        'user_answer': user_ans,
        'correct_answer': correct
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
