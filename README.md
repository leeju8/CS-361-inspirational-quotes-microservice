# Inspirational Quotes Microservice

A simple microservice that returns an inspirational quote.

# Running the Service

```bash
pip3 install -r requirements.txt
python3 app.py
```

# Requesting and Receiving Data

### Get Random Quote

**Endpoint:** 'GET /api/quote'

**Request:** Client sends a GET request with an empty body

Example:

```bash
curl http://localhost:5000/api/quote
```

**Response (Success):** Client receives 200 OK Status Code

**Response (Failure):** Client receives 404 NOT FOUND Status Code and JSON body containing:

```json
{
  "quote": {
    "id": 0,
    "quote": "No quotes available"
  }
}
```

### Add New Quote

**Endpoint:** 'POST /api/quote'

**Request:** Client sends a POST request with JSON body containing:

- 'quote': The quote you want to add

**Example:**

```bash
curl -X POST http://localhost:5000/api/quote \
  -H "Content-Type: application/json" \
  -d '{
    "quote": "Example quote I want to add"
  }'
```

**Response (Success):** Client receives 201 CREATED Status Code and JSON body containing:

```json
{
  {
    "message": "Quote added successfully!",
    "quote": {
      "id": "6",
      "quote": "Example quote that was added"
    }
  }
}
```

**Response (Failure):** Client receives 400 BAD REQUEST Status Code and JSON body containing:

```json
{
  "error": "Missing 'quote' field"
}
```

### Update Quote

**Endpoint:** 'PUT /api/quote/id'

**Request:** Client sends a PUT request with JSON body containing:

- 'quote': The updated quote text

Replace '<id>' with the ID of the quote you want to update

**Example:**

```bash
curl -X PUT http://localhost:5000/api/quote/2 \
  -H "Content-Type: application/json" \
  -d '{
    "quote": "Inspirational quote I want to update"
  }'
```

**Response (Success):** Client receives 200 OK Status Code and JSON body containing:

```json
{
  "message": "Quote updated!",
  "quote": {
    "id": 6,
    "quote": "Inspirational quote that was updated"
  }
}
```

**Response (Failure ):** Client receives 404 NOT FOUND Status Code and JSON body containing:

```json
{
  "error": "Quote not found"
}
```

# UML Sequence Diagram
