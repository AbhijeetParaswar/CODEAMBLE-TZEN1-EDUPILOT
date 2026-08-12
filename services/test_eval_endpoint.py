"""Test script to verify evaluation endpoint is working"""
import requests
import json

API_BASE = "http://localhost:8000"

print("🧪 Testing Evaluation Endpoint\n")

# Test 1: Check if backend is running
print("1️⃣ Checking if backend is running...")
try:
    response = requests.get(f"{API_BASE}/health", timeout=5)
    if response.status_code == 200:
        print("   ✅ Backend is running")
    else:
        print(f"   ❌ Backend returned status {response.status_code}")
        exit(1)
except requests.exceptions.ConnectionError:
    print("   ❌ Backend is NOT running!")
    print("   💡 Start it with: python -m app.main")
    exit(1)

# Test 2: Check eval endpoint
print("\n2️⃣ Checking /api/v1/eval/results endpoint...")
try:
    response = requests.get(f"{API_BASE}/api/v1/eval/results", timeout=5)
    
    if response.status_code == 200:
        print("   ✅ Evaluation endpoint is working!")
        data = response.json()
        
        print("\n📊 Latest Evaluation Results:")
        print(f"   Agent: {data['agent']}")
        print(f"   Last Updated: {data['last_updated']}")
        print(f"   Sample Size: {data['sample_size']} questions")
        print(f"   Source File: {data['source_file']}")
        
        print("\n   Metrics:")
        for metric, value in data['metrics'].items():
            if value is not None:
                grade = "🟢" if value >= 0.75 else "🟡" if value >= 0.60 else "🔴"
                print(f"   {grade} {metric.replace('_', ' ').title()}: {value:.4f}")
            else:
                print(f"   ⚪ {metric.replace('_', ' ').title()}: N/A")
                
    elif response.status_code == 404:
        print("   ⚠️  No evaluation results found")
        print("   💡 Run evaluation first: python eval/ragas_eval.py")
    else:
        print(f"   ❌ Unexpected status code: {response.status_code}")
        print(f"   Response: {response.text}")
        
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 3: Check CORS headers
print("\n3️⃣ Checking CORS configuration...")
try:
    response = requests.options(f"{API_BASE}/api/v1/eval/results")
    cors_headers = {k: v for k, v in response.headers.items() if 'access-control' in k.lower()}
    if cors_headers:
        print("   ✅ CORS is configured")
        for header, value in cors_headers.items():
            print(f"      {header}: {value}")
    else:
        print("   ⚠️  CORS headers not found")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "="*60)
print("✅ Test Complete!")
print("="*60)
