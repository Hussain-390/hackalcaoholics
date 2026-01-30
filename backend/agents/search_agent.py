from duckduckgo_search import DDGS
from models.schemas import Source
import time
import os
from dotenv import load_dotenv

load_dotenv()

class SearchAgent:
    def __init__(self):
        self.demo_mode = os.getenv("DEMO_MODE", "false").lower() == "true"
    
    def search_task(self, task_description: str, max_results: int = 5) -> list:
        """Search web for information"""
        
        if self.demo_mode:
            # Demo mode: return realistic mock sources
            return self._demo_search(task_description, max_results)
        
        try:
            # Use timeout and convert to list immediately
            print(f"[SEARCH] Attempting search for: {task_description[:50]}...")
            ddgs = DDGS(timeout=30)  # Increased timeout
            results = list(ddgs.text(task_description, region='wt-wt', max_results=max_results))
            
            sources = []
            for r in results:
                sources.append(Source(
                    url=r.get('href', ''),
                    title=r.get('title', 'No title'),
                    snippet=r.get('body', ''),
                    credibility_score=0.8
                ))
            
            print(f"[SEARCH] Found {len(sources)} sources for: {task_description[:50]}...")
            
            # If no results, try with simpler query
            if len(sources) == 0:
                print(f"[SEARCH] No results, trying simpler query...")
                # Extract key words
                simple_query = " ".join(task_description.split()[:5])
                ddgs2 = DDGS(timeout=30)
                results = list(ddgs2.text(simple_query, max_results=max_results))
                
                for r in results:
                    sources.append(Source(
                        url=r.get('href', ''),
                        title=r.get('title', 'No title'),
                        snippet=r.get('body', ''),
                        credibility_score=0.7
                    ))
                print(f"[SEARCH] Simple query found {len(sources)} sources")
            
            return sources
        except Exception as e:
            print(f"[ERROR] Search error: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def _demo_search(self, task_description: str, max_results: int) -> list:
        """Return demo search results"""
        query_lower = task_description.lower()
        
        # AI-related demo sources
        if 'ai' in query_lower or 'artificial intelligence' in query_lower:
            demo_sources = [
                Source(
                    url="https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai",
                   title="The State of AI in 2024 | McKinsey",
                    snippet="Artificial intelligence (AI) continues to transform industries globally. Recent surveys show 72% of organizations have adopted AI in at least one business function, with significant impact on productivity and decision-making processes."
                ),
                Source(
                    url="https://www.forbes.com/ai-artificial-intelligence/",
                    title="AI Trends and Impact on Business | Forbes",
                    snippet="AI technologies are reshaping how businesses operate, from automating routine tasks to enabling sophisticated data analysis. The global AI market is expected to reach $190 billion by 2025."
                ),
                Source(
                    url="https://www.nature.com/articles/d41586-024-00001-1",
                    title="AI Research Breakthroughs in 2024 | Nature",
                    snippet="Recent advances in large language models and computer vision have achieved near-human performance in multiple domains, raising both opportunities and ethical considerations."
                ),
                Source(
                    url="https://www.weforum.org/agenda/2024/01/ai-technology-future-jobs/",
                    title="How AI Will Transform the Future of Work | World Economic Forum",
                    snippet="Studies suggest AI could automate 25% of current work tasks by 2030 while creating new job categories. The focus shifts to reskilling and human-AI collaboration."
                ),
                Source(
                    url="https://ai.google/responsibility/",
                    title="Responsible AI Practices | Google AI",
                    snippet="Leading tech companies are developing frameworks for ethical AI development, focusing on fairness, transparency, privacy, and accountability in AI systems."
                )
            ]
        # EV-related demo sources
        elif 'ev' in query_lower or 'electric' in query_lower or 'power' in query_lower:
            demo_sources = [
                Source(
                    url="https://www.iea.org/reports/global-ev-outlook-2024",
                    title="Global EV Outlook 2024 | International Energy Agency",
                    snippet="Electric vehicle sales reached 14 million units globally in 2023, a 35% increase year-over-year. EVs accounted for 18% of total car sales, requiring significant grid infrastructure upgrades."
                ),
                Source(
                    url="https://economictimes.indiatimes.com/industry/renewables/india-power-grid-ev-charging",
                    title="India's Power Grid Faces EV Challenge | Economic Times",
                    snippet="India's power grid will need an additional 10-15 GW capacity by 2030 to support growing EV adoption. Smart charging infrastructure and renewable energy integration are key priorities."
                ),
                Source(
                    url="https://www.niti.gov.in/ev-policy-report",
                    title="EV Policy Framework for India | NITI Aayog",
                    snippet="Government initiatives target 30% EV penetration by 2030. This requires coordinated development of charging infrastructure, battery manufacturing, and grid modernization."
                ),
                Source(
                    url="https://www.sciencedirect.com/ev-grid-impact-study",
                    title="Impact of EV Charging on Distribution Networks | ScienceDirect",
                    snippet="Research shows managed charging strategies can reduce peak demand by 40%, while unmanaged charging could strain existing infrastructure. Vehicle-to-grid technology offers potential solutions."
                ),
                Source(
                    url="https://renewablesnow.com/ev-renewable-energy-integration",
                    title="Integrating EVs with Renewable Energy | Renewables Now",
                    snippet="Electric vehicles can serve as mobile energy storage, supporting renewable energy integration. Solar-powered EV charging reduces carbon footprint and grid dependency."
                )
            ]
        # Generic demo sources
        else:
            demo_sources = [
                Source(
                    url="https://www.example.com/research-article-1",
                    title=f"Comprehensive Analysis of {task_description[:40]}",
                    snippet=f"Latest research and data on {task_description[:50]}. Experts report significant developments and emerging trends in this area."
                ),
                Source(
                    url="https://www.example.com/research-article-2",
                    title=f"Industry Report: {task_description[:40]}",
                    snippet=f"Market analysis shows growing interest in {task_description[:50]}. Key stakeholders are investing in related technologies and infrastructure."
                ),
                Source(
                    url="https://www.example.com/research-article-3",
                    title= f"Expert Perspectives on {task_description[:40]}",
                    snippet=f"Leading researchers discuss implications and future outlook for {task_description[:50]}. Multiple approaches are being explored."
                ),
                Source(
                    url="https://www.example.com/research-article-4",
                    title=f"Statistical Overview: {task_description[:40]}",
                    snippet=f"Recent data highlights key metrics and performance indicators related to {task_description[:50]}. Year-over-year growth continues."
                ),
                Source(
                    url="https://www.example.com/research-article-5",
                    title=f"Future Trends in {task_description[:40]}",
                    snippet=f"Emerging patterns suggest significant evolution in {task_description[:50]}. Industry leaders project continued expansion and innovation."
                )
            ]
        
        print(f"[SEARCH] DEMO MODE: Returning {min(max_results, len(demo_sources))} mock sources")
        return demo_sources[:max_results]

# TEST THIS FILE
if __name__ == "__main__":
    import sys
    sys.path.insert(0, '.')
    agent = SearchAgent()
    sources = agent.search_task("What is Artificial Intelligence")
    print(f"\nFound {len(sources)} sources:")
    for s in sources[:3]:
        print(f"\n{s.title}\n{s.url}")
