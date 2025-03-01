from flask import Flask, request, jsonify, render_template
from chatbot import answer_howto_question

app = Flask(__name__)

@app.route('/')
def index():
    """Render the main chat interface."""
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    """Process user questions and return chatbot responses."""
    try:
        data = request.get_json()
        if not data or 'question' not in data:
            return jsonify({'error': 'No question provided'}), 400
        
        question = data['question']
        answer = answer_howto_question(question)
        
        return jsonify({'response': answer})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
