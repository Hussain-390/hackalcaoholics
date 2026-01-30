import { useEffect, useRef } from "react";

export default function ReasoningTrace({ logs }) {
  const endRef = useRef(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [logs]);

  return (
    <div className="card">
      <h3>Reasoning Trace</h3>
      <ul>
        {logs.map((log, i) => (
          <li key={i} className="log-item">
            {log}
          </li>
        ))}
        <div ref={endRef} />
      </ul>
    </div>
  );
}
