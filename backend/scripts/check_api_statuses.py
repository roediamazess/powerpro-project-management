import urllib.request, json, os, sys
from collections import Counter

# Set path for backend modules
sys.path.append('/app')
from app.core import security

token = security.create_access_token(subject="4483533d-8413-4fa7-8f3c-b733e3c34c20")
req = urllib.request.Request('http://localhost:8000/api/v1/projects/', headers={'Authorization': f'Bearer {token}'})

with urllib.request.urlopen(req) as f:
    data = json.load(f)
    counts = Counter(p.get('status_id') for p in data)
    print(json.dumps(counts, indent=2))
    
    # Also find project 4707 specifically
    p4707 = next((p for p in data if p.get('cnc_id') == '4707'), None)
    if p4707:
        print("\nProject 4707 details:")
        print(json.dumps(p4707, indent=2))
    else:
        print("\nProject 4707 not found in API response!")
