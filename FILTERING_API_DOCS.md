# College & Course Filtering API Documentation

## Overview
The filtering system automatically derives college categories from their courses. Colleges offering multiple streams (Engineering, Medical, Arts, etc.) will appear in results for any stream they offer.

---

## Course Filtering

### Available Filters

| Filter | Type | Description | Example |
|--------|------|-------------|---------|
| `level` | exact | Course level | `?level=undergraduate` |
| `degree` | exact | Degree type | `?degree=btech` |
| `main_stream` | exact | Main stream | `?main_stream=engineering` |
| `specialization` | icontains | Specialization (substring) | `?specialization=computer` |
| `college__college_code` | exact | College code | `?college__college_code=COL-ABC123` |
| `college__country` | icontains | College country | `?college__country=India` |
| `college__state` | icontains | College state | `?college__state=Tamil+Nadu` |
| `college__district` | icontains | College district | `?college__district=Chennai` |
| `fee__gte` | greater than or equal | Minimum fee | `?fee__gte=50000` |
| `fee__lte` | less than or equal | Maximum fee | `?fee__lte=100000` |

### Course Filtering Examples

```
# Get all undergraduate engineering courses
GET /api/courses/?level=undergraduate&main_stream=engineering

# Get B.Tech courses under 100000 fee
GET /api/courses/?degree=btech&fee__lte=100000

# Get all courses in a specific state
GET /api/courses/?college__state=California

# Get medical courses with specialization containing "cardio"
GET /api/courses/?main_stream=medical&specialization=cardio

# Get all law courses in government colleges
GET /api/courses/?main_stream=law&college_type=government

# Combine multiple filters
GET /api/courses/?level=postgraduate&degree=mtech&college__country=India&fee__gte=50000

# Search and filter
GET /api/courses/?search=computer&main_stream=engineering
```

---

## College Filtering

### Available Filters

| Filter | Type | Description | Example |
|--------|------|-------------|---------|
| `country` | icontains | Country (substring) | `?country=India` |
| `state` | icontains | State (substring) | `?state=Tamil+Nadu` |
| `district` | icontains | District (substring) | `?district=Chennai` |
| `main_stream` | dynamic | Stream from courses | `?main_stream=engineering` |
| `college_type` | exact | College type | `?college_type=private` |
| `verified` | exact | Verification status | `?verified=true` |
| `is_popular` | exact | Popular status | `?is_popular=true` |
| `is_featured` | exact | Featured status | `?is_featured=true` |

### How main_stream Works

**Important:** The `main_stream` filter for colleges works dynamically:

- A college is categorized by the courses it offers
- When filtering by `?main_stream=engineering`, ALL colleges offering engineering courses appear
- A college offering BOTH engineering AND medical courses appears in results for BOTH:
  - `?main_stream=engineering`
  - `?main_stream=medical`

### College Filtering Examples

```
# Get all colleges in a specific state
GET /api/colleges/list/?state=Tamil+Nadu

# Get all private engineering colleges
GET /api/colleges/list/?main_stream=engineering&college_type=private

# Get verified colleges in a district offering medical courses
GET /api/colleges/list/?district=Chennai&main_stream=medical&verified=true

# Get popular colleges in India
GET /api/colleges/list/?country=India&is_popular=true

# Get all featured engineering AND law colleges
GET /api/colleges/list/?main_stream=engineering
GET /api/colleges/list/?main_stream=law

# Search and filter
GET /api/colleges/list/?search=IIT&state=Delhi

# Combine location and stream filters
GET /api/colleges/list/?country=India&state=Maharashtra&main_stream=engineering&is_featured=true
```

---

## Key Features

### 1. **Dynamic Stream Detection**
- No need to manually maintain college main_stream field
- Automatically derived from courses offered
- Updated in real-time as courses are added/removed

### 2. **Multi-Stream Colleges**
Example: If a college offers:
- B.Tech (Engineering) 
- MBBS (Medical)
- BA (Arts)

Then:
- `?main_stream=engineering` → College appears ✓
- `?main_stream=medical` → College appears ✓
- `?main_stream=arts` → College appears ✓

### 3. **Flexible Filtering**
- Case-insensitive location filters (icontains)
- Exact match for streams/types
- Range filtering for fees (gte, lte)
- Text search on college names and descriptions

### 4. **Combined Filters**
Mix and match any filters:
```
GET /api/colleges/list/?state=Delhi&main_stream=engineering&college_type=autonomous&verified=true&is_popular=true
```

---

## Valid Values

### Course Level
- `undergraduate`
- `postgraduate`

### Degree
- `btech`
- `mtech`
- `ba`
- `llb`
- `mba`
- `mbbs`

### Main Stream
- `engineering`
- `law`
- `finance`
- `medical`
- `arts`

### College Type
- `government`
- `private`
- `autonomous`

### Boolean Filters
- `verified=true` or `verified=false`
- `is_popular=true` or `is_popular=false`
- `is_featured=true` or `is_featured=false`

---

## Response Format

### Courses Response
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "college": 1,
      "college_code": "COL-ABC123",
      "college_name": "XYZ Engineering College",
      "main_stream": "engineering",
      "degree": "btech",
      "name": "B.Tech in Computer Science",
      "level": "undergraduate",
      "specialization": "Computer Science",
      "duration": "4 Years",
      "fee": 400000,
      "eligibility": "12th Pass",
      "description": "...",
      "brochure": "...",
      "created_at": "2025-11-19T10:00:00Z",
      "updated_at": "2025-11-19T10:00:00Z"
    }
  ]
}
```

### Colleges Response
```json
{
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "college_name": "XYZ Engineering College",
      "college_code": "COL-ABC123",
      "college_type": "private",
      "country": "India",
      "state": "Tamil Nadu",
      "district": "Chennai",
      "main_streams": ["engineering", "arts"],
      "verified": true,
      "is_popular": true,
      "is_featured": false,
      ...
    }
  ]
}
```

---

## API Endpoints

### Courses
- `GET /api/courses/` - List all courses with filtering
- `GET /api/courses/{id}/` - Get specific course
- `POST /api/courses/` - Create course
- `PUT /api/courses/{id}/` - Update course
- `PATCH /api/courses/{id}/` - Partial update course
- `DELETE /api/courses/{id}/` - Delete course

### Colleges
- `GET /api/colleges/list/` - List all colleges with filtering
- `GET /api/colleges/profile/` - Get authenticated user's college profile
- `PUT /api/colleges/profile/` - Update college profile
- `PATCH /api/colleges/profile/` - Partial update college profile

---

## Ordering

Both endpoints support ordering with the `-` prefix for descending:

### Courses
- `ordering=created_at` → Newest first
- `ordering=-created_at` → Oldest first
- `ordering=fee` → Ascending by fee
- `ordering=-fee` → Descending by fee
- `ordering=duration` → By duration
- `ordering=name` → Alphabetical by name

### Colleges
- `ordering=college_name` → A-Z
- `ordering=-college_name` → Z-A
- `ordering=created_at` → Newest first
- `ordering=-created_at` → Oldest first
- `ordering=-is_popular` → Popular first

---

## Search

Both endpoints support text search:

```
GET /api/courses/?search=python
GET /api/colleges/list/?search=IIT
```

Search fields:
- **Courses**: name, specialization, college__college_name, description
- **Colleges**: college_name, country, state, district, about_college
