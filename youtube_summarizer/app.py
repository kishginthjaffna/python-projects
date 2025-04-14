from flask import Flask, render_template, request, jsonify
from main import summarize_youtube_video  # Import the summarize_youtube_video function from main.py

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/summarize", methods=["POST"])
def summarize():
    try:
        data = request.get_json()  
        url = data.get("url")

        if not url:
            return jsonify({"error": "YouTube video URL is required."}), 400

        
        if "watch?v=" in url:
            video_id = url.split("watch?v=")[-1].split("&")[0]
        else:
            video_id = url.strip()

        summary = summarize_youtube_video(video_id)

        return jsonify({"summary": summary})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
