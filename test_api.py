import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
print(f"API Key loaded: {api_key[:20]}...")

if api_key:
    genai.configure(api_key=api_key)
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content("Hello, test message", generation_config=genai.types.GenerationConfig(temperature=0.2, max_output_tokens=100))
        if response.text:
            print("✓ Gemini API working!")
            print(f"Response: {response.text[:100]}")
        else:
            print("✗ No response from Gemini")
    except Exception as e:
        print(f"✗ Error: {str(e)}")
else:
    print("✗ GEMINI_API_KEY not found")
