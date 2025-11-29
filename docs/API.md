# KB-Agent API Documentation

Complete API reference for KB-Agent backend services.

## Base URL

```
http://localhost:5000
```

## API Endpoints

### Health Check

#### GET /api/health
Check if the API is running and healthy.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00.000000"
}
```

---

### Documents

#### GET /api/documents
Retrieve all indexed documents.

**Response:**
```json
{
  "success": true,
  "count": 5,
  "documents": [
    {
      "id": "doc_001",
      "title": "Annual Leave Policy",
      "section": "HR Policies",
      "content": "Full policy content..."
    },
    ...
  ]
}
```

---

### Search

#### POST /api/search
Search documents using keyword matching.

**Request Body:**
```json
{
  "query": "annual leave entitlement"
}
```

**Response:**
```json
{
  "success": true,
  "query": "annual leave entitlement",
  "results": [
    {
      "id": "doc_001",
      "title": "Annual Leave Policy",
      "section": "HR Policies",
      "content": "Policy content...",
      "score": 0.85,
      "relevance": "Very High"
    },
    ...
  ],
  "count": 3
}
```

---

### Query Processing

#### POST /api/query
Submit a user query and get a response with relevant documents.

**Request Body:**
```json
{
  "query": "How many days of leave am I entitled to?"
}
```

**Response:**
```json
{
  "success": true,
  "query": "How many days of leave am I entitled to?",
  "response": "**Based on Annual Leave Policy (HR Policies):**\n\n• Full-time employees are entitled to 20 days of annual leave per year...",
  "sources": [
    {
      "title": "Annual Leave Policy",
      "section": "HR Policies"
    },
    {
      "title": "Employee Handbook",
      "section": "HR Operations"
    }
  ],
  "timestamp": "2024-01-15T10:35:00.000000"
}
```

---

### Query Logs

#### GET /api/logs
Retrieve all query logs.

**Query Parameters:**
- `limit` (optional): Number of logs to return

**Response:**
```json
{
  "success": true,
  "count": 42,
  "logs": [
    {
      "id": "a1b2c3d4",
      "timestamp": "2024-01-15T10:35:00.000000",
      "query": "How many days of leave am I entitled to?",
      "answered": true,
      "sources": [
        {
          "title": "Annual Leave Policy",
          "section": "HR Policies"
        }
      ]
    },
    ...
  ]
}
```

---

### Analytics

#### GET /api/stats
Get system statistics and analytics.

**Response:**
```json
{
  "success": true,
  "stats": {
    "total_documents": 5,
    "total_queries": 42,
    "answered_queries": 38,
    "response_rate": "90.5%",
    "vector_db_status": "Active",
    "query_logging": "Active",
    "avg_response_time": "< 1 second"
  }
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "success": false,
  "error": "Query cannot be empty"
}
```

### 404 Not Found
```json
{
  "success": false,
  "error": "Endpoint not found"
}
```

### 500 Internal Server Error
```json
{
  "success": false,
  "error": "Internal server error"
}
```

---

## Search Algorithm

The search service uses a keyword-based relevance scoring algorithm:

1. **Word Matching** (60% weight)
   - Matches query words against document content
   - Score: number of matches / total query words

2. **Phrase Matching** (30% bonus)
   - Checks if complete phrase appears in document
   - Adds 0.3 to score if found

3. **Title/Section Matching** (up to 25% bonus)
   - Boosts score if query words appear in title or section
   - Each match adds 0.15 to score

**Final Score = (word_match × 0.6) + phrase_bonus + title_bonus**

Score range: 0.0 to 1.0

Relevance labels:
- **Very High**: 0.8 - 1.0
- **High**: 0.6 - 0.8
- **Medium**: 0.4 - 0.6
- **Low**: 0.3 - 0.4

---

## Rate Limiting

Currently no rate limiting is implemented. Production deployments should add rate limiting for security.

---

## Authentication

Currently no authentication is required. Production deployments should implement JWT or OAuth2.

---

## CORS

The API supports CORS with the following origins (configurable in `.env`):
- `http://localhost:3000`
- `http://localhost:5000`

---

## Request Examples

### Using curl

**Query documents:**
```bash
curl -X POST http://localhost:5000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "How do I request leave?"}'
```

**Get all documents:**
```bash
curl http://localhost:5000/api/documents
```

**Get query logs:**
```bash
curl http://localhost:5000/api/logs
```

### Using Python

```python
import requests

API_URL = "http://localhost:5000"

# Submit a query
response = requests.post(
    f"{API_URL}/api/query",
    json={"query": "What is the remote work policy?"}
)
print(response.json())

# Get all documents
response = requests.get(f"{API_URL}/api/documents")
print(response.json())

# Get statistics
response = requests.get(f"{API_URL}/api/stats")
print(response.json())
```

### Using JavaScript/Fetch

```javascript
const API_URL = "http://localhost:5000";

// Submit a query
fetch(`${API_URL}/api/query`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ query: "How do I request leave?" })
})
  .then(r => r.json())
  .then(data => console.log(data));

// Get all documents
fetch(`${API_URL}/api/documents`)
  .then(r => r.json())
  .then(data => console.log(data));
```

---

## Webhooks

Webhooks are not currently implemented but can be added in future versions.

---

## Changelog

### v1.0.0
- Initial API release
- Document retrieval
- Semantic search
- Query processing
- Query logging
- System statistics

---

## Support

For API issues or questions:
- Check the main README.md
- Review the SETUP.md guide
- Open a GitHub issue
