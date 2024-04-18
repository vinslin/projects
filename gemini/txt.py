import google.generativeai as genai

# Replace with your actual API key
api_key = "AIzaSyBSlif-91q43MbqYypAxPnshlKIbFGAT2c"
genai.configure(api_key=api_key)

# Choose the model you want to use
model_name = "gemini-pro"  # For text-only prompts
# model_name = "gemini-pro-vision"  # For text and images prompts

# Create the model instance
model = genai.GenerativeModel(model_name)

# Prompt to send to the model
prompt = "Write a poem about a starry night."

# Generate the content
response = model.generate_content(prompt)

# Print the generated text
print("Generated text:")
print(response.text)
