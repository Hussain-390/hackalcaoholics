export default function ConfidenceBadge({ score }) {
  const percent = Math.round(score * 100);

  let level = "high";
  if (percent < 70) level = "medium";
  if (percent < 40) level = "low";

  return (
    <div className={`confidence ${level}`}>
      Confidence: {percent}%
    </div>
  );
}
