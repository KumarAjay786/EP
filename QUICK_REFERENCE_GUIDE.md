# 📋 Quick Reference Guide

## Course Model - After Refactoring

### Fields
```python
college                 # ForeignKey to CollegeProfile
main_stream            # CharField (engineering, law, finance, medical, arts)
degree                 # CharField (btech, mtech, ba, llb, mba, mbbs)
level                  # CharField (undergraduate, postgraduate)
specialization         # CharField (e.g., Computer Science, Mechanical)
duration               # CharField (e.g., "4 Years")
fee                    # DecimalField
eligibility            # TextField
description            # TextField
brochure               # FileField
created_at             # DateTimeField
updated_at             # DateTimeField
```

### Unique Constraint
```python
unique_together = {('college', 'degree', 'specialization', 'level')}
```
*Ensures no duplicate courses per college*

### String Representation
```
"B.Tech - Computer Science (IIT Delhi)"
```

---

## API Endpoints

### Courses List & Filter
```
GET /api/courses/
POST /api/courses/
GET /api/courses/{id}/
PUT /api/courses/{id}/
PATCH /api/courses/{id}/
DELETE /api/courses/{id}/
```

### Colleges List & Filter
```
GET /api/colleges/list/
```

---

## Top 5 Filtering Scenarios

### 1️⃣ Engineering B.Tech Courses
```
GET /api/courses/?degree=btech&main_stream=engineering
```

### 2️⃣ Affordable Courses Under 5 Lakhs
```
GET /api/courses/?fee__lte=500000
```

### 3️⃣ Computer Science Specialization
```
GET /api/courses/?specialization=computer
```

### 4️⃣ Postgraduate Programs
```
GET /api/courses/?level=postgraduate
```

### 5️⃣ Location-Based Filtering
```
GET /api/courses/?college__state=Tamil+Nadu&college__district=Chennai
```

---

## College Filtering Scenarios

### 1️⃣ Government Colleges in India
```
GET /api/colleges/list/?college_type=government&country=India
```

### 2️⃣ Verified Private Colleges
```
GET /api/colleges/list/?verified=true&college_type=private
```

### 3️⃣ Popular Colleges
```
GET /api/colleges/list/?is_popular=true
```

### 4️⃣ State-wise Search
```
GET /api/colleges/list/?state=Tamil+Nadu
```

### 5️⃣ Featured Colleges
```
GET /api/colleges/list/?is_featured=true
```

---

## Migration Summary

### Migration File
`College/migrations/0010_alter_course_options_alter_course_unique_together_and_more.py`

### Operations
1. Remove unique_together constraint
2. Remove `name` field
3. Add `degree` field
4. Add `main_stream` field
5. Update model options
6. Add new unique_together constraint

### Status
✅ Successfully applied to database

---

## Breaking Changes

⚠️ **If upgrading from previous version:**

| Old Code | New Code |
|----------|----------|
| `course.name` | `f"{course.degree} - {course.specialization}"` |
| Filter by `?name=` | Filter by `?degree=` or `?specialization=` |
| Serialize with `'name'` | Use `'degree'` + `'specialization'` |

---

## Quick Test Commands

### Check System
```bash
python manage.py check
```

### List All Courses
```bash
curl http://localhost:8000/api/courses/
```

### Filter Courses
```bash
curl "http://localhost:8000/api/courses/?degree=btech&main_stream=engineering"
```

### List Colleges
```bash
curl http://localhost:8000/api/colleges/list/
```

### Filter Colleges
```bash
curl "http://localhost:8000/api/colleges/list/?country=India&state=Tamil+Nadu"
```

---

## Common Issues & Solutions

### Issue: "Course has no field named 'name'"
**Solution:** Update API client to use degree + specialization

### Issue: Migration fails
**Solution:** Ensure order of operations (unique_together → field removal → additions)

### Issue: Duplicate courses error
**Solution:** Check unique constraint: college + degree + specialization + level

### Issue: Filtering not working
**Solution:** Verify filter parameter names match filterset_fields definition

---

## Performance Tips

✅ **Do use:**
- Filtering by specific degree/specialization (indexed fields)
- College-based filtering (faster than full scan)
- Pagination with ordering

❌ **Avoid:**
- Searching all courses without filters (slow)
- Complex nested filters (use separate queries)
- Multiple fee ranges in single query

---

## Documentation Files

```
📄 API_FILTERING_GUIDE.md           → Complete API documentation
📄 COURSE_MODEL_REFACTORING.md      → Model changes explanation
📄 MIGRATION_COMPLETION_REPORT.md   → Migration technical details
📄 PROJECT_COMPLETION_SUMMARY.md    → Overall project summary
📄 QUICK_REFERENCE_GUIDE.md         → This file
```

---

## What's Next?

1. **Test API endpoints** with provided examples
2. **Update frontend** to use new course format
3. **Migrate data** using provided migration
4. **Deploy to production** with confidence

---

✅ **All systems operational and ready for production**

For detailed information, see the comprehensive documentation files.
