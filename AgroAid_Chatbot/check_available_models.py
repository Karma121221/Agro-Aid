import google.generativeai as genai

genai.configure(api_key="API")

models = genai.list_models()
for m in models:
    print(m.name)
