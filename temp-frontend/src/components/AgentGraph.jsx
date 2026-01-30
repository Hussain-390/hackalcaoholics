import { useEffect, useState } from "react";

const agents = [
  "Coordinator",
  "Planner",
  "Search",
  "Verification",
  "Synthesis",
];

export default function AgentGraph({ status }) {
  const [activeAgent, setActiveAgent] = useState(null);

  useEffect(() => {
    const current = Object.entries(status).find(
      ([_, value]) => value === "active"
    );
    if (current) setActiveAgent(current[0]);
  }, [status]);

  return (
    <div className="card">
      <h3>Agent Graph</h3>
      {agents.map((agent) => (
        <div
          key={agent}
          className={`agent ${status[agent] || "idle"} ${
            activeAgent === agent ? "pulse" : ""
          }`}
        >
          <span>{agent}</span>
          <span>{status[agent] || "idle"}</span>
        </div>
      ))}
    </div>
  );
}
