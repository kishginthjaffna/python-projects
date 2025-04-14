from flask import Flask, render_template, request, jsonify
from main import fetch_tech_news

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.get_json()
    topic = data.get('url')  # The frontend sends the topic as 'url'
    
    if not topic:
        return jsonify({'error': 'No topic provided'}), 400

    try:
        summaries = fetch_tech_news(topic)
        if not summaries:
            return jsonify({'error': 'No relevant news found'}), 404
        return jsonify({'summaries': summaries})  # Return summaries as a JSON object
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
