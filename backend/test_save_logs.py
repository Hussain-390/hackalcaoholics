import requests
import json

url = "http://localhost:8000/research/start"
payload = {"query": "Impact of AI on jobs"}

print("Testing DETAILED Coordinator logs...")
try:
    response = requests.post(url, json=payload, timeout=30)
    if response.status_code == 200:
        data = response.json()
        job_id = data['job_id']
        
        # Fetch report
        report_response = requests.get(f"http://localhost:8000/research/{job_id}/report", timeout=30)
        report = report_response.json()
        
        # Save to file
        with open('reasoning_trace_output.txt', 'w', encoding='utf-8') as f:
            f.write(f"REASONING TRACE ({len(report['agent_logs'])} messages)\n")
            f.write("="*80 + "\n\n")
            
            for i, log in enumerate(report['agent_logs'], 1):
                agent_type = log['agent_type'].upper()
                message = log['message']
                
                # Add visual separators
                if i > 1 and log['agent_type'] != report['agent_logs'][i-2]['agent_type']:
                    f.write("\n")
                
                f.write(f"[{agent_type}] {message}\n")
            
            f.write("\n" + "="*80 + "\n")
            f.write(f"Total: {len(report['agent_logs'])} messages\n")
        
        print(f"✅ Saved {len(report['agent_logs'])} log messages to reasoning_trace_output.txt")
        
        # Also print first 15 for preview
        print("\nPreview (first 15 messages):")
        for log in report['agent_logs'][:15]:
            print(f"  [{log['agent_type'].upper()}] {log['message'][:80]}...")
        
except Exception as e:
    print(f"Error: {e}")
