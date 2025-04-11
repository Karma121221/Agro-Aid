import google.generativeai as genai

genai.configure(api_key="AIzaSyAPNqBA-Y0JNVdAZLB5sZoU7r14ZY1hCqU")

models = genai.list_models()
for m in models:
    print(m.name)
