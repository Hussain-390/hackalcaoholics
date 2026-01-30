import os
import sys
from dotenv import load_dotenv

load_dotenv()

#  Redirect output to file  
output_file = open("test_output.txt", "w")
sys.stdout = output_file
sys.stderr = output_file

print("🔑 Checking API Key...")
api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    print(f"✅ API Key found: {api_key[:10]}...{api_key[-4:]}")
else:
    print("❌ API Key NOT found!")
    output_file.close()
    sys.exit(1)

print("\n🧪 Testing Gemini API...")
try:
    import google.generativeai as genai
    print("✅ google.generativeai imported")
    
    genai.configure(api_key=api_key)
    print("✅ API key configured")
    
    # List available models
    print("\n📋 Listing available models...")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"  - {m.name}")
    
    model = genai.GenerativeModel('gemini-1.5-flash')
    print(f"\n✅ Model 'gemini-1.5-flash' created")
    
    response = model.generate_content("Say hello in 3 words")
    print(f"✅ API call successful!")
    print(f"Response: {response.text}")
    
    print("\n✅ ALL TESTS PASSED!")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()

output_file.close()
print("Output written to test_output.txt")
