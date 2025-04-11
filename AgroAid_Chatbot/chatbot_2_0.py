import google.generativeai as genai
from gtts import gTTS
import IPython.display as display
import re  # Import regex for text cleaning

API_KEY = "AIzaSyAPNqBA-Y0JNVdAZLB5sZoU7r14ZY1hCqU"  # Replace with your actual Gemini API key
genai.configure(api_key=API_KEY)

def agro_aid_chatbot(user_input):
    model = genai.GenerativeModel("models/gemini-2.0-flash")
    response = model.generate_content(user_input)
    cleaned_response = clean_text(response.text)  # Clean the text output
    return cleaned_response

def clean_text(text):
    text = re.sub(r'\*+', '', text)  # Remove asterisks (*** or **)
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces
    return text

def speak_text(text, language="auto"):
    if language == "auto":
        language = "hi" if any("\u0900" <= char <= "\u097F" for char in text) else "en"

    tts = gTTS(text=text, lang=language, slow=False)  # Use detected language
    tts.save("response.mp3")
    display.display(display.Audio("response.mp3", autoplay=True))

while True:
    user_input = input("\nYou: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Chatbot: Goodbye!")
        break

    response = agro_aid_chatbot(user_input)
    print(f"Chatbot: {response}")

    speak_text(response)  # Speak the cleaned response in Hindi or English
