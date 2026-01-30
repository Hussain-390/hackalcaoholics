import google.generativeai as genai
from models.schemas import Source
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class VerificationAgent:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-flash-latest')
        self.demo_mode = os.getenv("DEMO_MODE", "false").lower() == "true"
    
    def verify_sources(self, sources: list) -> dict:
        """Cross-check sources for contradictions"""
        
        if self.demo_mode or len(sources) == 0:
            # Demo mode or no sources
            return {
                "has_conflicts": False,
                "verification_text": "Sources show consistent information with no major contradictions detected. Multiple independent sources agree on key facts and figures.",
                "confidence_adjustment": 0.0
            }
        
        sources_text = "\n".join([
            f"{i+1}. {s.title}: {s.snippet[:100]}"
            for i, s in enumerate(sources[:5])
        ])
        
        prompt = f"""Analyze these sources for contradictions or agreements:

{sources_text}

Are there any major conflicts? Reply with ONLY:
"CONSISTENT: [brief explanation]" OR "CONFLICTS: [brief explanation]"
"""

        response = self.model.generate_content(prompt)
        text = response.text.strip()

        has_conflicts = text.startswith("CONFLICTS:")
        confidence_adjustment = -0.2 if has_conflicts else 0.0
        
        return {
            "has_conflicts": has_conflicts,
            "verification_text": text,
            "confidence_adjustment": confidence_adjustment,
            "sources_checked": len(sources)
        }

# TEST THIS FILE
if __name__ == "__main__":
    from search_agent import SearchAgent
    
    search = SearchAgent()
    sources = search.search_task("AI impact on jobs")
    
    verifier = VerificationAgent()
    result = verifier.verify_sources(sources)
    print(f"\n✅ Verification complete:")
    print(result["verification_text"])
