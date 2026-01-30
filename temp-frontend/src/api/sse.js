export function connectSSE(jobId, onEvent) {
  const source = new EventSource(
    `http://localhost:8000/research/${jobId}/conversation`
  );

  source.onmessage = (event) => {
    const data = JSON.parse(event.data);
    onEvent(data);
  };

  source.onerror = () => {
    console.error("SSE connection error");
    source.close();
  };

  return () => source.close();
}
