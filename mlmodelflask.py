from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import os

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# Define the path to your model file (adjust the path if needed)
MODEL_PATH = os.path.join("Models", "CropRecommendation", "crop_recommendation_model.pkl")

# Load the crop recommendation model
try:
    with open(MODEL_PATH, "rb") as model_file:
        model = pickle.load(model_file)
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No input data provided'}), 400

        # Extract and convert input values
        try:
            nitrogen    = float(data['nitrogen'])
            phosphorus  = float(data['phosphorus'])
            potassium   = float(data['potassium'])
            temperature = float(data['temperature'])
            humidity    = float(data['humidity'])
            soil_ph     = float(data['ph'])
            rainfall    = float(data['rainfall'])
        except (KeyError, ValueError) as e:
            return jsonify({'error': f'Invalid input data: {e}'}), 400

        # Validate input ranges (matching the constraints in your HTML form)
        if not (0 <= nitrogen <= 300):
            return jsonify({'error': 'Nitrogen value out of range (0-300)'}), 400
        if not (0 <= phosphorus <= 200):
            return jsonify({'error': 'Phosphorus value out of range (0-200)'}), 400
        if not (0 <= potassium <= 250):
            return jsonify({'error': 'Potassium value out of range (0-250)'}), 400
        if not (-10 <= temperature <= 50):
            return jsonify({'error': 'Temperature value out of range (-10 to 50°C)'}), 400
        if not (0 <= humidity <= 100):
            return jsonify({'error': 'Humidity value out of range (0-100%)'}), 400
        if not (3.5 <= soil_ph <= 10):
            return jsonify({'error': 'Soil pH value out of range (3.5-10)'}), 400
        if not (0 <= rainfall <= 5000):
            return jsonify({'error': 'Rainfall value out of range (0-5000 mm/year)'}), 400

        # Ensure the model is loaded
        if model is None:
            return jsonify({'error': 'Model is not loaded.'}), 500

        # Prepare input features as a 2D array (shape: [1, 7])
        features = np.array([[nitrogen, phosphorus, potassium, temperature, humidity, soil_ph, rainfall]])
        
        # Make a prediction using your ML model
        prediction = model.predict(features)
        predicted_crop = prediction[0]

        return jsonify({'crop': predicted_crop})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Run the Flask server on port 5000 in debug mode
    app.run(debug=True, port=5000)
