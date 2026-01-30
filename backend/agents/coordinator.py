from agents.planner_agent import PlannerAgent
from agents.search_agent import SearchAgent
from agents.verification_agent import VerificationAgent
from agents.synthesis_agent import SynthesisAgent
from models.schemas import AgentMessage, AgentType
from datetime import datetime

class CoordinatorAgent:
    def __init__(self):
        self.planner = PlannerAgent()
        self.searcher = SearchAgent()
        self.verifier = VerificationAgent()
        self.synthesizer = SynthesisAgent()
        self.agent_logs = []
    
    def log(self, agent_type: AgentType, message: str):
        """Log agent activity"""
        self.agent_logs.append(AgentMessage(
            agent_type=agent_type,
            message=message,
            timestamp=datetime.now()
        ))
        print(f"[{agent_type.value.upper()}] {message}")
    
    async def research(self, query: str):
        """Orchestrate full research"""
        
        self.agent_logs = []
        
        # Coordinator starts
        self.log(AgentType.COORDINATOR, f"Initiating research workflow for query: {query[:60]}...")
        self.log(AgentType.COORDINATOR, "Delegating to Planner Agent...")
        
        # Step 1: Plan
        self.log(AgentType.PLANNER, f"Analyzing query: '{query}'")
        tasks = self.planner.plan_research(query)
        self.log(AgentType.PLANNER, f"Created {len(tasks)} research tasks:")
        
        # Log each task
        for i, task in enumerate(tasks, 1):
            self.log(AgentType.PLANNER, f"  Task {i}: {task.description}")
        
        self.log(AgentType.COORDINATOR, f"Planner completed. Delegating to Search Agent for {len(tasks[:3])} tasks...")
        
        # Step 2: Search
        all_sources = []
        for i, task in enumerate(tasks[:3], 1):  # Limit to 3 tasks for speed
            self.log(AgentType.SEARCH, f"[Task {i}/{len(tasks[:3])}] Searching: {task.description[:60]}...")
            sources = self.searcher.search_task(task.description, max_results=5)
            
            # Log each source found
            if sources:
                self.log(AgentType.SEARCH, f"  Found {len(sources)} sources for Task {i}:")
                for j, source in enumerate(sources[:3], 1):  # Show top 3
                    self.log(AgentType.SEARCH, f"    [{j}] {source.title[:60]}...")
                    self.log(AgentType.SEARCH, f"        URL: {source.url}")
                if len(sources) > 3:
                    self.log(AgentType.SEARCH, f"    ...and {len(sources) - 3} more sources")
            else:
                self.log(AgentType.SEARCH, f"  No sources found for Task {i}")
            
            all_sources.extend(sources)
        
        self.log(AgentType.COORDINATOR, f"Search completed with {len(all_sources)} total sources. Delegating to Verification Agent...")
        
        # Step 3: Verify
        self.log(AgentType.VERIFICATION, f"Cross-checking {len(all_sources)} sources for consistency...")
        verification = self.verifier.verify_sources(all_sources)
        
        # Log verification details
        has_conflicts = verification.get('has_conflicts', False)
        if has_conflicts:
            self.log(AgentType.VERIFICATION, "⚠ Conflicts detected between sources")
            self.log(AgentType.VERIFICATION, f"  Details: {verification.get('verification_text', '')[:100]}...")
        else:
            self.log(AgentType.VERIFICATION, "✓ Sources are consistent - no major conflicts detected")
            self.log(AgentType.VERIFICATION, f"  {verification.get('sources_checked', 0)} sources cross-referenced")
        
        self.log(AgentType.VERIFICATION, "Verification complete")
        
        self.log(AgentType.COORDINATOR, "Verification complete. Delegating to Synthesis Agent for final report...")
        
        # Step 4: Synthesize
        self.log(AgentType.SYNTHESIS, "Analyzing all sources and generating comprehensive report...")
        self.log(AgentType.SYNTHESIS, f"Processing {len(all_sources)} sources across {len(tasks[:3])} research dimensions")
        
        report = self.synthesizer.synthesize_report(query, all_sources, verification)
        
        # Log synthesis details
        self.log(AgentType.SYNTHESIS, f"Generated executive summary ({len(report.executive_summary)} characters)")
        self.log(AgentType.SYNTHESIS, f"Extracted {len(report.key_findings)} key findings")
        self.log(AgentType.SYNTHESIS, f"Calculated confidence score: {int(report.confidence_score*100)}%")
        self.log(AgentType.SYNTHESIS, "Report generation complete")
        
        report.agent_logs = self.agent_logs
        
        self.log(AgentType.COORDINATOR, f"Research workflow completed successfully!")
        self.log(AgentType.COORDINATOR, f"Delivering report with {len(all_sources)} sources and {int(report.confidence_score*100)}% confidence")
        
        return report
