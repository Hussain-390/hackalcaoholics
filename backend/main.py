from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from models.schemas import ResearchRequest
from agents.coordinator import CoordinatorAgent
import uuid

load_dotenv()

app = FastAPI(title="ResearchSwarm AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage (for demo)
research_jobs = {}
coordinator = CoordinatorAgent()

@app.get("/")
def root():
    return {
        "message": "ResearchSwarm API Running!", 
        "version": "1.0",
        "status": "healthy"
    }

@app.post("/research/start")
async def start_research(request: ResearchRequest):
    """Start a new research job"""
    job_id = str(uuid.uuid4())
    
    try:
        # Validate query
        query = request.query.strip()
        
        # Check if query is too short
        if len(query) < 5:
            raise HTTPException(
                status_code=400, 
                detail="Query too short. Please provide a more detailed research question."
            )
        
        # Check if query is too long
        if len(query) > 500:
            raise HTTPException(
                status_code=400,
                detail="Query too long. Please keep your research question under 500 characters."
            )
        
        # Filter irrelevant/inappropriate queries
        irrelevant_keywords = ['hello', 'hi', 'test', 'asdf', '123', 'lol', 'haha']
        if any(keyword in query.lower() for keyword in irrelevant_keywords) and len(query) < 20:
            raise HTTPException(
                status_code=400,
                detail="Please provide a meaningful research question. Avoid greetings or test inputs."
            )
        
        # Check if query is actually a question/research topic
        query_lower = query.lower()
        has_question_words = any(word in query_lower for word in [
            'what', 'why', 'how', 'when', 'where', 'who', 'which',
            'analyze', 'research', 'investigate', 'explore', 'study',
            'impact', 'effect', 'trend', 'comparison', 'overview'
        ])
        
        # If no question words and very short, might be irrelevant
        if not has_question_words and len(query) < 15:
            raise HTTPException(
                status_code=400,
                detail="Please provide a clear research question. Try starting with 'What is...', 'How does...', etc."
            )
        
        # Run research
        print(f"[COORDINATOR] Starting research for: {query[:100]}...")
        report = await coordinator.research(query)
        
        # Store result
        research_jobs[job_id] = report
        
        print(f"[COORDINATOR] Research completed. Job ID: {job_id}")
        return {
            "job_id": job_id,
            "status": "completed",
            "message": "Research completed successfully"
        }
    
    except HTTPException:
        # Re-raise HTTP exceptions (validation errors)
        raise
    
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"[ERROR] Research failed: {str(e)}")
        print(error_trace)
        
        # Return user-friendly error
        raise HTTPException(
            status_code=500, 
            detail=f"Research failed due to an internal error. Please try again or contact support if the issue persists."
        )

@app.get("/research/{job_id}")
def get_research(job_id: str):
    """Get research results"""
    if job_id not in research_jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return research_jobs[job_id]

@app.get("/research/{job_id}/report")
def get_research_report(job_id: str):
    """Get research report (alias for frontend compatibility)"""
    if job_id not in research_jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return research_jobs[job_id]

@app.get("/research/{job_id}/conversation")
async def get_conversation_sse(job_id: str):
    """SSE endpoint stub - frontend expects this but we'll use polling instead"""
    # For now, just return 404 gracefully - frontend will handle it
    raise HTTPException(status_code=404, detail="SSE not implemented, use /report endpoint")

if __name__ == "__main__":
    import uvicorn
    print("Starting ResearchSwarm Backend...")
    print("Server: http://localhost:8000")
    print("Gemini API Key configured")
    uvicorn.run(app, host="0.0.0.0", port=8000)
