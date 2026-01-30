const BASE_URL = "http://localhost:8000";

export async function startResearch(query) {
  const res = await fetch(`${BASE_URL}/research/start`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query }),
  });

  if (!res.ok) {
    // Handle HTTP errors
    const errorData = await res.json().catch(() => ({ detail: "Network error" }));
    const error = new Error(errorData.detail || "Request failed");
    error.response = { data: errorData, status: res.status };
    throw error;
  }

  return res.json(); // { job_id }
}

export async function fetchReport(jobId) {
  const res = await fetch(`${BASE_URL}/research/${jobId}/report`);

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({ detail: "Network error" }));
    const error = new Error(errorData.detail || "Request failed");
    error.response = { data: errorData, status: res.status };
    throw error;
  }

  return res.json();
}
