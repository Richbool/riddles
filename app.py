import os
import random
from flask import Flask, render_template, request, session, redirect, url_for
import json

app = Flask(__name__)
app.secret_key = os.urandom(24)  # 使用强加密密钥
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

RIDDLE_FILE = 'riddles.json'

def load_riddles():
    if not os.path.exists(RIDDLE_FILE):
        return []
    with open(RIDDLE_FILE, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_riddle(riddle, answer):
    with open(RIDDLE_FILE, 'a+', encoding='utf-8') as f:
        f.seek(0)
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = []
        data.append({"riddle": riddle, "answer": answer.lower()})
        f.seek(0)
        json.dump(data, f, ensure_ascii=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        riddle = request.form.get('riddle', '').strip()
        answer = request.form.get('answer', '').strip()

        if not riddle or not answer:
            return render_template('index.html',
                                 error="❌ 灯谜和答案都不能为空！",
                                 riddles=load_riddles())

        save_riddle(riddle, answer)
        return redirect(url_for('index'))

    return render_template('index.html', riddles=load_riddles())

@app.route('/guess', methods=['GET', 'POST'])
def guess_riddle():
    riddles = load_riddles()

    # 处理获取新题目
    if request.method == 'GET':
        if not riddles:
            return render_template('index.html',
                                 error="❌ 题库为空，请先添加灯谜！",
                                 riddles=[])

        selected = random.choice(riddles)
        # 生成唯一题号防止重复
        session['current_riddle_id'] = riddles.index(selected)
        session['expected_answer'] = selected['answer'].lower()
        return render_template('index.html',
                             current_riddle=selected['riddle'],
                             riddles=riddles)

    # 处理答案提交
    if request.method == 'POST':
        # 防御性检查
        if 'expected_answer' not in session:
            return redirect(url_for('guess_riddle'))

        user_answer = request.form.get('answer', '').strip().lower()
        correct_answer = session.pop('expected_answer', None)
        riddle_id = session.get('current_riddle_id')

        # 验证题库一致性
        if not (0 <= riddle_id < len(riddles)):
            session.clear()
            return redirect(url_for('index'))

        result = {
            'is_correct': user_answer == correct_answer,
            'correct_answer': riddles[riddle_id]['answer'],
            'user_answer': user_answer
        }
        session.pop('current_riddle_id', None)

        return render_template('index.html',
                             result=result,
                             riddles=riddles,
                             current_riddle=riddles[riddle_id]['riddle'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
