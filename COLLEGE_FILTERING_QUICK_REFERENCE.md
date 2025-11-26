# College Filtering API - Quick Reference Guide

## Endpoint
```
GET /api/colleges/list/
```

## Quick Filter Cheat Sheet

### By Location
```bash
# By District
?district=Chennai
?district=bangalore

# By State
?state=Tamil+Nadu
?state=karnataka

# By Country
?country=India
```

### By Industry/Stream
```bash
# Engineering colleges
?main_stream=engineering

# Medical colleges
?main_stream=medical

# Law colleges
?main_stream=law

# Finance/MBA colleges
?main_stream=finance

# Arts colleges
?main_stream=arts
```

### By Degree Type
```bash
# B.Tech colleges
?degree=btech

# M.Tech colleges
?degree=mtech

# MBBS colleges
?degree=mbbs

# BA colleges
?degree=ba

# LLB colleges
?degree=llb

# MBA colleges
?degree=mba
```

### By Course Level
```bash
# Undergraduate programs
?level=undergraduate

# Postgraduate programs
?level=postgraduate
```

### By Specialization
```bash
# Computer Science
?specialization=Computer+Science

# Civil Engineering
?specialization=Civil

# Mechanical Engineering
?specialization=Mechanical
```

### By Status
```bash
# Verified colleges only
?verified=true

# Popular colleges
?is_popular=true

# Featured colleges
?is_featured=true
```

### By College Type
```bash
# Government colleges
?college_type=government

# Private colleges
?college_type=private

# Autonomous colleges
?college_type=autonomous
```

### By Accreditation
```bash
# AICTE accredited
?accreditation_body=AICTE

# NBA accredited
?accreditation_body=NBA

# MCI approved (Medical)
?accreditation_body=MCI
```

## Common Search Combinations

| Use Case | Query |
|----------|-------|
| Engineering colleges in Chennai | `?district=Chennai&main_stream=engineering` |
| Private medical colleges | `?college_type=private&main_stream=medical` |
| Top AICTE colleges | `?accreditation_body=AICTE&is_popular=true` |
| Featured colleges | `?is_featured=true&verified=true` |
| B.Tech colleges | `?degree=btech&main_stream=engineering` |
| Government colleges | `?college_type=government&verified=true` |
| Undergrad CS courses | `?level=undergraduate&specialization=Computer+Science` |
| MBA colleges | `?degree=mba&main_stream=finance` |

## Ordering

```bash
# Sort A-Z by name
?ordering=college_name

# Sort Z-A by name
?ordering=-college_name

# Sort newest first
?ordering=-created_at

# Sort oldest first
?ordering=created_at

# Sort by popularity
?ordering=-is_popular

# Sort by establishment year
?ordering=-established_year
```

## Pagination

```bash
# Get first page
?page=1

# Get second page
?page=2

# Combine with filters
?district=Chennai&main_stream=engineering&page=1
```

## Search

```bash
# Search by college name
?search=IIT

# Search by location
?search=Chennai

# Combine with filters
?college_type=government&search=engineering
```

## Complex Queries

### Query 1: Top Private Engineering Colleges in Tamil Nadu
```
/api/colleges/list/?state=Tamil+Nadu&college_type=private&main_stream=engineering&is_popular=true&ordering=college_name
```

### Query 2: AICTE Accredited B.Tech Colleges in Bangalore
```
/api/colleges/list/?district=Bangalore&degree=btech&accreditation_body=AICTE&verified=true
```

### Query 3: Featured Medical Colleges for MBBS
```
/api/colleges/list/?main_stream=medical&degree=mbbs&is_featured=true&level=undergraduate
```

### Query 4: Government Colleges by Stream with Sorting
```
/api/colleges/list/?college_type=government&main_stream=engineering&ordering=college_name&page=1
```

### Query 5: Computer Science in Top Colleges
```
/api/colleges/list/?specialization=Computer+Science&level=undergraduate&is_popular=true&ordering=-established_year
```

## URL Encoding Tips

| Text | Encoded |
|------|---------|
| Space | `+` or `%20` |
| "Tamil Nadu" | `Tamil+Nadu` |
| "Computer Science" | `Computer+Science` |

## Response Example

```json
{
  "count": 45,
  "next": "http://127.0.0.1:8000/api/colleges/list/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "college_name": "IIT Madras",
      "college_code": "COL-001234",
      "college_type": "autonomous",
      "accreditation_body": "AICTE, NBA",
      "country": "India",
      "state": "Tamil Nadu",
      "district": "Chennai",
      "verified": true,
      "is_popular": true,
      "is_featured": true
    }
  ]
}
```

## All Available Fields to Filter

| Field | Type | Values |
|-------|------|--------|
| `district` | String | Any district name |
| `state` | String | Any state name |
| `country` | String | Any country name |
| `main_stream` | String | engineering, medical, law, finance, arts |
| `degree` | String | btech, mtech, mbbs, ba, llb, mba |
| `level` | String | undergraduate, postgraduate |
| `specialization` | String | Any specialization name |
| `college_type` | String | government, private, autonomous |
| `accreditation_body` | String | AICTE, NBA, MCI, etc. |
| `verified` | Boolean | true, false |
| `is_popular` | Boolean | true, false |
| `is_featured` | Boolean | true, false |

## PowerShell Examples

```powershell
# Get engineering colleges in Chennai
$url = "http://127.0.0.1:8000/api/colleges/list/?district=Chennai&main_stream=engineering"
Invoke-RestMethod -Uri $url -Method Get -Headers @{"Authorization" = "Bearer YOUR_TOKEN"}

# Get private medical colleges (verified)
$url = "http://127.0.0.1:8000/api/colleges/list/?college_type=private&main_stream=medical&verified=true"
Invoke-RestMethod -Uri $url -Method Get

# Get featured colleges, sorted by name
$url = "http://127.0.0.1:8000/api/colleges/list/?is_featured=true&ordering=college_name"
Invoke-RestMethod -Uri $url -Method Get
```

## Python Examples

```python
import requests

# Get engineering colleges in Chennai
params = {
    'district': 'Chennai',
    'main_stream': 'engineering'
}
response = requests.get('http://127.0.0.1:8000/api/colleges/list/', params=params)
colleges = response.json()

# Get private AICTE colleges
params = {
    'college_type': 'private',
    'accreditation_body': 'AICTE',
    'verified': 'true'
}
response = requests.get('http://127.0.0.1:8000/api/colleges/list/', params=params)

# Get popular colleges, paginated
params = {
    'is_popular': 'true',
    'ordering': '-established_year',
    'page': 1
}
response = requests.get('http://127.0.0.1:8000/api/colleges/list/', params=params)
```

## Postman Collection

```json
{
  "info": {
    "name": "College Filtering API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Get All Colleges",
      "request": {
        "method": "GET",
        "url": "http://127.0.0.1:8000/api/colleges/list/"
      }
    },
    {
      "name": "Engineering Colleges in Chennai",
      "request": {
        "method": "GET",
        "url": "http://127.0.0.1:8000/api/colleges/list/?district=Chennai&main_stream=engineering"
      }
    },
    {
      "name": "Private AICTE Colleges",
      "request": {
        "method": "GET",
        "url": "http://127.0.0.1:8000/api/colleges/list/?college_type=private&accreditation_body=AICTE"
      }
    }
  ]
}
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| No results | Try fewer filters, verify filter values |
| Encoding errors | Use `+` for spaces: `Tamil+Nadu` |
| Slow response | Add filters to narrow results, check pagination |
| Invalid filter | Check filter name spelling, verify valid values |
| 404 error | Verify endpoint URL is correct |

## Performance Tips

1. **Use specific filters** instead of generic search
2. **Combine multiple filters** for better results
3. **Always paginate** large result sets
4. **Sort by relevant fields** for consistent results
5. **Cache popular searches** on frontend

---

**Last Updated**: November 26, 2024
**Version**: 1.0
