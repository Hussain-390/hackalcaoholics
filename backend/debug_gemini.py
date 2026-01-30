import os
import sys
from dotenv import load_dotenv

# Redirect all output to file
output = open("debug_output.txt", "w", encoding="utf-8")
sys.stdout = output
sys.stderr = output

load_dotenv()

print("Checking API Key...")
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("[ERROR] API Key NOT found!")
    output.close()
    sys.exit(1)

print(f"API Key found: {api_key[:10]}...{api_key[-4:]}")

print("\nTesting Gemini API...")
try:
    import google.generativeai as genai
    print("google.generativeai imported")
    
    genai.configure(api_key=api_key)
    print("API key configured")
    
    print("\nListing available models...")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"  - {m.name}")
    
    model = genai.GenerativeModel('gemini-pro')
    print("\nModel 'gemini-pro' created")
    
    response = model.generate_content("Say hello in 3 words")
    print(f"API call successful!")
    print(f"Response: {response.text}")
    print("\n[SUCCESS] All tests passed!")
    
except Exception as e:
    print(f"\n[ERROR] {e}")
    import traceback
    traceback.print_exc()

output.close()
