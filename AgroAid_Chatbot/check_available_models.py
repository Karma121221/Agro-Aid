import google.generativeai as genai

genai.configure(api_key="PUT API HERE")

models = genai.list_models()
for m in models:
    print(m.name)
