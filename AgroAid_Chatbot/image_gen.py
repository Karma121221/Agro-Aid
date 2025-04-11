import google.generativeai as genai

# Set your API key
GOOGLE_API_KEY = "AIzaSyAPNqBA-Y0JNVdAZLB5sZoU7r14ZY1hCqU"
genai.configure(api_key=GOOGLE_API_KEY)

# Select the model
model = genai.GenerativeModel("models/imagen-3.0-generate-002")

# Define the prompt for image generation
prompt = "A futuristic city skyline at sunset with flying cars"

# Generate the image
response = model.generate_content(prompt)

# Save the generated image
if response and hasattr(response, "images"):
    image = response.images[0]
    image.save("generated_image.png")
    print("Image saved as generated_image.png")
else:
    print("Failed to generate image.")
