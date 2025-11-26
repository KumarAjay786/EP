# College Filtering API - Testing & Examples

## Testing Tools Setup

### 1. Using cURL

```bash
# Get all colleges
curl -X GET "http://127.0.0.1:8000/api/colleges/list/" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Filter by district
curl -X GET "http://127.0.0.1:8000/api/colleges/list/?district=Chennai" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Complex filter
curl -X GET "http://127.0.0.1:8000/api/colleges/list/?district=Chennai&main_stream=engineering&college_type=private" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 2. Using Postman

#### Request Setup
```
Method: GET
URL: http://127.0.0.1:8000/api/colleges/list/
Auth: Bearer Token (YOUR_TOKEN)
```

#### Query Parameters Tab
```
district        | Chennai
main_stream     | engineering
college_type    | private
verified        | true
ordering        | college_name
page            | 1
```

#### Response
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [...]
}
```

### 3. Using Python Requests

```python
import requests

# Setup
BASE_URL = "http://127.0.0.1:8000/api/colleges/list/"
HEADERS = {"Authorization": "Bearer YOUR_TOKEN"}

# Simple filter
response = requests.get(BASE_URL, 
    params={'district': 'Chennai'},
    headers=HEADERS)
print(response.json())

# Multiple filters
response = requests.get(BASE_URL,
    params={
        'district': 'Chennai',
        'main_stream': 'engineering',
        'college_type': 'private',
        'verified': 'true'
    },
    headers=HEADERS)
colleges = response.json()
print(f"Found {colleges['count']} colleges")
for college in colleges['results']:
    print(f"- {college['college_name']}")
```

### 4. Using JavaScript/Fetch

```javascript
// Setup
const BASE_URL = "http://127.0.0.1:8000/api/colleges/list/";
const token = "YOUR_TOKEN";

// Helper function
async function fetchColleges(filters = {}) {
  const params = new URLSearchParams();
  Object.entries(filters).forEach(([key, value]) => {
    if (value) params.append(key, value);
  });
  
  const response = await fetch(`${BASE_URL}?${params}`, {
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
  });
  
  return await response.json();
}

// Usage
const colleges = await fetchColleges({
  district: 'Chennai',
  main_stream: 'engineering',
  college_type: 'private'
});

console.log(`Found ${colleges.count} colleges`);
colleges.results.forEach(college => {
  console.log(`- ${college.college_name}`);
});
```

## Complete Test Scenarios

### Scenario 1: Search for Engineering Colleges

**User Story**: As a student, I want to find engineering colleges in my district.

**Steps**:
1. Get district value from user input
2. Filter by district and main_stream

```python
# Python
response = requests.get(BASE_URL, params={
    'district': 'Chennai',
    'main_stream': 'engineering'
})
results = response.json()['results']

# JavaScript
const colleges = await fetchColleges({
  district: 'Chennai',
  main_stream: 'engineering'
});
```

**Expected Response**:
```json
{
  "count": 8,
  "results": [
    {
      "id": 1,
      "college_name": "IIT Madras",
      "college_code": "COL-001",
      "college_type": "autonomous",
      "district": "Chennai",
      "main_stream": "engineering",
      "verified": true
    }
  ]
}
```

### Scenario 2: Find Top Private Colleges

**User Story**: Show featured private colleges with AICTE accreditation

**Steps**:
1. Filter by college_type = 'private'
2. Filter by is_featured = true
3. Filter by accreditation_body = 'AICTE'
4. Sort by popularity

```python
response = requests.get(BASE_URL, params={
    'college_type': 'private',
    'is_featured': 'true',
    'accreditation_body': 'AICTE',
    'ordering': '-is_popular'
})
```

**Curl Command**:
```bash
curl "http://127.0.0.1:8000/api/colleges/list/?college_type=private&is_featured=true&accreditation_body=AICTE&ordering=-is_popular"
```

### Scenario 3: Search by Specialization

**User Story**: Find colleges offering Computer Science B.Tech

**Steps**:
1. Filter by degree = 'btech'
2. Filter by specialization containing 'Computer'
3. Filter by level = 'undergraduate'

```python
response = requests.get(BASE_URL, params={
    'degree': 'btech',
    'specialization': 'Computer',
    'level': 'undergraduate'
})
```

### Scenario 4: Find Medical Colleges

**User Story**: Show medical colleges offering MBBS in a state

**Steps**:
1. Filter by main_stream = 'medical'
2. Filter by degree = 'mbbs'
3. Filter by state
4. Verify accreditation

```python
response = requests.get(BASE_URL, params={
    'main_stream': 'medical',
    'degree': 'mbbs',
    'state': 'Tamil Nadu',
    'verified': 'true',
    'accreditation_body': 'MCI'
})
```

### Scenario 5: Pagination Test

**User Story**: Implement infinite scroll pagination

**Steps**:
1. Fetch page 1
2. User scrolls, fetch page 2
3. Continue until no more results

```python
page = 1
all_colleges = []

while True:
    response = requests.get(BASE_URL, params={
        'district': 'Chennai',
        'page': page
    })
    data = response.json()
    
    all_colleges.extend(data['results'])
    
    if not data['next']:
        break
    
    page += 1

print(f"Total colleges: {len(all_colleges)}")
```

## Edge Cases & Error Handling

### Edge Case 1: No Results

**Request**:
```
GET /api/colleges/list/?district=NonExistentDistrict
```

**Response** (200 OK):
```json
{
  "count": 0,
  "next": null,
  "previous": null,
  "results": []
}
```

**Handling**:
```javascript
const colleges = await fetchColleges({ district: 'NonExistent' });
if (colleges.count === 0) {
  console.log('No colleges found. Please try different filters.');
}
```

### Edge Case 2: Invalid Filter Value

**Request**:
```
GET /api/colleges/list/?verified=maybe
```

**Response** (200 OK - Filter Ignored):
```json
{
  "count": 100,  // Returns all colleges, filter ignored
  "results": [...]
}
```

**Note**: Invalid boolean values are ignored by the filter.

### Edge Case 3: Multiple Filters with No Matches

**Request**:
```
GET /api/colleges/list/?district=Delhi&main_stream=engineering&degree=btech&college_type=autonomous&verified=true
```

**Response** (200 OK - Empty):
```json
{
  "count": 0,
  "results": []
}
```

**Handling**:
```python
response = requests.get(BASE_URL, params=filters)
if response.status_code == 200 and response.json()['count'] == 0:
    # Try relaxing filters
    filters.pop('college_type')  # Remove autonomous filter
    response = requests.get(BASE_URL, params=filters)
```

### Edge Case 4: Special Characters in Search

**Request**:
```
GET /api/colleges/list/?search=IIT-M&ordering=college_name
```

**Note**: Hyphens and special characters are handled by Django's ORM

### Edge Case 5: Large Result Sets

**Request**:
```
GET /api/colleges/list/?country=India
```

**Handling**: 
- Results are paginated (default 20 per page)
- Use `page` parameter to navigate
- Check `count` field for total results

```python
response = requests.get(BASE_URL, params={'country': 'India'})
total = response.json()['count']
print(f"Total colleges: {total}")
print(f"Pages needed: {(total + 19) // 20}")  # Ceiling division
```

## Performance Testing

### Load Testing with Apache Bench

```bash
# Simple request (100 requests, 10 concurrent)
ab -n 100 -c 10 "http://127.0.0.1:8000/api/colleges/list/?district=Chennai"

# Results show:
# - Requests per second
# - Mean response time
# - Max response time
```

### Load Testing with Locust

```python
# locustfile.py
from locust import HttpUser, task, between

class CollegeUser(HttpUser):
    wait_time = between(1, 3)
    
    @task(1)
    def filter_by_district(self):
        self.client.get("/api/colleges/list/?district=Chennai")
    
    @task(2)
    def filter_by_stream(self):
        self.client.get("/api/colleges/list/?main_stream=engineering")
    
    @task(1)
    def complex_filter(self):
        self.client.get(
            "/api/colleges/list/?district=Chennai&main_stream=engineering&college_type=private"
        )
```

Run with:
```bash
locust -f locustfile.py --host=http://127.0.0.1:8000
```

## Authentication Testing

### Test Without Token

```bash
curl -X GET "http://127.0.0.1:8000/api/colleges/list/"
```

**Response** (200 OK - Read-only access):
```json
{
  "count": 50,
  "results": [...]  // Public data only
}
```

### Test With Token

```bash
curl -X GET "http://127.0.0.1:8000/api/colleges/list/" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Response** (200 OK - Full access):
```json
{
  "count": 50,
  "results": [...]  // All data
}
```

### Test With Invalid Token

```bash
curl -X GET "http://127.0.0.1:8000/api/colleges/list/" \
  -H "Authorization: Bearer INVALID_TOKEN"
```

**Response** (401 Unauthorized):
```json
{
  "detail": "Invalid token."
}
```

## Browser Testing

### Using Browser Console

```javascript
// Get all colleges
fetch('http://127.0.0.1:8000/api/colleges/list/', {
  headers: {'Authorization': 'Bearer YOUR_TOKEN'}
})
.then(r => r.json())
.then(data => console.log(data));

// Filter colleges
fetch('http://127.0.0.1:8000/api/colleges/list/?district=Chennai&main_stream=engineering', {
  headers: {'Authorization': 'Bearer YOUR_TOKEN'}
})
.then(r => r.json())
.then(data => {
  console.log(`Found ${data.count} colleges`);
  data.results.forEach(c => console.log(c.college_name));
});
```

## Debugging Tips

### 1. Check Filter Names
```bash
# Use Django admin or shell to see model field names
python manage.py shell
>>> from College.models import CollegeProfile
>>> CollegeProfile._meta.fields
```

### 2. Log SQL Queries
```python
# settings.py
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {'class': 'logging.StreamHandler'},
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

### 3. Test Individual Filters
```python
# Test each filter separately
for param in ['district', 'main_stream', 'college_type', 'degree']:
    response = requests.get(BASE_URL, params={param: 'some_value'})
    print(f"{param}: {response.status_code}")
```

## Test Results Template

```
Test Case: Filter Engineering Colleges in Chennai
Date: 2024-11-26
Tester: QA Team

Request:
GET /api/colleges/list/?district=Chennai&main_stream=engineering

Expected:
- Status: 200 OK
- Count > 0
- All results have main_stream='engineering'
- All results have district='Chennai'

Actual:
- Status: 200 OK
- Count: 8
- ✓ All results have engineering courses
- ✓ All results in Chennai

Result: PASS
Notes: Response time 245ms, pagination working correctly
```

## Continuous Integration Testing

```yaml
# .github/workflows/test.yml
name: API Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Run tests
        run: python manage.py test College
      
      - name: API Tests
        run: |
          python manage.py runserver &
          sleep 3
          curl -X GET "http://127.0.0.1:8000/api/colleges/list/"
          pytest tests/api/test_college_filtering.py -v
```

## Automated Test Suite

```python
# tests/test_college_filtering.py

from django.test import TestCase
from rest_framework.test import APIClient
from College.models import CollegeProfile, Course

class CollegeFilteringTests(TestCase):
    fixtures = ['test_colleges.json']
    
    def setUp(self):
        self.client = APIClient()
    
    def test_filter_district(self):
        response = self.client.get('/api/colleges/list/?district=Chennai')
        self.assertEqual(response.status_code, 200)
        self.assertGreater(response.data['count'], 0)
    
    def test_filter_main_stream(self):
        response = self.client.get('/api/colleges/list/?main_stream=engineering')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(all(
            any(c['main_stream'] == 'engineering' for c in college['courses'])
            for college in response.data['results']
        ))
    
    def test_combined_filters(self):
        response = self.client.get(
            '/api/colleges/list/?district=Chennai&main_stream=engineering'
        )
        self.assertEqual(response.status_code, 200)
    
    def test_pagination(self):
        response = self.client.get('/api/colleges/list/?page=1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('next', response.data)
    
    def test_ordering(self):
        response = self.client.get('/api/colleges/list/?ordering=college_name')
        self.assertEqual(response.status_code, 200)
        names = [c['college_name'] for c in response.data['results']]
        self.assertEqual(names, sorted(names))

if __name__ == '__main__':
    import unittest
    unittest.main()
```

---

**Version**: 1.0
**Last Updated**: November 26, 2024
