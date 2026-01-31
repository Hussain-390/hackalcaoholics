import google.generativeai as genai
from models.schemas import Source, ResearchReport, AgentMessage, AgentType
from datetime import datetime
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class SynthesisAgent:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-flash-latest')
        self.demo_mode = os.getenv("DEMO_MODE", "false").lower() == "true"
    
    def direct_llm_query(self, query: str) -> ResearchReport:
        """Directly query the LLM and return a structured response with clickable references"""
        prompt = f"""You are a senior research analyst. Provide a comprehensive, professional research report for the following query:
"{query}"

Your response must be in JSON format with the following structure:
{{
    "summary": "A detailed executive summary (2-3 paragraphs, markdown supported). Use in-text citations like [1], [2] where appropriate.",
    "findings": [
        "Key finding 1 with details and in-text citation [1]",
        "Key finding 2 with details and in-text citation [2]"
    ],
    "recommendations": "Strategic recommendations or next steps.",
    "references": [
        {{
            "title": "Clear Title of the Source",
            "url": "https://www.example.com/actual-relevant-link",
            "type": "Wikipedia/Paper/Website",
            "snippet": "Briefly describe how this source supports the research."
        }}
    ]
}}

Requirements:
- Include at least 5-7 diverse references (Wikipedia, research papers like ArXiv/Nature, industry leaders like McKinsey/Gartner, and government/educational sites).
- All links must be valid URLs.
- IMPORTANT: Use numerical in-text citations (e.g., [1], [2]) in the 'summary' and 'findings' sections. 
- The summary should be thorough and academically rigorous.
"""

        try:
            # Request JSON output
            response = self.model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
            data = json.loads(response.text)
            
            summary = data.get("summary", "No summary provided.")
            findings = data.get("findings", [])
            recommendations = data.get("recommendations", "")
            references = data.get("references", [])
            
            # Helper to make citations open external links directly
            def linkify_citations(text, refs):
                for i, ref in enumerate(refs, 1):
                    url = ref.get("url", "#")
                    # Replace [1] with [[1]](url)
                    text = text.replace(f"[{i}]", f"[ [{i}] ]({url})")
                return text

            summary = linkify_citations(summary, references)
            findings = [linkify_citations(f, references) for f in findings]
            
            # Build Markdown Report
            full_report_md = f"# Research Report: {query}\n\n"
            full_report_md += f"## Executive Summary\n{summary}\n\n"
            
            if findings:
                full_report_md += "## Key Findings\n"
                for i, f in enumerate(findings, 1):
                    full_report_md += f"{i}. {f}\n"
                full_report_md += "\n"
                
            if recommendations:
                full_report_md += f"## Recommendations\n{recommendations}\n\n"
            
            # Force a VERY visible References section
            full_report_md += "---\n\n"
            full_report_md += "## 📚 References & Source Links\n"
            full_report_md += "Click on a citation number in the text above to open the source directly, or use the links below.\n\n"
            
            sources = []
            for i, ref in enumerate(references, 1):
                title = ref.get("title", "Source")
                url = ref.get("url", "#")
                ref_type = ref.get("type", "Web")
                snippet = ref.get("snippet", "")
                
                # Add to markdown
                full_report_md += f"### [{i}] [{title}]({url})\n"
                full_report_md += f"**Type:** {ref_type} | **Link:** [{url}]({url})\n\n"
                if snippet:
                    full_report_md += f"> {snippet}\n\n"
                
                # Also populate the Sources list in the object
                sources.append(Source(
                    url=url,
                    title=title,
                    snippet=snippet,
                    credibility_score=0.9
                ))

            return ResearchReport(
                query=query,
                executive_summary=full_report_md,
                key_findings=findings,
                sources=sources,
                confidence_score=0.95,
                agent_logs=[]
            )

        except Exception as e:
            error_report = f"## Error Generating Report\nSomething went wrong: {str(e)}\n\n"
            return ResearchReport(
                query=query,
                executive_summary=error_report,
                key_findings=[],
                sources=[],
                confidence_score=0.0,
                agent_logs=[]
            )

    def synthesize_report(self, query: str, sources: list, verification: dict):
        """Generate final research report"""
        
        # Calculate confidence score based on sources
        confidence = self._calculate_confidence(sources, verification)
        
        if not sources or len(sources) == 0:
            return ResearchReport(
                query=query,
                executive_summary="Insufficient credible data available.",
                key_findings=[],
                sources=[],
                confidence_score=0.3,
                agent_logs=[]
            )

        if self.demo_mode:
            return self._generate_demo_report(query, sources, verification, confidence)

        return self._generate_real_report(query, sources, verification, confidence)
    
    def _generate_demo_report(self, query: str, sources: list, verification: dict, confidence: float) -> ResearchReport:
        """Generate a robust demo report without API calls"""
        references_text = self._build_references(sources)
        
        # Create generic but professional sounding content based on query
        executive_summary = f"""This report provides a comprehensive analysis of **{query}**, synthesizing information from multiple authoritative sources to deliver evidence-based insights. The investigation examines current trends, emerging patterns, and potential implications.

The analysis draws from diverse sources (see References) to construct a multifaceted understanding of the topic. Key themes identified include technological developments, market dynamics, and stakeholder perspectives that shape the current landscape.

**Note: This is a generated demonstration report based on search results.**"""

        key_findings = [
            f"Significant activity and growing interest found in {query[:30]} domain [1].",
            f"Multiple credible sources indicate positive growth trajectories [2].",
            "Experts emphasize the importance of strategic implementation and adaptation [3].",
            "Recent developments suggest a shift towards more sustainable and efficient models [4]."
        ]
        
        full_report = f"""## Executive Summary

{executive_summary}

---

## Key Findings

{self._format_findings_markdown(key_findings)}

---

## Detailed Analysis

### Market Overview
Recent data highlights key metrics and performance indicators related to the subject. Year-over-year growth continues to be a strong indicator of sector health.

### Strategic Implications
Stakeholders are pursuing diverse approaches, reflecting varying priorities and operational contexts. Innovation remains a primary driver of competitive advantage.

---

## Conclusion

The long-term outlook remains constructive, subject to continued investment and favorable conditions. Stakeholders should monitor these trends closely.

---

## Conflict & Confidence Report
{verification.get('verification_text', 'No verification data.')}

*Confidence Score: {int(confidence * 100)}%*

---

## References

{references_text}
"""
        
        return ResearchReport(
            query=query,
            executive_summary=full_report,
            key_findings=key_findings,
            sources=sources[:20],
            confidence_score=confidence,
            agent_logs=[]
        )
    
    def _generate_real_report(self, query: str, sources: list, verification: dict, confidence: float) -> ResearchReport:
        """Generate a professionally formatted academic report using Gemini"""
        
        # Prepare sources text
        sources_text = "\n".join([
            f"[{i+1}] Title: {s.title}\n    URL: {s.url}\n    Content: {s.snippet[:400]}..." 
            for i, s in enumerate(sources[:15])
        ])
        
        verification_notes = verification.get('verification_text', 'No conflicts detected')
        
        prompt = f"""You are an advanced research synthesis agent. Your task is to generate a comprehensive, professional research report based strictly on the provided sources.

Query: {query}

Sources:
{sources_text}

Verification Notes:
{verification_notes}

Instructions:
1. Synthesize information from the provided sources.
2. Cite sources using [1], [2] notation corresponding to the source list numbers.
3. Be objective, comprehensive, and clear.
4. If sources contradict, mention the conflict.

Return a JSON object with the following structure:
{{
    "executive_summary": "A 2-3 paragraph professional summary of the research (Markdown supported).",
    "key_findings": [
        "Finding 1 with citation [1]",
        "Finding 2 with citation [2]"
    ],
    "detailed_analysis": "A detailed analysis section breaking down the topic (Markdown supported).",
    "conclusion": "Final concluding remarks."
}}
"""
        
        try:
            response = self.model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
            response_text = response.text
            data = json.loads(response_text)
        except Exception as e:
            print(f"Error generating report: {e}")
            # Fallback if JSON parsing fails
            return self._fallback_report(query, sources)

        # Build full markdown report
        references_text = self._build_references(sources)
        
        full_report = f"""## Executive Summary

{data.get('executive_summary', 'Summary not available.')}

---

## Key Findings

{self._format_findings_markdown(data.get('key_findings', []))}

---

## Detailed Analysis

{data.get('detailed_analysis', 'Analysis not available.')}

---

## Conclusion

{data.get('conclusion', '')}

---

## References

{references_text}
"""
        
        return ResearchReport(
            query=query,
            executive_summary=full_report,  # Store full markdown here as per convention
            key_findings=data.get('key_findings', []),
            sources=sources[:20],
            confidence_score=confidence,
            agent_logs=[]
        )

    def _format_findings_markdown(self, findings: list) -> str:
        return "\n".join([f"{i+1}. {finding}" for i, finding in enumerate(findings)])

    def _calculate_confidence(self, sources: list, verification: dict) -> float:
        """Calculate confidence score based on sources and verification"""
        if not sources:
            return 0.3
        
        source_count = len(sources)
        base_confidence = 0.5
        if source_count >= 10: base_confidence = 0.9
        elif source_count >= 5: base_confidence = 0.8
        elif source_count >= 3: base_confidence = 0.7
        else: base_confidence = 0.6
        
        if verification.get('has_conflicts', False):
            base_confidence -= 0.15
        
        return min(0.95, max(0.3, base_confidence))

    def _build_references(self, sources: list) -> str:
        """Build properly formatted references section"""
        references = []
        for idx, source in enumerate(sources[:20], 1):
            publisher = "Web Source"
            if source.url:
                try:
                    from urllib.parse import urlparse
                    domain = urlparse(source.url).netloc
                    publisher = domain.replace('www.', '').split('.')[0].title()
                except:
                    pass
            
            ref = f"{idx}. {source.title}, {publisher}\n   {source.url}"
            references.append(ref)
        
        return "\n\n".join(references)

    def _fallback_report(self, query, sources):
        return ResearchReport(
            query=query,
            executive_summary="Error generating full report. Please try again.",
            key_findings=["Error parsing AI response"],
            sources=sources,
            confidence_score=0.5,
            agent_logs=[]
        )
