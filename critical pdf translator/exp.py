import argostranslate

# Load the translator
translator = argostranslate.Translator.load("en", "ta")  # English to Tamil translation

# Perform translation
english_text = "Hello, how are you?"
tamil_translation = translator.translate(english_text)
print(tamil_translation)
