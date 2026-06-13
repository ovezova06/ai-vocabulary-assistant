# 📚 AI Vocabulary Assistant

A modern Flask web application for learning English vocabulary with an AI-powered agent. Users can register, log in, add words to their vocabulary, search for words, and review them.

## Features

✨ **User Authentication**
- User registration with email and password validation
- Secure login system with session management
- Password confirmation on registration

🤖 **AI Vocabulary Agent**
- Demo AI agent that generates comprehensive word data
- Supports common English words with realistic data
- Falls back to placeholder data for unknown words
- Data includes: phonetic, part_of_speech, meaning, synonyms, antonyms, collocations, example_sentence, translation, and sources

📖 **Dashboard**
- View all user's vocabulary words
- Search functionality to find words
- Add new words using the AI agent
- Delete words from vocabulary
- Responsive card-based layout

🔄 **Review System**
- Random word selection for review
- Displays word meaning, example, and translation
- Navigate through words one at a time

🎨 **Modern UI**
- Dark theme with green accents
- Responsive design for mobile and desktop
- Split-screen login/register pages
- Smooth animations and transitions

## Tech Stack

- **Backend**: Python Flask 2.3.2
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Environment**: python-dotenv for configuration

## Project Structure

```
ai-vocabulary-assistant/
├── app.py                 # Main Flask application
├── database.py            # Database initialization and setup
├── ai_agent.py            # AI agent for generating vocabulary data
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (API keys, etc.)
├── instance/
│   └── vocabulary.db      # SQLite database
├── static/
│   ├── style.css          # Global styles
│   └── script.js          # Frontend JavaScript
└── templates/
    ├── login.html         # Login page
    ├── register.html      # Registration page
    ├── dashboard.html     # Main vocabulary dashboard
    └── review.html        # Word review page
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone or Download the Project**
   ```bash
   cd ai-vocabulary-assistant
   ```

2. **Create a Virtual Environment** (Recommended)
   ```bash
   python -m venv venv
   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**
   - The `.env` file is included with placeholder values
   - For production, update the `SECRET_KEY` in `.env`

5. **Initialize Database**
   - Database will automatically initialize on first run
   - Tables: `users` and `words` are created automatically

## Running the Application

### Development Mode

```bash
python app.py
```

The application will start on `http://localhost:5000`

### Production Mode (Recommended)

```bash
gunicorn app:app
```

## Usage Guide

### 1. Create an Account
- Navigate to the registration page
- Enter username, email, password, and confirm password
- Click "SIGN UP"

### 2. Login
- Enter your username and password
- Click "SIGN IN"

### 3. Add Words
- On the dashboard, enter an English word in the AI form
- Click "Generate With AI"
- The system will fetch vocabulary data and save it

### 4. Search Words
- Use the search box at the top of the dashboard
- Search by word name
- Click "Search" to filter results

### 5. Review Words
- Click the "Review" button in the topbar
- View a random word with its meaning, example, and translation
- Click "Next Word" to see another word

### 6. Delete Words
- Click the "Delete" button on any vocabulary card
- The word will be permanently removed

## Demo Words

The AI agent includes data for these common words:
- **teacher** - noun, education-related
- **environment** - noun, ecology-related
- **abandon** - verb, action-related
- **accomplish** - verb, achievement-related
- **benevolent** - adjective, character-related
- **eloquent** - adjective, communication-related
- **perseverance** - noun, determination-related
- **pragmatic** - adjective, approach-related

For any other words, the system generates placeholder data.

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

## Security Notes

⚠️ **Important for Production**
- Change the `SECRET_KEY` in `.env`
- Consider using password hashing (bcrypt) for production
- Use HTTPS in production
- Implement CSRF protection
- Add input validation and sanitization
- Consider adding rate limiting

## Future Enhancements

- 🔐 Real password hashing with bcrypt
- 🤖 Integration with real AI APIs (OpenAI, Google Cloud NLP)
- 📊 Progress tracking and statistics
- 🔔 Spaced repetition algorithm for better learning
- 🎯 Difficulty levels and categories
- 📈 Achievement badges and leaderboards
- 🌍 Multiple language support
- 📱 Mobile app version

## Troubleshooting

### Database Issues
- Delete the `instance/vocabulary.db` file to reset the database
- Ensure the `instance/` directory exists

### Port Already in Use
```bash
# Change the port in app.py
app.run(debug=True, port=5001)
```

### Module Not Found Errors
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt` again

## License

This project is open source and available under the MIT License.

## Support

For issues or questions, please create an issue in the repository or contact the development team.

---

**Happy Learning! 📚✨**
