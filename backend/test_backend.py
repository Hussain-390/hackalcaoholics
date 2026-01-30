import requests
import json

url = "http://localhost:8000/research/start"
payload = {"query": "What is AI"}

print("Testing backend POST request...")
try:
    response = requests.post(url, json=payload, timeout=30)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Success! Job ID: {data.get('job_id')}")
        
        # Try fetching report
        report_url = f"http://localhost:8000/research/{data['job_id']}/report"
        print(f"\nFetching report from {report_url}...")
        report_response = requests.get(report_url, timeout=30)
        print(f"Report Status: {report_response.status_code}")
        if report_response.status_code == 200:
            report = report_response.json()
            print(f"\nReport Summary: {report.get('executive_summary', '')[:150]}...")
            print(f"Confidence: {report.get('confidence_score', 0)*100}%")
            print(f"Sources: {len(report.get('sources', []))}")
            print("\n✅ DEMO MODE WORKING!")
        else:
            print(f"Report fetch failed: {report_response.text}")
    else:
        print(f"Request failed with: {response.text}")
except Exception as e:
    print(f"Error: {e}")
