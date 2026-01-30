import google.generativeai as genai
from models.schemas import ResearchTask
import os
import uuid
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class PlannerAgent:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-flash-latest')
        self.demo_mode = os.getenv("DEMO_MODE", "false").lower() == "true"
    
    def plan_research(self, query: str) -> list:
        """Break down complex query into research tasks"""
        
        if self.demo_mode:
            # Demo mode: return predefined tasks based on query
            return self._demo_plan(query)
        
        prompt = f"""You are a research planner. Break down this query into 3-5 specific research tasks.

Query: {query}

Return ONLY a numbered list of tasks. Example:
1. Find current statistics on X
2. Research expert opinions about Y
3. Analyze trends in Z"""

        response = self.model.generate_content(prompt)
        tasks_text = response.text.strip()
        
        # Parse tasks
        tasks = []
        for i, line in enumerate(tasks_text.split('\n')):
            if line.strip() and (line[0].isdigit() or line.startswith('-')):
                task_desc = line.split('.', 1)[-1].strip()
                if task_desc:
                    tasks.append(ResearchTask(
                        id=str(uuid.uuid4()),
                        description=task_desc,
                        priority=i+1
                    ))
        
        return tasks
    
    def _demo_plan(self, query: str) -> list:
        """Return demo tasks"""
        query_lower = query.lower()
        
        # AI-related queries
        if 'ai' in query_lower or 'artificial intelligence' in query_lower:
            task_descriptions = [
                "Research current AI definitions and capabilities",
                "Find statistics on AI adoption across industries",
                "Analyze AI impact on employment and workforce",
                "Explore ethical considerations and regulations"
            ]
        # EV-related queries
        elif 'ev' in query_lower or 'electric vehicle' in query_lower:
            task_descriptions = [
                "Research EV market growth and adoption rates",
                "Analyze power grid infrastructure requirements",
                "Find data on charging infrastructure development",
                "Explore environmental and economic impacts"
            ]
        # Default generic tasks
        else:
            task_descriptions = [
                f"Research current state of {query[:30]}",
                f"Find statistics and data about {query[:30]}",
                f"Analyze impact and implications of {query[:30]}",
                f"Explore future trends in {query[:30]}"
            ]
        
        return [ResearchTask(
            id=str(uuid.uuid4()),
            description=desc,
            priority=i+1
        ) for i, desc in enumerate(task_descriptions)]

# TEST THIS FILE
if __name__ == "__main__":
    agent = PlannerAgent()
    tasks = agent.plan_research("Impact of EVs on Indian power grid")
    print(f"\nGenerated {len(tasks)} tasks:")
    for task in tasks:
        print(f"{task.priority}. {task.description}")
