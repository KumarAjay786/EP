# College Filtering API Documentation

## Overview

The College Filtering API provides comprehensive filtering and search capabilities for colleges based on multiple criteria including location, courses offered, degree types, course levels, specialization, and college status.

## Base URL

```
http://127.0.0.1:8000/api/colleges/list/
```

## Authentication

- **Permission Required**: `IsAuthenticatedOrReadOnly`
- Authenticated users can access all filters
- Unauthenticated users can only view public listings (read-only)

## Filter Parameters

### 1. Location Filters

#### District Filter
Filters colleges by district (case-insensitive substring matching)

**Parameter**: `district`
**Type**: String
**Example**: 
```
GET /api/colleges/list/?district=Chennai
GET /api/colleges/list/?district=bangalore
```

#### State Filter
Filters colleges by state (case-insensitive substring matching)

**Parameter**: `state`
**Type**: String
**Example**:
```
GET /api/colleges/list/?state=Tamil+Nadu
GET /api/colleges/list/?state=karnataka
```

#### Country Filter
Filters colleges by country (case-insensitive substring matching)

**Parameter**: `country`
**Type**: String
**Example**:
```
GET /api/colleges/list/?country=India
GET /api/colleges/list/?country=USA
```

---

### 2. Industry/Stream Filters

#### Main Stream Filter
Filters colleges by the main stream of courses they offer. A college offering multiple streams will appear in multiple filter results.

**Parameter**: `main_stream`
**Type**: String (exact match)
**Valid Values**:
- `engineering` - Engineering courses
- `medical` - Medical/MBBS courses
- `law` - Law/LLB courses
- `finance` - Finance/MBA courses
- `arts` - Arts/BA/MA courses

**Example**:
```
GET /api/colleges/list/?main_stream=engineering
GET /api/colleges/list/?main_stream=medical
```

---

### 3. Course Details Filters

#### Degree Filter
Filters colleges by degree type offered in their courses

**Parameter**: `degree`
**Type**: String (exact match)
**Valid Values**:
- `btech` - Bachelor of Technology
- `mtech` - Master of Technology
- `mbbs` - Bachelor of Medicine, Bachelor of Surgery
- `ba` - Bachelor of Arts
- `llb` - Bachelor of Laws
- `mba` - Master of Business Administration

**Example**:
```
GET /api/colleges/list/?degree=btech
GET /api/colleges/list/?degree=mbbs
```

#### Course Level Filter
Filters colleges by the level of courses they offer

**Parameter**: `level`
**Type**: String (exact match)
**Valid Values**:
- `undergraduate` - Undergraduate courses (B.Tech, BA, LLB, MBBS)
- `postgraduate` - Postgraduate courses (M.Tech, MBA, MA)

**Example**:
```
GET /api/colleges/list/?level=undergraduate
GET /api/colleges/list/?level=postgraduate
```

#### Specialization Filter
Filters colleges by course specialization (case-insensitive substring matching)

**Parameter**: `specialization`
**Type**: String
**Example**:
```
GET /api/colleges/list/?specialization=Computer+Science
GET /api/colleges/list/?specialization=Civil
```

---

### 4. College Status Filters

#### Verified Filter
Filters colleges by verification status

**Parameter**: `verified`
**Type**: Boolean
**Valid Values**: `true`, `false`

**Example**:
```
GET /api/colleges/list/?verified=true
GET /api/colleges/list/?verified=false
```

#### Popular Filter
Filters colleges marked as popular

**Parameter**: `is_popular`
**Type**: Boolean
**Valid Values**: `true`, `false`

**Example**:
```
GET /api/colleges/list/?is_popular=true
```

#### Featured Filter
Filters colleges marked as featured

**Parameter**: `is_featured`
**Type**: Boolean
**Valid Values**: `true`, `false`

**Example**:
```
GET /api/colleges/list/?is_featured=true
```

---

### 5. College Information Filters

#### College Type Filter
Filters colleges by type/category

**Parameter**: `college_type`
**Type**: String (exact match)
**Valid Values**:
- `government` - Government colleges
- `private` - Private colleges
- `autonomous` - Autonomous colleges

**Example**:
```
GET /api/colleges/list/?college_type=government
GET /api/colleges/list/?college_type=private
```

#### Accreditation Body Filter
Filters colleges by accreditation body (case-insensitive substring matching)

**Parameter**: `accreditation_body`
**Type**: String
**Common Values**:
- `AICTE` - All India Council for Technical Education
- `NBA` - National Board of Accreditation
- `MCI` - Medical Council of India
- `BCI` - Bar Council of India

**Example**:
```
GET /api/colleges/list/?accreditation_body=AICTE
GET /api/colleges/list/?accreditation_body=NBA
```

---

## Search Parameters

### Full Text Search
Search across college name, location, description, and accreditation body

**Parameter**: `search`
**Type**: String
**Searchable Fields**:
- college_name
- country
- state
- district
- about_college
- accreditation_body

**Example**:
```
GET /api/colleges/list/?search=IIT
GET /api/colleges/list/?search=Chennai
```

---

## Ordering Parameters

### Order Results
Sort results by specified field

**Parameter**: `ordering`
**Type**: String
**Valid Fields**:
- `college_name` - Sort by college name (A-Z)
- `-college_name` - Sort by college name (Z-A)
- `created_at` - Sort by creation date (oldest first)
- `-created_at` - Sort by creation date (newest first)
- `is_popular` - Sort by popularity status
- `is_featured` - Sort by featured status
- `established_year` - Sort by establishment year (oldest first)
- `-established_year` - Sort by establishment year (newest first)

**Default Ordering**: `-created_at` (newest first)

**Example**:
```
GET /api/colleges/list/?ordering=college_name
GET /api/colleges/list/?ordering=-established_year
GET /api/colleges/list/?ordering=is_popular
```

---

## Combining Multiple Filters

Filters can be combined to narrow down results. All filters use AND logic by default.

### Examples

#### Example 1: Engineering colleges in a specific district
```
GET /api/colleges/list/?district=Chennai&main_stream=engineering
```
Returns all engineering colleges located in Chennai.

#### Example 2: Private medical colleges that are verified
```
GET /api/colleges/list/?college_type=private&main_stream=medical&verified=true
```
Returns private medical colleges that have been verified.

#### Example 3: Popular colleges offering BTECH in Tamil Nadu
```
GET /api/colleges/list/?state=Tamil+Nadu&degree=btech&is_popular=true
```
Returns popular colleges in Tamil Nadu offering B.Tech degrees.

#### Example 4: AICTE accredited engineering colleges, sorted by name
```
GET /api/colleges/list/?accreditation_body=AICTE&main_stream=engineering&ordering=college_name
```
Returns AICTE-accredited engineering colleges sorted alphabetically.

#### Example 5: Undergraduate Computer Science courses in private colleges
```
GET /api/colleges/list/?specialization=Computer+Science&level=undergraduate&college_type=private
```
Returns private colleges offering undergraduate Computer Science programs.

#### Example 6: Featured undergraduate engineering colleges in India
```
GET /api/colleges/list/?is_featured=true&level=undergraduate&main_stream=engineering&country=India
```
Returns featured undergraduate engineering colleges in India.

#### Example 7: Complete filtering example
```
GET /api/colleges/list/?country=India&state=Karnataka&district=Bangalore&main_stream=engineering&college_type=private&degree=btech&verified=true&is_popular=true&ordering=-created_at
```
Returns private engineering colleges in Bangalore, India offering B.Tech degrees, which are verified and popular, sorted by newest first.

---

## Response Format

### Success Response (200 OK)

```json
{
  "count": 45,
  "next": "http://127.0.0.1:8000/api/colleges/list/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "user": 5,
      "college_name": "Indian Institute of Technology Madras",
      "college_code": "COL-001234",
      "college_type": "autonomous",
      "established_year": 1959,
      "accreditation_body": "AICTE, NBA",
      "country": "India",
      "state": "Tamil Nadu",
      "district": "Chennai",
      "address": "IIT Madras Campus, Chennai",
      "email": "info@iitm.ac.in",
      "phone": "+91-44-2257-8111",
      "website": "https://www.iitm.ac.in",
      "verified": true,
      "approved_by": 3,
      "is_popular": true,
      "is_featured": true,
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-11-26T15:45:00Z"
    }
  ]
}
```

### Pagination
- **Default page size**: 20 results per page
- **Query parameter**: `?page=2`
- **Response fields**: `count`, `next`, `previous`, `results`

---

## HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful, results returned |
| 400 | Bad Request | Invalid filter parameters or query format |
| 401 | Unauthorized | Authentication required (for certain endpoints) |
| 403 | Forbidden | Permission denied |
| 404 | Not Found | No colleges match the filter criteria |
| 500 | Server Error | Internal server error |

---

## Error Responses

### Invalid Filter Parameter
```json
{
  "error": "Invalid value for filter: main_stream. Valid values are: engineering, medical, law, finance, arts"
}
```

### No Results Found
```json
{
  "count": 0,
  "next": null,
  "previous": null,
  "results": []
}
```

---

## Best Practices

### 1. **Use Exact Matches When Possible**
For better performance, use exact match filters instead of substring searches:
```
✓ Good:   ?degree=btech&level=undergraduate
✗ Avoid:  ?search=btech
```

### 2. **Combine Location + Stream Filters**
For better results, always combine location and stream:
```
✓ Better:  ?district=Chennai&main_stream=engineering
✓ Good:    ?main_stream=engineering
```

### 3. **Filter Before Searching**
Narrow down with filters, then use search:
```
GET /api/colleges/list/?college_type=private&verified=true&search=Anna
```

### 4. **Use Pagination**
For large result sets, always implement pagination:
```
GET /api/colleges/list/?district=Chennai&page=1
GET /api/colleges/list/?district=Chennai&page=2
```

### 5. **Sort Results for Better UX**
Always specify an ordering for consistent results:
```
GET /api/colleges/list/?main_stream=engineering&ordering=college_name
```

---

## URL Encoding

When using special characters in query parameters, ensure proper URL encoding:

| Character | Encoded |
|-----------|---------|
| Space | `+` or `%20` |
| & | `%26` |
| ? | `%3F` |
| # | `%23` |

**Examples**:
```
✓ Correct:   ?state=Tamil+Nadu
✓ Correct:   ?state=Tamil%20Nadu
✗ Incorrect: ?state=Tamil Nadu
```

---

## Common Use Cases

### Use Case 1: Find colleges for a student
**Scenario**: Student wants engineering colleges in Chennai that are government or autonomous

```
GET /api/colleges/list/?main_stream=engineering&district=Chennai&college_type=government
GET /api/colleges/list/?main_stream=engineering&district=Chennai&college_type=autonomous
```

Or combine with search:
```
GET /api/colleges/list/?main_stream=engineering&district=Chennai&search=engineering&ordering=is_featured
```

### Use Case 2: Find featured colleges
**Scenario**: Portal wants to show featured colleges to visitors

```
GET /api/colleges/list/?is_featured=true&verified=true&ordering=-is_popular
```

### Use Case 3: Find AICTE accredited colleges
**Scenario**: Show all AICTE accredited colleges

```
GET /api/colleges/list/?accreditation_body=AICTE&verified=true&ordering=college_name
```

### Use Case 4: Medical college search
**Scenario**: Find medical colleges by location and level

```
GET /api/colleges/list/?main_stream=medical&level=undergraduate&state=Maharashtra
```

### Use Case 5: Compare similar colleges
**Scenario**: Find colleges offering same specialization

```
GET /api/colleges/list/?specialization=Computer+Science&main_stream=engineering&ordering=college_name
```

---

## Technical Implementation Details

### Custom FilterSet Class

The filtering system uses a custom `CollegeFilterSet` class that extends Django's `FilterSet`:

```python
class CollegeFilterSet(FilterSet):
    # Location filters (substring match)
    country = CharFilter(field_name='country', lookup_expr='icontains')
    state = CharFilter(field_name='state', lookup_expr='icontains')
    district = CharFilter(field_name='district', lookup_expr='icontains')
    
    # College info filters
    college_type = CharFilter(field_name='college_type', lookup_expr='exact')
    accreditation_body = CharFilter(field_name='accreditation_body', lookup_expr='icontains')
    
    # Course-related filters (handles M2M relations)
    main_stream = CharFilter(field_name='courses__main_stream', lookup_expr='exact', distinct=True)
    degree = CharFilter(field_name='courses__degree', lookup_expr='exact', distinct=True)
    level = CharFilter(field_name='courses__level', lookup_expr='exact', distinct=True)
    specialization = CharFilter(field_name='courses__specialization', lookup_expr='icontains', distinct=True)
    
    # Status filters
    verified = BooleanFilter(field_name='verified')
    is_popular = BooleanFilter(field_name='is_popular')
    is_featured = BooleanFilter(field_name='is_featured')
```

### Distinct Handling
- The `distinct=True` parameter is used on course-related filters to avoid duplicate results
- The `get_queryset()` method calls `.distinct()` to ensure no duplicates in final results

### Related Field Filtering
- Filters can search related Course fields using Django ORM's double-underscore notation
- Example: `courses__main_stream` filters colleges by their related courses' main_stream

---

## Performance Considerations

### Query Optimization
1. **Indexes**: Ensure database indexes on frequently filtered fields:
   - `district`, `state`, `country`
   - `college_type`, `verified`, `is_popular`, `is_featured`
   - `courses__main_stream`, `courses__degree`, `courses__level`

2. **Pagination**: Always implement pagination for large result sets
3. **Caching**: Consider caching popular filter combinations

### Database Optimization
```sql
-- Recommended indexes
CREATE INDEX idx_district ON college_collegeprofile(district);
CREATE INDEX idx_state ON college_collegeprofile(state);
CREATE INDEX idx_college_type ON college_collegeprofile(college_type);
CREATE INDEX idx_verified ON college_collegeprofile(verified);
CREATE INDEX idx_is_popular ON college_collegeprofile(is_popular);
CREATE INDEX idx_is_featured ON college_collegeprofile(is_featured);
CREATE INDEX idx_course_main_stream ON college_course(main_stream);
CREATE INDEX idx_course_degree ON college_course(degree);
CREATE INDEX idx_course_level ON college_course(level);
```

---

## Troubleshooting

### Issue: No results returned
**Solution**: 
- Verify filter values match available data
- Check URL encoding for special characters
- Use search parameter to debug: `?search=college_name`

### Issue: Duplicate results
**Solution**: Already handled by custom FilterSet with `distinct=True` and `get_queryset().distinct()`

### Issue: Slow queries
**Solution**:
- Use more specific filters (exact match over substring)
- Combine filters to narrow results
- Implement pagination
- Check database indexes exist

### Issue: Filter not working
**Solution**:
- Verify correct parameter name (case-sensitive)
- Check for URL encoding issues
- Use browser developer tools to inspect actual request

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024-11-26 | Initial release with comprehensive filtering |

---

## Support

For issues or questions regarding the College Filtering API, please contact:
- **Backend Team**: backend@educationpioneer.com
- **Documentation**: [Full API Documentation](./API_DOCUMENTATION.md)
- **Issues**: Report via GitHub Issues

---

## Related Documentation

- [Course Filtering API](./COURSE_FILTERING_DOCUMENTATION.md)
- [College Profile Setup API](./COLLEGE_PROFILE_DOCUMENTATION.md)
- [Authentication & Permissions](./AUTHENTICATION_DOCUMENTATION.md)
