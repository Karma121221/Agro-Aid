import requests
import datetime as dt
import pandas as pd
import pickle

# Constants
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
API_KEY = '43d8484111b238514fc86737aba0ba2f'  # Replace with your actual API key
MODEL_PATH = r"D:\vs-code\EPICS AgroAid\training_data\crop_recommendation_model.pkl"

# Load the trained model
with open(MODEL_PATH, 'rb') as file:
    model = pickle.load(file)

print("Model loaded successfully!")

# Function to fetch weather data from the API
def fetch_weather_data(city):
    url = BASE_URL + "appid=" + API_KEY + "&q=" + city
    response = requests.get(url).json()
    
    if response['cod'] != 200:
        print(f"Error: {response['message']}")
        return None
    return response

# Function to parse API response and extract relevant weather data
def parse_api_response(response):
    try:
        # Extract temperature
        temp_kelvin = response['main']['temp']
        temp_celsius = temp_kelvin - 273.15
        temp_fahrenheit = temp_celsius * (9/5) + 32

        # Extract "feels like" temperature
        feels_like_kelvin = response['main']['feels_like']
        feels_like_celsius = feels_like_kelvin - 273.15
        feels_like_fahrenheit = feels_like_celsius * (9/5) + 32

        # Extract wind speed, humidity, and weather description
        wind_speed = response['wind']['speed']
        humidity = response['main']['humidity']
        description = response['weather'][0]['description']

        # Convert sunrise and sunset times to local time
        sunrise_time = dt.datetime.utcfromtimestamp(response['sys']['sunrise'] + response['timezone'])
        sunset_time = dt.datetime.utcfromtimestamp(response['sys']['sunset'] + response['timezone'])

        return {
            "Temperature": temp_celsius,
            "Feels_Like": feels_like_celsius,
            "Wind_Speed": wind_speed,
            "Humidity": humidity,
            "Description": description,
            "Sunrise": sunrise_time,
            "Sunset": sunset_time
        }
    except Exception as e:
        print("Error parsing API response:", e)
        return None

# Function to make crop recommendation
def recommend_crop(weather_data, nitrogen, phosphorus, potassium, ph_value, rainfall=0):  # Default rainfall to 0
    # Create DataFrame from weather data and soil inputs
    data = pd.DataFrame([{
        "Nitrogen": nitrogen,
        "Phosphorus": phosphorus,
        "Potassium": potassium,
        "Temperature": weather_data["Temperature"],
        "Humidity": weather_data["Humidity"],
        "pH_Value": ph_value,  # Updated to match model's feature
        "Rainfall": rainfall   # Use default value if no input
    }])

    # Ensure columns match model features
    data = data[["Nitrogen", "Phosphorus", "Potassium", "Temperature", "Humidity", "pH_Value", "Rainfall"]]

    # Use the model to predict the recommended crop
    try:
        predicted_crop = model.predict(data)
        return predicted_crop[0]
    except Exception as e:
        print("Error making prediction:", e)
        return None

# Main script
def main():
    # Get city name from user
    city = input("Enter your city: ")

    # Fetch weather data from the API
    response = fetch_weather_data(city)
    if response:
        weather_data = parse_api_response(response)
        print(f"Weather Data for {city}:")
        print(f"Temperature: {weather_data['Temperature']:.2f}°C")
        print(f"Feels Like: {weather_data['Feels_Like']:.2f}°C")
        print(f"Humidity: {weather_data['Humidity']}%")
        print(f"Wind Speed: {weather_data['Wind_Speed']} m/s")
        print(f"Weather: {weather_data['Description']}")
        print(f"Sunrise: {weather_data['Sunrise']}")
        print(f"Sunset: {weather_data['Sunset']}")

        # Ask user for additional soil data
        nitrogen = float(input("Nitrogen (N) content in soil: "))
        phosphorus = float(input("Phosphorus (P) content in soil: "))
        potassium = float(input("Potassium (K) content in soil: "))
        ph_value = float(input("Soil pH value: "))

        # Default rainfall value (0)
        rainfall = 0  # You can ask the user for rainfall or use a default

        # Get crop recommendation
        crop = recommend_crop(weather_data, nitrogen, phosphorus, potassium, ph_value, rainfall)
        if crop:
            print(f"The recommended crop for your region and soil is: {crop}")
        else:
            print("Could not make a crop recommendation.")
    else:
        print("Failed to fetch weather data.")

if __name__ == "__main__":
    main()
