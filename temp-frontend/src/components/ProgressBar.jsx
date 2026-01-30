const TOTAL_AGENTS = 5; // Coordinator, Planner, Search, Verification, Synthesis

export default function ProgressBar({ status }) {
  const completed = Object.values(status).filter(
    (s) => s === "complete"
  ).length;

  const active = Object.values(status).filter(
    (s) => s === "active"
  ).length;

  const percent = Math.round((completed / TOTAL_AGENTS) * 100);

  return (
    <div className="progress-wrap">
      <div className="progress-label">
        Progress: {percent}% {active > 0 && `(${active} agent${active > 1 ? 's' : ''} working...)`}
      </div>
      <div className="progress-bar">
        <div
          className="progress-fill"
          style={{ width: `${percent}%` }}
        />
      </div>
    </div>
  );
}
