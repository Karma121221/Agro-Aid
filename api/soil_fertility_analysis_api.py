from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import pickle
import os

app = Flask(__name__)
CORS(app)

# Load the soil fertility model
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'Models', 'Soil-Quality-Fertility-Prediction', 'random_forest_pkl.pkl')

try:
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    print("Model loaded successfully from:", MODEL_PATH)
except Exception as e:
    print(f"Error loading model: {str(e)}")
    model = None

@app.route('/soil_fertility_predict', methods=['POST'])
def predict():
    if model is None:
        print("Error: Model not loaded")
        return jsonify({"error": "Model not loaded"}), 500
        
    try:
        data = request.json
        print("Received data:", data)
        
        if not data:
            print("Error: No data received")
            return jsonify({"error": "No data received"}), 400

        required_fields = ['nitrogen', 'phosphorus', 'potassium', 'ph', 'ec', 'oc', 's', 'zn', 'fe', 'cu', 'mn', 'b']
        
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            print(f"Error: Missing fields: {missing_fields}")
            return jsonify({"error": f"Missing required fields: {missing_fields}"}), 400
            
        # Extract features in the correct order
        try:
            features = [float(data[field]) for field in required_fields]
        except ValueError as e:
            print(f"Error converting values: {str(e)}")
            return jsonify({"error": "Invalid numeric value provided"}), 400
        
        # Make prediction
        features_array = np.array(features).reshape(1, -1)
        print("Feature array shape:", features_array.shape)
        print("Feature values:", features_array)
        
        prediction = model.predict(features_array)[0]
        print("Raw prediction:", prediction)
        
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
        
        print("Prediction result:", result)
        return jsonify(result)
        
    except Exception as e:
        print("Error during prediction:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
