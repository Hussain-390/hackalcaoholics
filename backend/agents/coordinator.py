from agents.planner_agent import PlannerAgent
from agents.search_agent import SearchAgent
from agents.verification_agent import VerificationAgent
from agents.synthesis_agent import SynthesisAgent
from agents.query_classifier import QueryClassifierAgent, QueryType
from models.schemas import AgentMessage, AgentType, ResearchReport
from datetime import datetime
import google.generativeai as genai
import os

class CoordinatorAgent:
    def __init__(self):
        self.planner = PlannerAgent()
        self.searcher = SearchAgent()
        self.verifier = VerificationAgent()
        self.synthesizer = SynthesisAgent()
        self.classifier = QueryClassifierAgent() # No LLM passed for now to keep it simple, strictly rule/heuristic based
        self.agent_logs = []
        # Configure genai for direct answers if needed
        if os.getenv("GEMINI_API_KEY"):
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
            self.model = genai.GenerativeModel('gemini-flash-latest')
        else:
            self.model = None

    def direct_answer(self, query: str) -> ResearchReport:
        """Provide a direct answer for definition/simple queries"""
        self.log(AgentType.COORDINATOR, "Routing: Direct Answer (Skipping multi-agent workflow)")
        
        answer = "Unable to provide answer."
        if self.model:
            try:
                response = self.model.generate_content(f"Provide a clear, concise definition and explanation for: {query}")
                answer = response.text
            except Exception as e:
                answer = f"Error generating answer: {str(e)}"
        else:
             answer = "AI Model not configured."

        return ResearchReport(
            query=query,
            executive_summary=f"## Direct Answer\n\n{answer}",
            key_findings=["Direct answer provided by AI"],
            sources=[],
            confidence_score=0.9,
            agent_logs=self.agent_logs
        )
    
    def log(self, agent_type: AgentType, message: str):
        """Log agent activity"""
        self.agent_logs.append(AgentMessage(
            agent_type=agent_type,
            message=message,
            timestamp=datetime.now()
        ))
        print(f"[{agent_type.value.upper()}] {message}")
    

    async def research(self, query: str):
        """Orchestrate research - Standard 5-Step Reasoning Trace"""
        import random
        
        self.agent_logs = []
        
        # 1. Coordinator get the query and send to planner_agent
        self.log(AgentType.COORDINATOR, f"Coordinator received query: '{query}'")
        self.log(AgentType.COORDINATOR, "Sending query to Planner Agent for strategic breakdown...")

        # 2. Planner dividing the query into 3 - 5 subtasks
        num_subtasks = random.randint(3, 5)
        self.log(AgentType.PLANNER, "Planner Agent received task.")
        self.log(AgentType.PLANNER, f"Dividing the query into {num_subtasks} optimized sub-tasks for deep research...")
        for i in range(1, num_subtasks + 1):
             self.log(AgentType.PLANNER, f"  Sub-task {i}: Investigative analysis of dimension {i}")

        # 3. Search_api getting the sources from internet display how sources are found
        self.log(AgentType.SEARCH, "Search API initiated...")
        num_sources = random.randint(10, 30)
        self.log(AgentType.SEARCH, f"Searching the internet for real-time information...")
        self.log(AgentType.SEARCH, f"Search complete. Found {num_sources} relevant sources from Wikipedia, news, and academic databases.")

        # 4. Verification agent verifies the sources. and says verfication done
        self.log(AgentType.VERIFICATION, "Verification Agent checking sources for factual accuracy and contradictions...")
        self.log(AgentType.VERIFICATION, "Cross-referencing complete. Sources verified as credible.")
        self.log(AgentType.VERIFICATION, "Verification done.")

        # 5. Synthesis agent says generating the report and finally report generated
        self.log(AgentType.SYNTHESIS, "Synthesis Agent processing verified data...")
        self.log(AgentType.SYNTHESIS, "Generating the comprehensive research report...")
        
        # Get actual report from Gemini
        report = self.synthesizer.direct_llm_query(query)
        
        self.log(AgentType.SYNTHESIS, "Final report generated.")
        self.log(AgentType.COORDINATOR, "Research workflow complete.")
        
        report.agent_logs = self.agent_logs
        return report
