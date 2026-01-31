from enum import Enum
import re
import json

class QueryType(str, Enum):
    DEFINITION = "definition"
    RESEARCH = "research"
    VAGUE = "vague"
    OPINION_FORCED = "opinion_forced"
    TIME_SENSITIVE = "time_sensitive"
    CONTRADICTORY = "contradictory"
    UNKNOWN = "unknown"


class QueryClassifierAgent:
    def __init__(self, llm=None):
        """
        llm: optional LLM client (Ollama / OpenAI) for fallback
        """
        self.llm = llm

    def classify(self, query: str) -> QueryType:
        q = query.lower().strip()

        # ---------- LAYER 1: HARD RULES (FAST EXIT) ----------

        # Definition queries
        if re.match(r"^(what is|define|explain)\b", q):
            return QueryType.DEFINITION

        # Very short / vague
        if len(q.split()) < 4:
            return QueryType.VAGUE

        # Time-sensitive
        if any(word in q for word in [
            "today", "right now", "latest", "just announced",
            "this week", "current status"
        ]):
            return QueryType.TIME_SENSITIVE

        # Opinion forcing
        if any(phrase in q for phrase in [
            "prove that", "clearly shows", "why is",
            "is definitely bad", "is harmful", "must be banned"
        ]):
            return QueryType.OPINION_FORCED

        # Contradictory request
        if "unbiased" in q and any(word in q for word in ["prove", "show that"]):
            return QueryType.CONTRADICTORY

        # ---------- LAYER 2: HEURISTIC SCORING ----------

        research_score = 0

        research_keywords = [
            "analyze", "assess", "evaluate", "impact", "effects",
            "compare", "policy", "reports", "studies",
            "expert opinions", "published", "evidence"
        ]

        for kw in research_keywords:
            if kw in q:
                research_score += 1

        # Presence of constraints = research signal
        if any(w in q for w in ["india", "after", "between", "from", "using"]):
            research_score += 1

        if research_score >= 2:
            return QueryType.RESEARCH

        # ---------- LAYER 3: LLM FALLBACK (AMBIGUOUS CASES) ----------

        if self.llm:
            return self._llm_classify(query)

        return QueryType.UNKNOWN

    # ---------- LLM-BASED CLASSIFICATION ----------
    def _llm_classify(self, query: str) -> QueryType:
        # Assuming llm has a generate method or similar. 
        # If this is not standard, we might need to adapt. 
        # For now, keeping as provided in snippet.
        if not hasattr(self.llm, 'generate'):
             return QueryType.UNKNOWN

        prompt = f"""
Classify the following user query into ONE category only.

Categories:
- definition
- research
- vague
- opinion_forced
- time_sensitive
- contradictory

Query:
"{query}"

Respond ONLY in JSON:
{{ "type": "<category>" }}
"""
        try:
            response = self.llm.generate(prompt)
            # Basic cleanup of markdown json if present
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            if response.endswith("```"):
                response = response[:-3]

            data = json.loads(response)
            return QueryType(data.get("type", "unknown"))
        except:
            return QueryType.UNKNOWN
