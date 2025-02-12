import os
import random
import json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
DATA_FILE = 'riddles.json'

def load_riddles():
    """加载灯谜数据"""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def save_riddles(data):
    """保存灯谜数据"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route('/')
def home():
    """主页面"""
    return render_template('index.html', count=len(load_riddles()))

@app.route('/api/riddles', methods=['GET', 'POST'])
def handle_riddles():
    """灯谜API接口"""
    if request.method == 'GET':
        # 获取随机灯谜
        riddles = load_riddles()
        if not riddles:
            return jsonify({"error": "暂无灯谜，请先添加"})
        return jsonify(random.choice(riddles))

    elif request.method == 'POST':
        # 添加新灯谜
        data = request.json
        if not data.get('question') or not data.get('answer'):
            return jsonify({"error": "谜题和答案不能为空"}), 400

        riddles = load_riddles()
        riddles.append({
            "question": data['question'].strip(),
            "answer": data['answer'].strip().lower()
        })
        save_riddles(riddles)
        return jsonify({"message": "添加成功", "count": len(riddles)})

@app.route('/api/check', methods=['POST'])
def check_answer():
    """答案验证接口"""
    data = request.json
    riddles = load_riddles()

    for riddle in riddles:
        if riddle['question'] == data['question']:
            correct = (data['answer'].strip().lower() == riddle['answer'])
            return jsonify({"correct": correct, "answer": riddle['answer']})

    return jsonify({"error": "未找到对应灯谜"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)