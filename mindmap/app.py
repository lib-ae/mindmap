from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import json
import os
import sys
from datetime import datetime
from ai_utils import AIAssistant

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", os.urandom(24).hex())

# 初始化AI助手（不传API密钥，将在每个请求中从前端获取）
ai_assistant = AIAssistant()

# 确保数据目录存在
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# 确保对话历史目录存在
CHAT_DIR = os.path.join(DATA_DIR, 'chats')
if not os.path.exists(CHAT_DIR):
    os.makedirs(CHAT_DIR)

def get_mindmaps():
    """获取所有思维导图列表"""
    mindmaps = []
    if os.path.exists(DATA_DIR):
        for filename in os.listdir(DATA_DIR):
            if filename.endswith('.json'):
                map_id = filename[:-5]  # 移除 .json 扩展名
                try:
                    with open(os.path.join(DATA_DIR, filename), 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        mindmaps.append({
                            'id': map_id,
                            'title': data.get('title', 'Untitled'),
                            'updated_at': data.get('updated_at', '')
                        })
                except:
                    continue
    return sorted(mindmaps, key=lambda x: x.get('updated_at', ''), reverse=True)

@app.route('/')
def index():
    """首页，显示思维导图列表"""
    mindmaps = get_mindmaps()
    return render_template('index.html', mindmaps=mindmaps)

@app.route('/mindmap/new')
def new_mindmap():
    """创建新的思维导图"""
    map_id = datetime.now().strftime('%Y%m%d%H%M%S')
    return redirect(url_for('edit_mindmap', map_id=map_id))

@app.route('/mindmap/<map_id>')
def edit_mindmap(map_id):
    """编辑思维导图"""
    return render_template('mindmap.html', map_id=map_id)

@app.route('/api/mindmap/<map_id>', methods=['GET'])
def get_mindmap(map_id):
    """获取思维导图数据"""
    file_path = os.path.join(DATA_DIR, f"{map_id}.json")
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return jsonify(json.load(f))
    else:
        # 返回新的空思维导图
        return jsonify({
            'title': 'Untitled Mindmap',
            'nodes': [],
            'links': [],
            'updated_at': datetime.now().isoformat()
        })

@app.route('/api/mindmap/<map_id>', methods=['POST'])
def save_mindmap(map_id):
    """保存思维导图数据"""
    data = request.json
    data['updated_at'] = datetime.now().isoformat()
    
    file_path = os.path.join(DATA_DIR, f"{map_id}.json")
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return jsonify({'success': True})

@app.route('/api/mindmap/<map_id>/delete', methods=['POST'])
def delete_mindmap(map_id):
    """删除思维导图"""
    file_path = os.path.join(DATA_DIR, f"{map_id}.json")
    if os.path.exists(file_path):
        os.remove(file_path)
    return jsonify({'success': True})

# 新增AI相关路由

@app.route('/ai-assistant')
def ai_assistant_page():
    """AI助手页面"""
    return render_template('ai_assistant.html')

@app.route('/settings')
def settings_page():
    """设置页面"""
    return render_template('settings.html')

@app.route('/api/update-settings', methods=['POST'])
def update_settings():
    """更新设置（仅会话期间有效）"""
    data = request.json
    api_key = data.get('api_key', '')
    use_mock_data = data.get('use_mock_data', True)
    
    # 仅在会话中保存，不存储到服务器上
    session['api_key'] = api_key
    session['use_mock_data'] = use_mock_data
    
    return jsonify({'success': True})

@app.route('/api/expand-idea', methods=['POST'])
def expand_idea():
    """AI扩展想法"""
    data = request.json
    idea = data.get('idea', '')
    use_mock_data = data.get('use_mock_data', True)
    
    # 从请求头获取API密钥
    api_key = request.headers.get('X-API-KEY', '')
    
    if not idea:
        return jsonify({'error': '想法不能为空'}), 400
        
    # 创建一个新的AI助手实例（使用请求中的API密钥）
    temp_assistant = AIAssistant(api_key=api_key)
    
    # 调用AI助手扩展想法
    if use_mock_data or not api_key or api_key.strip() == "":
        # 使用模拟数据
        expanded = temp_assistant._mock_expand_idea(idea)
    else:
        # 使用真实API
        expanded = temp_assistant.expand_idea(idea)
    
    return jsonify(expanded)

@app.route('/api/chat', methods=['POST'])
def chat():
    """与AI对话"""
    data = request.json
    message = data.get('message', '')
    chat_id = data.get('chat_id', datetime.now().strftime('%Y%m%d%H%M%S'))
    use_mock_data = data.get('use_mock_data', True)
    
    # 从请求头获取API密钥
    api_key = request.headers.get('X-API-KEY', '')
    
    if not message:
        return jsonify({'error': '消息不能为空'}), 400
        
    # 获取对话历史
    chat_history = get_chat_history(chat_id)
    
    # 添加用户消息
    chat_history.append({"role": "user", "content": message})
    
    # 创建一个新的AI助手实例（使用请求中的API密钥）
    temp_assistant = AIAssistant(api_key=api_key)
    
    # 调用AI助手获取回复
    if use_mock_data or not api_key or api_key.strip() == "":
        # 使用模拟数据
        ai_response = temp_assistant._mock_chat(chat_history)
    else:
        # 使用真实API
        ai_response = temp_assistant.chat(chat_history)
    
    # 添加AI回复到历史
    chat_history.append({"role": "assistant", "content": ai_response})
    
    # 保存对话历史
    save_chat_history(chat_id, chat_history)
    
    return jsonify({
        'message': ai_response,
        'chat_id': chat_id
    })

@app.route('/api/chat/<chat_id>', methods=['GET'])
def get_chat(chat_id):
    """获取对话历史"""
    chat_history = get_chat_history(chat_id)
    return jsonify({'history': chat_history})

@app.route('/api/create-mindmap-from-idea', methods=['POST'])
def create_mindmap_from_idea():
    """从AI扩展的想法创建思维导图"""
    data = request.json
    expanded_idea = data.get('expanded_idea', {})
    
    if not expanded_idea:
        return jsonify({'error': '扩展想法数据不能为空'}), 400
        
    # 创建新的思维导图ID
    map_id = datetime.now().strftime('%Y%m%d%H%M%S')
    
    # 构建思维导图结构
    mindmap_data = {
        'title': expanded_idea.get('title', 'AI扩展想法'),
        'updated_at': datetime.now().isoformat(),
        'nodes': [
            {
                'id': 'root',
                'text': expanded_idea.get('title', 'AI扩展想法'),
                'x': 400,
                'y': 300,
                'color': '#ff9900',
                'shape': 'ellipse'
            }
        ],
        'links': []
    }
    
    # 添加相关概念节点
    related_concepts = expanded_idea.get('related_concepts', [])
    for i, concept in enumerate(related_concepts):
        node_id = f'concept-{i}'
        mindmap_data['nodes'].append({
            'id': node_id,
            'text': concept,
            'x': 400 + (i+1) * 150 * (-1 if i % 2 == 0 else 1),
            'y': 300 - 100 - (i // 2) * 80,
            'color': '#66ccff',
            'shape': 'rectangle'
        })
        mindmap_data['links'].append({
            'source': 'root',
            'target': node_id
        })
    
    # 添加行动项节点
    action_items = expanded_idea.get('action_items', [])
    for i, action in enumerate(action_items):
        node_id = f'action-{i}'
        mindmap_data['nodes'].append({
            'id': node_id,
            'text': action,
            'x': 400 + (i+1) * 160 * (-1 if i % 2 == 0 else 1),
            'y': 300 + 100 + (i // 2) * 80,
            'color': '#99cc66',
            'shape': 'rectangle'
        })
        mindmap_data['links'].append({
            'source': 'root',
            'target': node_id
        })
    
    # 保存思维导图
    file_path = os.path.join(DATA_DIR, f"{map_id}.json")
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(mindmap_data, f, ensure_ascii=False, indent=2)
    
    return jsonify({
        'success': True,
        'map_id': map_id
    })

def get_chat_history(chat_id):
    """获取对话历史"""
    file_path = os.path.join(CHAT_DIR, f"{chat_id}.json")
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def save_chat_history(chat_id, history):
    """保存对话历史"""
    file_path = os.path.join(CHAT_DIR, f"{chat_id}.json")
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    # 确保在正确的工作目录下运行
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # 启动Flask应用
    print("正在启动思维导图应用，请访问 http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000) 