import requests
import json

url = "http://localhost:8000/research/start"
payload = {"query": "Impact of AI on jobs"}

print("Testing DETAILED Coordinator logs...")
print("="*80)
try:
    response = requests.post(url, json=payload, timeout=30)
    if response.status_code == 200:
        data = response.json()
        job_id = data['job_id']
        
        # Fetch report
        report_response = requests.get(f"http://localhost:8000/research/{job_id}/report", timeout=30)
        report = report_response.json()
        
        # Display all agent logs with proper formatting
        print(f"\n✅ REASONING TRACE ({len(report['agent_logs'])} messages):\n")
        
        for i, log in enumerate(report['agent_logs'], 1):
            agent_type = log['agent_type'].upper()
            message = log['message']
            
            # Add visual separators for different agents
            if i == 1 or (i > 1 and log['agent_type'] != report['agent_logs'][i-2]['agent_type']):
                print()
            
            # Format based on agent type
            if agent_type == 'COORDINATOR':
                print(f"🎯 [{agent_type}] {message}")
            elif agent_type == 'PLANNER':
                print(f"📋 [{agent_type}] {message}")
            elif agent_type == 'SEARCH':
                print(f"🔍 [{agent_type}] {message}")
            elif agent_type == 'VERIFICATION':
                print(f"✓ [{agent_type}] {message}")
            elif agent_type == 'SYNTHESIS':
                print(f"📊 [{agent_type}] {message}")
        
        print("\n" + "="*80)
        print(f"✅ Total: {len(report['agent_logs'])} log messages")
        print(f"✅ Agents: {', '.join(set(log['agent_type'].upper() for log in report['agent_logs']))}")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
