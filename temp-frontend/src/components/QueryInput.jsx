import { useState } from "react";

export default function QueryInput({ onStart }) {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);

  const handleClick = async () => {
    setLoading(true);
    await onStart(query);
    setLoading(false);
  };

  return (
    <div className="query-box">
      <textarea
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Enter your research query..."
        disabled={loading}
      />
      <button onClick={handleClick} disabled={loading}>
        {loading ? "Running Agents..." : "Start Research"}
      </button>
    </div>
  );
}
