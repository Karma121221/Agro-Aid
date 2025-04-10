from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import joblib
import numpy as np
import os
import pandas as pd

app = Flask(__name__)
CORS(app)

# Load Crop Recommendation Model
CROP_RECOMMENDATION_MODEL_PATH = os.path.join("Models", "CropRecommendation", "crop_recommendation_model.pkl")
try:
    with open(CROP_RECOMMENDATION_MODEL_PATH, "rb") as model_file:
        crop_recommendation_model = pickle.load(model_file)
    print("Crop recommendation model loaded successfully.")
except Exception as e:
    print(f"Error loading crop recommendation model: {e}")
    crop_recommendation_model = None

# Load Crop Yield Prediction Model using joblib
YIELD_PREDICTION_MODEL_PATH = os.path.join("Models", "YieldbyProduction", "best_rf_yield.pkl")
try:
    yield_model_pipeline = joblib.load(YIELD_PREDICTION_MODEL_PATH)
    print("Crop yield prediction model loaded successfully.")
    print("Loaded yield_model_pipeline type:", type(yield_model_pipeline))
except Exception as e:
    print(f"Error loading yield prediction model: {e}")
    yield_model_pipeline = None

# Crop Recommendation Endpoint
@app.route('/predict', methods=['POST'])
def recommend_crop():
    try:
        data = request.get_json()
        nitrogen    = float(data['nitrogen'])
        phosphorus  = float(data['phosphorus'])
        potassium   = float(data['potassium'])
        temperature = float(data['temperature'])
        humidity    = float(data['humidity'])
        soil_ph     = float(data['ph'])
        rainfall    = float(data['rainfall'])

        if crop_recommendation_model is None:
            return jsonify({'error': 'Crop recommendation model not loaded.'}), 500

        features = np.array([[nitrogen, phosphorus, potassium, temperature, humidity, soil_ph, rainfall]])
        prediction = crop_recommendation_model.predict(features)
        return jsonify({'crop': prediction[0]})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Yield Prediction Endpoint
@app.route('/predict-yield', methods=['POST'])
def predict_yield():
    try:
        data = request.get_json()

        land_area = float(data['land_area'])  # in hectares
        production = float(data['production'])  # in tonnes
        state = data['state']
        crop = data['crop']
        district = data['district']
        season = data['season']

        if yield_model_pipeline is None:
            return jsonify({'error': 'Yield prediction model not loaded.'}), 500

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
        return jsonify({'error': str(e)}), 500

# ----------------------
# Start the Flask App
# ----------------------
if __name__ == '__main__':
    app.run(debug=True, port=5000)
