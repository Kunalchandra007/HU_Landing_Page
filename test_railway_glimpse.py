"""
Test adding a glimpse to Railway backend
"""
import requests

API_URL = "https://web-production-bd5a.up.railway.app/api"

# Test data
data = {
    'title': 'Test Glimpse',
    'description': 'Testing glimpse without image',
    'video_url': 'https://www.youtube.com/embed/test123',
    'hashtags': '#test'
}

try:
    print("Testing Railway API...")
    print(f"URL: {API_URL}/admin/glimpses")
    
    response = requests.post(
        f"{API_URL}/admin/glimpses",
        data=data
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
except Exception as e:
    print(f"Error: {e}")
