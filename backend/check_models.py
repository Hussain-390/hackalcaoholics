
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("Error: GEMINI_API_KEY not found in .env")
    exit(1)

genai.configure(api_key=api_key)


with open("models_list.txt", "w", encoding="utf-8") as f:
    f.write(f"Checking models with key: {api_key[:5]}...{api_key[-5:]}\n")
    f.write(f"Library version: {genai.__version__}\n")
    try:
        f.write("\nListing available models:\n")
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                f.write(f"- {m.name}\n")
    except Exception as e:
        f.write(f"Error listing models: {e}\n")

