from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS 
import google.generativeai as genai
import re
import pickle
import joblib
import numpy as np
import os
import pandas as pd

# Initialize Flask app
app = Flask(__name__, static_folder=".", static_url_path="")
CORS(app)

# ==================== CONFIGURATION ====================
# Get API key from environment variable
API_KEY = os.environ.get('GOOGLE_API_KEY', 'API')
genai.configure(api_key=API_KEY)

# ==================== MODEL LOADING ====================

# Load Crop Recommendation Model
CROP_RECOMMENDATION_MODEL_PATH = os.path.join("Models", "CropRecommendation", "crop_recommendation_model.pkl")
try:
    with open(CROP_RECOMMENDATION_MODEL_PATH, "rb") as model_file:
        crop_recommendation_model = pickle.load(model_file)
    print("✓ Crop recommendation model loaded successfully.")
except Exception as e:
    print(f"✗ Error loading crop recommendation model: {e}")
    crop_recommendation_model = None

# Load Crop Yield Prediction Model
YIELD_PREDICTION_MODEL_PATH = os.path.join("Models", "YieldbyProduction", "best_rf_yield.pkl")
try:
    yield_model_pipeline = joblib.load(YIELD_PREDICTION_MODEL_PATH)
    print("✓ Crop yield prediction model loaded successfully.")
except Exception as e:
    print(f"✗ Error loading yield prediction model: {e}")
    print("  The /predict-yield endpoint will return an error until this model is available.")
    yield_model_pipeline = None

# Load Soil Fertility Model
SOIL_FERTILITY_MODEL_PATH = os.path.join('Models', 'Soil-Quality-Fertility-Prediction', 'random_forest_pkl.pkl')
try:
    with open(SOIL_FERTILITY_MODEL_PATH, 'rb') as f:
        soil_fertility_model = pickle.load(f)
    print("✓ Soil fertility model loaded successfully.")
except Exception as e:
    print(f"✗ Error loading soil fertility model: {e}")
    soil_fertility_model = None

# ==================== HELPER FUNCTIONS ====================

def agro_aid_chatbot(user_input):
    """Process chatbot requests using Google Gemini AI"""
    try:
        model = genai.GenerativeModel("models/gemini-2.5-flash")
        response = model.generate_content(user_input)
        formatted_response = format_text(response.text) if response.text else "I'm sorry, I couldn't understand that."
        return formatted_response
    except Exception as e:
        print(f"Chatbot error: {e}")
        return "I'm experiencing technical difficulties. Please try again later."

def format_text(text):
    """Format chatbot response text"""
    text = re.sub(r'\*+', '', text)
    text = re.sub(r'\s+', ' ', text).strip() 
    formatted_text = re.sub(r'(?<!• )([A-Za-z ]+):', r'\n• \1:', text)  
    return formatted_text.strip()

# ==================== STATIC FILE ROUTES ====================

@app.route("/")
def serve_home():
    """Serve the home page"""
    return send_from_directory(".", "index.html")

@app.route("/<path:path>")
def serve_static_files(path):
    """Serve static files (CSS, JS, images, etc.)"""
    return send_from_directory(".", path)

# ==================== API ENDPOINTS ====================

@app.route("/chat", methods=["POST"])
def chat():
    """Chatbot endpoint using Google Gemini AI"""
    try:
        data = request.json  
        user_input = data.get("message", "").strip()
        
        if not user_input:
            return jsonify({"reply": "Please provide a message."})
        
        bot_response = agro_aid_chatbot(user_input) 
        return jsonify({"reply": bot_response})
    except Exception as e:
        print(f"Chat endpoint error: {e}")
        return jsonify({"reply": "An error occurred processing your message."}), 500

@app.route('/predict', methods=['POST'])
def recommend_crop():
    """Crop recommendation endpoint"""
    try:
        if crop_recommendation_model is None:
            return jsonify({'error': 'Crop recommendation model not loaded.'}), 500
        
        data = request.get_json()
        nitrogen    = float(data['nitrogen'])
        phosphorus  = float(data['phosphorus'])
        potassium   = float(data['potassium'])
        temperature = float(data['temperature'])
        humidity    = float(data['humidity'])
        soil_ph     = float(data['ph'])
        rainfall    = float(data['rainfall'])

        features = np.array([[nitrogen, phosphorus, potassium, temperature, humidity, soil_ph, rainfall]])
        prediction = crop_recommendation_model.predict(features)
        return jsonify({'crop': prediction[0]})
    
    except Exception as e:
        print(f"Crop prediction error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/predict-yield', methods=['POST'])
def predict_yield():
    """Yield prediction endpoint"""
    try:
        if yield_model_pipeline is None:
            return jsonify({
                'error': 'Yield prediction model not loaded. Please contact the administrator.',
                'details': 'The best_rf_yield.pkl model file is missing from the Models/YieldbyProduction directory.'
            }), 503
        
        data = request.get_json()
        
        land_area = float(data['land_area'])  # in hectares
        production = float(data['production'])  # in tonnes
        state = data['state']
        crop = data['crop']
        district = data['district']
        season = data['season']

        input_data = {
            'Land area utilized for production': [land_area],
            'Crop production': [production],
            'srcStateName': [state],
            'Crop name': [crop],
            'srcDistrictName': [district],
            'Crop season': [season],
        }
        df = pd.DataFrame(input_data)
        prediction = yield_model_pipeline.predict(df)
        return jsonify({'yield': prediction[0]})
    
    except Exception as e:
        print(f"Yield prediction error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/soil_fertility_predict', methods=['POST'])
def predict_soil_fertility():
    """Soil fertility prediction endpoint"""
    try:
        if soil_fertility_model is None:
            return jsonify({"error": "Soil fertility model not loaded"}), 500
        
        data = request.json
        
        if not data:
            return jsonify({"error": "No data received"}), 400

        required_fields = ['nitrogen', 'phosphorus', 'potassium', 'ph', 'ec', 'oc', 's', 'zn', 'fe', 'cu', 'mn', 'b']
        
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({"error": f"Missing required fields: {missing_fields}"}), 400
        
        # Extract features in the correct order
        try:
            features = [float(data[field]) for field in required_fields]
        except ValueError as e:
            return jsonify({"error": "Invalid numeric value provided"}), 400
        
        # Make prediction
        features_array = np.array(features).reshape(1, -1)
        prediction = soil_fertility_model.predict(features_array)[0]
        numeric_prediction = int(prediction)
        
        fertility_levels = {
            0: "Less Fertile",
            1: "Fertile",
            2: "Highly Fertile"
        }
        
        result = {
            "fertility": fertility_levels.get(numeric_prediction, "Unknown"),
            "numeric_prediction": numeric_prediction
        }
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Soil fertility prediction error: {e}")
        return jsonify({"error": str(e)}), 500

# ==================== HEALTH CHECK ====================

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring"""
    models_status = {
        "crop_recommendation": crop_recommendation_model is not None,
        "yield_prediction": yield_model_pipeline is not None,
        "soil_fertility": soil_fertility_model is not None
    }
    return jsonify({
        "status": "healthy",
        "models": models_status
    })

# ==================== START APPLICATION ====================

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    print(f"\n🌱 Agro-Aid Server Starting...")
    print(f"📍 Running on port: {port}")
    print(f"🔑 API Key configured: {'Yes' if API_KEY != 'API' else 'No (using placeholder)'}")
    print(f"\nModel Status:")
    print(f"  Crop Recommendation: {'✓ Loaded' if crop_recommendation_model else '✗ Not loaded'}")
    print(f"  Yield Prediction: {'✓ Loaded' if yield_model_pipeline else '✗ Not loaded'}")
    print(f"  Soil Fertility: {'✓ Loaded' if soil_fertility_model else '✗ Not loaded'}")
    print(f"\n🚀 Server ready!\n")
    
    app.run(host='0.0.0.0', port=port, debug=False)
