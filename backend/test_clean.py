import os
from dotenv import load_dotenv

load_dotenv()

print("Checking API Key...")
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("[ERROR] API Key NOT found!")
    exit(1)

print(f"API Key found: {api_key[:10]}...{api_key[-4:]}")

print("\nTesting Gemini API...")
try:
    import google.generativeai as genai
    print("google.generativeai imported")
    
    genai.configure(api_key=api_key)
    print("API key configured")
    
    model = genai.GenerativeModel('gemini-1.5-flash')
    print("Model created")
    
    response = model.generate_content("Say hello")
    print(f"API call successful!")
    print(f"Response: {response.text}")
    print("\n[SUCCESS] All tests passed!")
    
except Exception as e:
    print(f"\n[ERROR] {e}")
    import traceback
    traceback.print_exc()
