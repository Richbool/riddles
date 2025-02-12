import os
import json
import random
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = os.urandom(24)  # 安全会话密钥

# 数据文件路径
def get_riddles_path():
    return os.path.join(os.path.dirname(__file__), 'riddles.json')

# 初始化题库文件
def init_riddles_file():
    file_path = get_riddles_path()
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump([], f)

# 加载验证题库
def load_valid_riddles():
    file_path = get_riddles_path()
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            riddles = json.load(f)
        return [r for r in riddles if isinstance(r, dict) and r.get('riddle') and r.get('answer')]
    except:
        return []

@app.route('/')
def index():
    init_riddles_file()
    riddles = load_valid_riddles()
    return render_template('index.html', 
                         riddle_count=len(riddles),
                         current_riddle=session.get('current_riddle'))

@app.route('/add', methods=['POST'])
def add_riddle():
    riddle = request.form.get('riddle', '').strip()
    answer = request.form.get('answer', '').strip()
    
    if not riddle or not answer:
        return render_template('index.html', 
                             error="❌ 灯谜和答案不能为空！",
                             riddle_count=len(load_valid_riddles()))

    try:
        riddles = load_valid_riddles()
        riddles.append({'riddle': riddle, 'answer': answer})
        with open(get_riddles_path(), 'w', encoding='utf-8') as f:
            json.dump(riddles, f, ensure_ascii=False, indent=2)
    except Exception as e:
        return render_template('index.html',
                             error=f"❌ 保存失败：{str(e)}",
                             riddle_count=len(riddles))

    return redirect(url_for('index'))

@app.route('/guess', methods=['GET', 'POST'])
def guess_riddle():
    riddles = load_valid_riddles()
    
    if request.method == 'GET':
        if not riddles:
            return render_template('index.html',
                                 error="❌ 题库为空，请先添加灯谜！",
                                 riddle_count=0)
        selected = random.choice(riddles)
        session['current_riddle'] = selected['riddle']
        session['current_answer'] = selected['answer']
        return redirect(url_for('index'))

    elif request.method == 'POST':
        user_answer = request.form.get('answer', '').strip().lower()
        correct_answer = session.get('current_answer', '').lower()
        
        result = {
            'text': "✅ 猜对了！" if user_answer == correct_answer 
                   else f"❌ 正确答案：{session['current_answer']}",
            'is_correct': user_answer == correct_answer
        }
        return render_template('index.html',
                             result=result,
                             riddle_count=len(riddles),
                             current_riddle=session.get('current_riddle'))

if __name__ == '__main__':
    app.run(debug=True)
