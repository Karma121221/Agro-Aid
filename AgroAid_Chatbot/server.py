from flask import Flask, request, jsonify
from flask_cors import CORS  # Enable CORS for frontend requests
import google.generativeai as genai
import re  # For text cleaning

# Configure Gemini API (Replace with your valid API key)
API_KEY = "AIzaSyAO7QHEB2fH1uVsAuhVjp6NCKT1v_DzQRQ"
genai.configure(api_key=API_KEY)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Function to process user input and get chatbot response
def agro_aid_chatbot(user_input):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(user_input)
    formatted_response = format_text(response.text) if response.text else "I'm sorry, I couldn't understand that."
    return formatted_response

# Function to clean and format chatbot response
def format_text(text):
    text = re.sub(r'\*+', '', text)  # Remove asterisks (*** or **)
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces

    # Use regex to insert line breaks before categories
    formatted_text = re.sub(r'(?<!• )([A-Za-z ]+):', r'\n• \1:', text)  

    return formatted_text.strip()

# API endpoint for chatbot
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json  # Get user input from JSON request
    user_input = data.get("message", "").strip()  # Extract and clean message
    if not user_input:
        return jsonify({"reply": "Please provide a message."})

    bot_response = agro_aid_chatbot(user_input)  # Get chatbot reply
    return jsonify({"reply": bot_response})  # Return JSON response

# Run the Flask server
if __name__ == "__main__":
    app.run(debug=True)
