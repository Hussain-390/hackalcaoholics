import ConfidenceBadge from "./ConfidenceBadge";
import ReactMarkdown from 'react-markdown';

export default function ResearchReport({ report }) {
  if (!report) {
    return (
      <div className="card">
        <h3>Final Report</h3>
        <p>Waiting for report...</p>
      </div>
    );
  }

  return (
    <div className="card report-enter" style={{ maxHeight: '600px', overflowY: 'auto' }}>
      <h3>Research Report</h3>

      {/* Render markdown content */}
      <div className="markdown-content" style={{
        lineHeight: '1.7',
        fontSize: '14px'
      }}>
        <ReactMarkdown
          components={{
            a: ({ node, ...props }) => <a {...props} target="_blank" rel="noopener noreferrer" />
          }}
        >
          {report.executive_summary}
        </ReactMarkdown>
      </div>
    </div>
  );
}
