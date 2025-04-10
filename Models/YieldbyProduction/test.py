import pickle
import pandas as pd

with open("Models/YieldbyProduction/best_rf_yield.pkl", "rb") as f:
    model = pickle.load(f)

sample_data = pd.DataFrame({
    'Land area utilized for production': [2.5],
    'Crop production': [500],
    'srcStateName': ['GUJARAT'],
    'Crop name': ['Wheat'],
    'srcDistrictName': ['SomeDistrict'],
    'Crop season': ['Kharif'],
})
prediction = model.predict(sample_data)
print("Prediction:", prediction)
