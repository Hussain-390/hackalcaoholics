from pydantic import BaseModel
from typing import List
from datetime import datetime
from enum import Enum

class AgentType(str, Enum):
    PLANNER = "planner"
    SEARCH = "search"
    VERIFICATION = "verification"
    SYNTHESIS = "synthesis"
    COORDINATOR = "coordinator"

class ResearchTask(BaseModel):
    id: str
    description: str
    priority: int
    status: str = "pending"

class Source(BaseModel):
    url: str
    title: str
    snippet: str
    credibility_score: float = 0.8

class AgentMessage(BaseModel):
    agent_type: AgentType
    message: str
    timestamp: datetime

class ResearchRequest(BaseModel):
    query: str

class ResearchReport(BaseModel):
    query: str
    executive_summary: str
    key_findings: List[str]
    sources: List[Source]
    confidence_score: float
    agent_logs: List[AgentMessage]
