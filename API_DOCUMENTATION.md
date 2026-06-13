# API Documentation - AI Vocabulary Assistant

## Base URL

```
http://localhost:5000
```

## Endpoints

### Authentication Routes

#### GET /
**Description**: Home page / Login redirect  
**Authentication**: Not required  
**Response**: Renders login.html  
**Status Code**: 200

#### GET /register
**Description**: Show registration page  
**Authentication**: Not required  
**Response**: Renders register.html  
**Status Code**: 200

#### POST /register
**Description**: Create new user account  
**Authentication**: Not required  
**Request Body**:
```json
{
  "username": "string (3-50 chars)",
  "email": "string (valid email)",
  "password": "string (6+ chars)",
  "confirm_password": "string (must match password)"
}
```
**Response**: Redirect to / on success  
**Status Codes**: 
- 302: Redirect (success)
- 200: Error response with message

**Validation**:
- Username: minimum 3 characters, must be unique
- Email: must be valid email format, must be unique
- Password: minimum 6 characters
- Passwords must match

#### GET /login
**Description**: Show login page  
**Authentication**: Not required  
**Response**: Renders login.html  
**Status Code**: 200

#### POST /login
**Description**: Authenticate user  
**Authentication**: Not required  
**Request Body**:
```json
{
  "username": "string",
  "password": "string"
}
```
**Response**: 
- Success: Redirect to /dashboard (sets session cookies)
- Failure: Renders login.html with error message

**Status Codes**:
- 302: Redirect (success)
- 200: Login page with error

**Session Variables Set**:
- `user_id`: User's database ID
- `username`: User's username

---

### Dashboard Routes

#### GET /dashboard
**Description**: Main vocabulary dashboard  
**Authentication**: Required (user_id in session)  
**Query Parameters**:
- `search` (optional): String to search words

**Response**: Renders dashboard.html  
**Status Codes**:
- 200: Dashboard page
- 302: Redirect to / (if not authenticated)

**Template Variables**:
- `username`: Current user's username
- `words`: Array of word objects
- `search`: Search query string

**Word Object Structure**:
```
[0] = id (INTEGER)
[1] = user_id (INTEGER)
[2] = word (TEXT)
[3] = phonetic (TEXT)
[4] = part_of_speech (TEXT)
[5] = meaning (TEXT)
[6] = synonyms (TEXT)
[7] = antonyms (TEXT)
[8] = collocations (TEXT)
[9] = example_sentence (TEXT)
[10] = translation (TEXT)
[11] = source_name (TEXT)
[12] = source_url (TEXT)
```

#### POST /ai-add-word
**Description**: Add new word to vocabulary using AI agent  
**Authentication**: Required  
**Request Body**:
```json
{
  "word": "string (English word)"
}
```
**Response**: Redirect to /dashboard  
**Status Codes**:
- 302: Redirect (success or error)
- (Errors are handled via query parameters)

**Process**:
1. Validates word input (not empty)
2. Calls `generate_word_data(word)` from ai_agent.py
3. Inserts record into words table
4. Associates with current user

**Word Data Generated**:
- word, phonetic, part_of_speech
- meaning, synonyms, antonyms
- collocations, example_sentence
- translation, source_name, source_url

#### GET /delete-word/<int:word_id>
**Description**: Delete word from vocabulary  
**Authentication**: Required  
**URL Parameters**:
- `word_id`: ID of word to delete (integer)

**Response**: Redirect to /dashboard  
**Status Code**: 302

**Security**: Only allows deletion of words owned by authenticated user

#### GET /review
**Description**: Review random vocabulary word  
**Authentication**: Required  
**Response**: Renders review.html  
**Status Codes**:
- 200: Review page
- 302: Redirect to / (if not authenticated)

**Template Variables**:
- `word`: Random word object (or None if no words)

**Query**:
```sql
SELECT * FROM words 
WHERE user_id = ? 
ORDER BY RANDOM() LIMIT 1
```

#### GET /logout
**Description**: End user session  
**Authentication**: Required  
**Response**: Redirect to /  
**Status Code**: 302

**Action**: Clears all session data

---

### Error Routes

#### 404 - Not Found
**Description**: Page not found error  
**Response**: Renders 404.html  
**Status Code**: 404

#### 500 - Server Error
**Description**: Internal server error  
**Response**: Renders 500.html  
**Status Code**: 500

---

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL,
    password TEXT NOT NULL
)
```

### Words Table
```sql
CREATE TABLE words (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    word TEXT NOT NULL,
    phonetic TEXT,
    part_of_speech TEXT,
    meaning TEXT,
    synonyms TEXT,
    antonyms TEXT,
    collocations TEXT,
    example_sentence TEXT,
    translation TEXT,
    source_name TEXT,
    source_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

---

## Session Management

### Session Variables
| Variable | Type | Description |
|----------|------|-------------|
| user_id | Integer | Unique user identifier |
| username | String | User's username |

### Session Configuration
- Type: Signed cookies
- Secure: True (production)
- HttpOnly: True
- Duration: 24 hours

---

## Error Responses

### Validation Errors
**Format**: HTML page with error message

**Examples**:
- "Username must be at least 3 characters."
- "Password must be at least 6 characters."
- "Passwords do not match."
- "This email or username already exists."

### Authentication Errors
**Format**: HTML page with error message

**Examples**:
- "Invalid username or password."
- "Username and password are required."

---

## AI Agent API

### Function: generate_word_data(word)

**Input**:
- `word` (str): English word to generate data for

**Output**:
```python
{
    "word": str,
    "phonetic": str,
    "part_of_speech": str,
    "meaning": str,
    "synonyms": str,
    "antonyms": str,
    "collocations": str,
    "example_sentence": str,
    "translation": str,
    "source_name": str,
    "source_url": str
}
```

**Behavior**:
- Returns demo data if word exists in demo_data dictionary
- Generates placeholder data if word is not in demo database
- Always returns all required fields

---

## Rate Limiting

Currently not implemented. Future versions should include:
- Login attempts: Max 5 per minute
- Word additions: Max 100 per hour
- Search queries: Max 1000 per hour

---

## CORS Headers

Not currently set. When integrating with external services, add:

```python
from flask_cors import CORS
CORS(app)
```

---

## Authentication Flow

### Registration Flow
```
1. User accesses /register
2. User fills form (username, email, password, confirm_password)
3. POST /register with form data
4. Server validates input
5. Server checks for duplicates
6. Server inserts user record
7. Server redirects to / (login page)
```

### Login Flow
```
1. User accesses /login
2. User fills form (username, password)
3. POST /login with credentials
4. Server queries user table
5. Server compares password
6. If valid: Sets session variables, redirects to /dashboard
7. If invalid: Returns login.html with error
```

### Vocabulary Management Flow
```
1. Authenticated user on /dashboard
2. User enters word and clicks "Generate With AI"
3. POST /ai-add-word with word
4. Server validates input
5. Server calls generate_word_data(word)
6. Server inserts record in words table
7. Server redirects to /dashboard
8. Dashboard shows updated word list
```

---

## Future API Enhancements

- [ ] RESTful JSON endpoints
- [ ] API key authentication
- [ ] Pagination support
- [ ] Advanced filtering options
- [ ] Bulk operations
- [ ] Export functionality (CSV, JSON)
- [ ] WebSocket for real-time updates
- [ ] GraphQL endpoint
- [ ] OpenAPI/Swagger documentation

---

## Security Considerations

### Current Measures
- SQL injection protection (parameterized queries)
- Session management
- User isolation
- Input validation
- Error handling

### Recommended Additions
- HTTPS/SSL enforcement
- CSRF protection tokens
- Rate limiting
- Password hashing (bcrypt)
- API key validation
- CORS configuration
- Security headers
- Input sanitization

---

## Testing Endpoints

### Test User Creation
```bash
curl -X POST http://localhost:5000/register \
  -d "username=testuser&email=test@example.com&password=password123&confirm_password=password123"
```

### Test Login
```bash
curl -X POST http://localhost:5000/login \
  -d "username=testuser&password=password123"
```

### Test Word Addition
```bash
curl -X POST http://localhost:5000/ai-add-word \
  -d "word=teacher"
```

---

## Performance Notes

- Queries use LIMIT 1 for random word selection
- Index recommendations:
  - users(username)
  - users(email)
  - words(user_id)
  - words(word)
  - words(user_id, created_at)

- Consider pagination for large word lists
- Implement caching for frequently accessed data

---

## Version History

- **v1.0** (Current) - Initial release
  - User authentication
  - Vocabulary management
  - Demo AI agent
  - Review functionality

---

For implementation details, refer to `app.py` and `ai_agent.py`.
