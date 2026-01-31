import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-flash-latest')

query = "Impact of AI on software development"
enhanced_prompt = f"""You are a research expert. Provide a detailed, professional research report for the following query:
"{query}"

Structure your response with:
1. A clear Executive Summary.
2. Detailed Findings/Analysis.
3. A "References" section at the end with valid, clickable URL links to:
   - Wikipedia articles
   - Research papers (e.g., from Google Scholar, ArXiv, or Nature)
   - Authoritative websites (e.g., McKinsey, WEF, Forbes, or government agencies)
   - News articles or industry reports

Ensure the links are real and relevant to the topic."""

response = model.generate_content(enhanced_prompt)
print(response.text)
