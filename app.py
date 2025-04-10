from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS 
import google.generativeai as genai
import re 

API_KEY = "API"
genai.configure(api_key=API_KEY)

app = Flask(__name__, static_folder="Agro-Aid", static_url_path="/Agro-Aid")
CORS(app)

def agro_aid_chatbot(user_input):
    model = genai.GenerativeModel("models/gemini-2.0-flash")
    response = model.generate_content(user_input)
    formatted_response = format_text(response.text) if response.text else "I'm sorry, I couldn't understand that."
    return formatted_response

def format_text(text):
    text = re.sub(r'\*+', '', text)
    text = re.sub(r'\s+', ' ', text).strip() 

    formatted_text = re.sub(r'(?<!• )([A-Za-z ]+):', r'\n• \1:', text)  

    return formatted_text.strip()

@app.route("/")
def serve_home():
    return send_from_directory(".", "index.html")

@app.route("/<path:path>")
def serve_static_files(path):
    return send_from_directory(".", path)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json  
    user_input = data.get("message", "").strip()
    if not user_input:
        return jsonify({"reply": "Please provide a message."})

    bot_response = agro_aid_chatbot(user_input) 
    return jsonify({"reply": bot_response}) 

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5500, debug=True)
