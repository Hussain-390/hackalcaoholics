import { useState } from "react";
import QueryInput from "./components/QueryInput";
import AgentGraph from "./components/AgentGraph";
import ReasoningTrace from "./components/ReasoningTrace";
import ResearchReport from "./components/ResearchReport";
import { startResearch, fetchReport } from "./api/api";
import ProgressBar from "./components/ProgressBar";

function App() {
  const [agentStatus, setAgentStatus] = useState({});
  const [logs, setLogs] = useState([]);
  const [report, setReport] = useState(null);

  const handleStart = async (query) => {
    setAgentStatus({});
    setLogs([]);
    setReport(null);

    try {
      // Start research
      const { job_id } = await startResearch(query);

      // Fetch completed report
      const finalReport = await fetchReport(job_id);

      // Animate agent logs for better UX
      if (finalReport.agent_logs && finalReport.agent_logs.length > 0) {
        await animateAgentLogs(finalReport.agent_logs);
      }

      // Show final report
      setReport(finalReport);

    } catch (error) {
      console.error("Research failed:", error);

      // Extract error message from response
      let errorMessage = "Research failed. Please try again.";

      if (error.response && error.response.data && error.response.data.detail) {
        // Backend validation error
        errorMessage = error.response.data.detail;
      } else if (error.message) {
        errorMessage = error.message;
      }

      // Display error in logs
      setLogs([`❌ Error: ${errorMessage}`]);

      // Set all agents to error state
      setAgentStatus({
        Coordinator: "error",
        Planner: "error",
        Search: "error",
        Verification: "error",
        Synthesis: "error"
      });
    }
  };

  const animateAgentLogs = async (agent_logs) => {
    const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

    // Set Coordinator as active from the start
    setAgentStatus({ Coordinator: "active" });

    for (let i = 0; i < agent_logs.length; i++) {
      const log = agent_logs[i];
      const agentType = log.agent_type.toLowerCase();
      const message = log.message;

      // Add log message
      setLogs(prev => [...prev, `[${log.agent_type.toUpperCase()}] ${message}`]);

      // Update agent status
      const statusMap = {
        'coordinator': 'Coordinator',
        'planner': 'Planner',
        'search': 'Search',
        'verification': 'Verification',
        'synthesis': 'Synthesis'
      };

      const agentKey = statusMap[agentType];
      if (agentKey) {
        // Coordinator stays active throughout
        if (agentKey === 'Coordinator') {
          setAgentStatus(prev => ({
            ...prev,
            Coordinator: "active"
          }));
        } else {
          // Other agents become active when they work
          setAgentStatus(prev => ({
            ...prev,
            Coordinator: "active", // Keep coordinator active
            [agentKey]: "active"
          }));
        }
      }

      // Small delay between logs for animation effect
      await delay(300);

      // Mark as complete when moving to next agent (but not Coordinator)
      if (i < agent_logs.length - 1) {
        const nextLog = agent_logs[i + 1];
        const nextAgentType = nextLog.agent_type.toLowerCase();

        // Complete current agent if next log is from different agent
        if (nextAgentType !== agentType && agentKey && agentKey !== 'Coordinator') {
          setAgentStatus(prev => ({
            ...prev,
            Coordinator: "active", // Keep coordinator active
            [agentKey]: "complete"
          }));
        }
      }
    }

    // Mark all as complete at the end
    setAgentStatus({
      Coordinator: "complete",
      Planner: "complete",
      Search: "complete",
      Verification: "complete",
      Synthesis: "complete"
    });
  };

  return (
    <div className="container">
      <h1>ResearchSwarm AI</h1>

      <QueryInput onStart={handleStart} />
      <ProgressBar status={agentStatus} />
      <div className="grid">
        <AgentGraph status={agentStatus} />
        <ReasoningTrace logs={logs} />
        <ResearchReport report={report} />
      </div>
    </div>
  );
}

export default App;
