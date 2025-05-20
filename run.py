from flask import Flask, render_template, request, jsonify, session
from api.chatbot_service import ChatbotService
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = 'nigedease_secret_key'  # Change this in production
chatbot = ChatbotService()

@app.route('/')
def home():
    # Initialize session variables if not set
    if 'language' not in session:
        session['language'] = 'en'
    if 'demo_mode' not in session:
        session['demo_mode'] = False
    return render_template('index.html')

@app.route('/api/settings', methods=['GET'])
def get_settings():
    return jsonify({
        'language': session.get('language', 'en'),
        'demo_mode': session.get('demo_mode', False)
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    print(111)
    data = request.json
    user_message = data.get('message', '')
    language = data.get('language', session.get('language', 'en'))
    demo_mode = data.get('demo_mode', session.get('demo_mode', False))
    
    # Update session
    session['language'] = language
    session['demo_mode'] = demo_mode
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    try:
        result = chatbot.generate_response(user_message, language, demo_mode)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/settings', methods=['POST'])
def update_settings():
    data = request.json
    session['language'] = data.get('language', 'en')
    session['demo_mode'] = data.get('demo_mode', False)
    return jsonify({'status': 'success'})

@app.route('/api/reload_kb', methods=['POST'])
def reload_knowledge_base():
    try:
        chatbot.load_knowledge_base()
        return jsonify({'message': 'Knowledge base reloaded successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/analytics')
def analytics():
    stats = chatbot.get_analytics()
    return render_template('analytics.html', stats=stats)

if __name__ == '__main__':
    app.run(debug=True, port=5001)