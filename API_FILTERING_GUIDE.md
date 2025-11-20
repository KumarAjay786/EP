# College & Course Filtering API Documentation

## Course Filtering Endpoints

### Base URL
```
GET /api/courses/
```

### Supported Filters

| Filter | Type | Example | Description |
|--------|------|---------|-------------|
| `level` | exact | `?level=undergraduate` | Filter by course level (undergraduate, postgraduate) |
| `degree` | exact | `?degree=btech` | Filter by degree (btech, mtech, ba, llb, mba, mbbs) |
| `main_stream` | exact | `?main_stream=engineering` | Filter by main stream (engineering, law, finance, medical, arts) |
| `specialization` | contains | `?specialization=computer` | Filter by specialization (case-insensitive) |
| `college__college_code` | exact | `?college__college_code=COL-ABC123` | Filter by college code |
| `college__country` | contains | `?college__country=India` | Filter by college country |
| `college__state` | contains | `?college__state=Tamil+Nadu` | Filter by college state |
| `college__district` | contains | `?college__district=Chennai` | Filter by college district |
| `college__main_stream` | exact | `?college__main_stream=engineering` | Filter by college's main stream |
| `fee__lte` | less than or equal | `?fee__lte=500000` | Filter courses with fee ≤ value |
| `fee__gte` | greater than or equal | `?fee__gte=100000` | Filter courses with fee ≥ value |

### Search Fields
- `specialization` - Full text search
- `college__college_name` - College name search
- `description` - Course description search

### Ordering
```
?ordering=created_at        # Newest first (default is -created_at)
?ordering=-fee              # Highest fee first
?ordering=duration          # Shortest duration first
?ordering=degree            # Alphabetical by degree
```

### Example Queries

#### 1. Find all B.Tech Engineering courses in Tamil Nadu
```
GET /api/courses/?degree=btech&main_stream=engineering&college__state=Tamil+Nadu
```

#### 2. Find undergraduate courses with fee between 100k-500k
```
GET /api/courses/?level=undergraduate&fee__gte=100000&fee__lte=500000
```

#### 3. Find Computer Science courses in verified colleges
```
GET /api/courses/?specialization=computer&college__verified=true
```

#### 4. Search for specific colleges' Engineering courses
```
GET /api/courses/?main_stream=engineering&college__country=India&college__district=Chennai
```

#### 5. Find all medical programs
```
GET /api/courses/?main_stream=medical
```

---

## College Filtering Endpoints

### Base URL
```
GET /api/colleges/list/
```

### Supported Filters

| Filter | Type | Example | Description |
|--------|------|---------|-------------|
| `country` | contains | `?country=India` | Filter by country (case-insensitive) |
| `state` | contains | `?state=Tamil+Nadu` | Filter by state (case-insensitive) |
| `district` | contains | `?district=Chennai` | Filter by district (case-insensitive) |
| `college_type` | exact | `?college_type=private` | Filter by type (government, private, autonomous) |
| `verified` | exact | `?verified=true` | Filter by verification status |
| `is_popular` | exact | `?is_popular=true` | Filter by popular status |
| `is_featured` | exact | `?is_featured=true` | Filter by featured status |

### Search Fields
- `college_name` - College name search
- `country` - Country search
- `state` - State search
- `district` - District search
- `about_college` - College description search

### Ordering
```
?ordering=college_name      # Alphabetical
?ordering=-created_at       # Newest first (default)
?ordering=-is_popular       # Popular colleges first
?ordering=is_featured       # Featured colleges first
```

### How Colleges Are Categorized by Main Stream

Colleges automatically appear in multiple main stream categories based on their courses:

**Example:**
- College A offers: B.Tech (Engineering), B.Tech (Science)
- Filters: `?main_stream=engineering` → Shows College A ✓
- Filters: `?main_stream=medical` → Doesn't show College A (no medical courses)

This is handled dynamically through the `main_streams` field which is computed from related courses.

### Example Queries

#### 1. Find private colleges in Tamil Nadu
```
GET /api/colleges/list/?college_type=private&state=Tamil+Nadu
```

#### 2. Find verified colleges in Chennai
```
GET /api/colleges/list/?verified=true&district=Chennai
```

#### 3. Find government colleges that are popular
```
GET /api/colleges/list/?college_type=government&is_popular=true
```

#### 4. Search for colleges in India
```
GET /api/colleges/list/?country=India
```

#### 5. Find featured colleges
```
GET /api/colleges/list/?is_featured=true&ordering=-created_at
```

---

## Combined Query Examples

### 1. Find Engineering courses in verified private colleges in Tamil Nadu
```
GET /api/courses/?main_stream=engineering&college__college_type=private&college__verified=true&college__state=Tamil+Nadu
```

### 2. Find affordable B.Tech courses
```
GET /api/courses/?degree=btech&fee__lte=300000&college__verified=true
```

### 3. Postgraduate programs in government colleges
```
GET /api/courses/?level=postgraduate&college__college_type=government
```

### 4. Search for "Computer" specialization in popular colleges
```
GET /api/courses/?search=computer&college__is_popular=true
```

---

## Response Format

### Course Response Example
```json
{
    "id": 1,
    "college": "COL-ABC123",
    "college_code": "COL-ABC123",
    "college_name": "IIT Delhi",
    "main_stream": "engineering",
    "degree": "btech",
    "level": "undergraduate",
    "specialization": "Computer Science",
    "duration": "4 Years",
    "fee": 500000,
    "eligibility": "12th Pass with 75% marks",
    "description": "B.Tech in Computer Science",
    "brochure": "/media/courses/brochures/cse_brochure.pdf",
    "created_at": "2025-11-20T10:30:00Z",
    "updated_at": "2025-11-20T10:30:00Z"
}
```

### College Response Example
```json
{
    "id": 1,
    "college_name": "IIT Delhi",
    "college_code": "COL-ABC123",
    "college_type": "government",
    "main_streams": ["engineering", "medical"],
    "country": "India",
    "state": "Delhi",
    "district": "New Delhi",
    "verified": true,
    "is_popular": true,
    "is_featured": false,
    "created_at": "2025-11-15T08:00:00Z",
    "updated_at": "2025-11-20T10:30:00Z"
}
```

---

## Notes

- All text filters are case-insensitive
- Multiple filters can be combined with `&`
- Use `+` or `%20` for spaces in URLs
- Ordering can be combined with any filter
- All timestamps are in UTC (ISO 8601 format)
