import requests
import json

url = "http://localhost:8000/research/start"
payload = {"query": "What is AI"}

print("Testing Coordinator logs...")
try:
    response = requests.post(url, json=payload, timeout=30)
    if response.status_code == 200:
        data = response.json()
        job_id = data['job_id']
        
        # Fetch report
        report_response = requests.get(f"http://localhost:8000/research/{job_id}/report", timeout=30)
        report = report_response.json()
        
        # Check agent logs
        print(f"\n✅ Found {len(report['agent_logs'])} agent log messages:\n")
        
        coordinator_count = 0
        for log in report['agent_logs']:
            agent_type = log['agent_type'].upper()
            message = log['message']
            print(f"[{agent_type}] {message}")
            if agent_type == 'COORDINATOR':
                coordinator_count += 1
        
        print(f"\n✅ Coordinator appears {coordinator_count} times")
        print(f"✅ Total agents involved: {len(set(log['agent_type'] for log in report['agent_logs']))}")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
