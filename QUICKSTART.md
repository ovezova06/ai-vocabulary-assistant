# Quick Start Guide - AI Vocabulary Assistant

## 🚀 Getting Started in 5 Minutes

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
python app.py
```

### Step 3: Open in Browser
Navigate to: **http://localhost:5000**

---

## 📝 First Time Setup

### Create Your Account
1. Click "Sign up here" on the login page
2. Enter:
   - Username (minimum 3 characters)
   - Email address
   - Password (minimum 6 characters)
   - Confirm password
3. Click "SIGN UP"

### Login
1. Enter your username and password
2. Click "SIGN IN"
3. You'll be redirected to the dashboard

---

## 📚 Using the App

### Adding Words
1. On the dashboard, find the "Add Word with AI Agent" section
2. Type an English word (e.g., "teacher", "environment", "abandon")
3. Click "Generate With AI"
4. The word will be added to your vocabulary with:
   - Phonetic pronunciation
   - Part of speech
   - English meaning
   - Synonyms and antonyms
   - Collocations
   - Example sentence
   - Chinese translation
   - Source information

### Searching Words
1. Use the search box at the top of the dashboard
2. Type any part of a word name
3. Click "Search"
4. View filtered results

### Reviewing Words
1. Click the "Review" button in the top right
2. You'll see a random word from your vocabulary
3. Study the meaning, example, and translation
4. Click "Next Word" to see another word

### Managing Your Vocabulary
- Click "Delete" on any card to remove a word
- Click "Open Source" to visit the reference source
- Search to find specific words

---

## 🎯 Demo Words to Try

Start with these words to see the AI agent in action:

| Word | Part of Speech |
|------|-----------------|
| teacher | noun |
| environment | noun |
| abandon | verb |
| accomplish | verb |
| benevolent | adjective |
| eloquent | adjective |
| perseverance | noun |
| pragmatic | adjective |

---

## 🔧 Troubleshooting

### "Port 5000 is already in use"
Edit `app.py` and change the port:
```python
if __name__ == "__main__":
    app.run(debug=True, port=5001)  # Change port to 5001
```

### Database errors
Delete the `instance/vocabulary.db` file and restart:
```bash
rm instance/vocabulary.db
python app.py
```

### Module import errors
Ensure virtual environment is activated:
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# Then install requirements
pip install -r requirements.txt
```

---

## 📱 Features Overview

✅ **User Management**
- Secure registration and login
- Individual vocabulary per user
- Session management

✅ **AI Agent**
- Demo data for common words
- Fallback generation for unknown words
- Comprehensive word information

✅ **Vocabulary Management**
- Add unlimited words
- Search functionality
- Delete words
- Organize by user

✅ **Review System**
- Random word selection
- Learning-focused display
- Navigation between words

✅ **Modern UI**
- Dark theme
- Responsive design
- Smooth animations
- Professional appearance

---

## 🌐 Deployment Options

### Local Development
```bash
python app.py
```

### Production (Gunicorn)
```bash
pip install gunicorn
gunicorn app:app
```

### Docker (Optional)
```bash
docker build -t ai-vocab .
docker run -p 5000:5000 ai-vocab
```

---

## 📞 Need Help?

1. Check the README.md for detailed documentation
2. Review error messages in the terminal
3. Ensure all dependencies are installed
4. Try resetting the database if issues persist

---

## 🎓 Learning Tips

1. **Regular Review**: Use the review feature daily
2. **Add Context**: Look for words in context of books/movies
3. **Use Examples**: Study the example sentences provided
4. **Practice**: Write sentences using new words
5. **Track Progress**: Monitor your growing vocabulary

---

**Happy Learning! 🎉**

For more information, see README.md in the project root.
