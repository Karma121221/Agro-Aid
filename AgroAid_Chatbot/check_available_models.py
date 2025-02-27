import google.generativeai as genai

genai.configure(api_key="API KEY HERE")

models = genai.list_models()
for m in models:
    print(m.name)
