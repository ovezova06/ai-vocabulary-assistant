from flask import Flask, render_template, request, redirect, session, flash, jsonify
from database import init_db
from ai_agent import generate_word_data
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "ai_vocab_secret_key_change_in_production")

DB_PATH = "instance/vocabulary.db"
init_db()
def record_history(user_id, word_id, word, action):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO learning_history (user_id, word_id, word, action)
        VALUES (?, ?, ?, ?)
    """, (user_id, word_id, word, action))
    conn.commit()
    conn.close()


@app.route("/")
def home():
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    
    username = request.form.get("username", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")
    confirm_password = request.form.get("confirm_password", "")

    if not all([username, email, password, confirm_password]):
        return render_template("register.html", error="All fields are required.")
    
    if len(username) < 3:
        return render_template("register.html", error="Username must be at least 3 characters.")
    
    if len(password) < 6:
        return render_template("register.html", error="Password must be at least 6 characters.")
    
    if password != confirm_password:
        return render_template("register.html", error="Passwords do not match.")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users(username, email, password) VALUES (?, ?, ?)",
            (username, email, password)
        )
        conn.commit()
        conn.close()
        return redirect("/")
    except sqlite3.IntegrityError:
        conn.close()
        return render_template("register.html", error="This email or username already exists.")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    if not username or not password:
        return render_template("login.html", error="Username and password are required.")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?",
        (username, password)
    )

    user = cursor.fetchone()
    conn.close()

    if user:
        session["user_id"] = user[0]
        session["username"] = user[1]
        return redirect("/dashboard")

    return render_template("login.html", error="Invalid username or password.")


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/")

    search = request.args.get("search", "")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if search:
        cursor.execute(
            "SELECT * FROM words WHERE user_id = ? AND word LIKE ? ORDER BY id DESC",
            (session["user_id"], f"%{search}%")
        )
    else:
        cursor.execute(
            "SELECT * FROM words WHERE user_id = ? ORDER BY id DESC",
            (session["user_id"],)
        )

    words = cursor.fetchall()
    conn.close()

    return render_template(
        "dashboard.html",
        username=session["username"],
        words=words,
        search=search
    )


@app.route("/ai-add-word", methods=["POST"])
def ai_add_word():
    if "user_id" not in session:
        return redirect("/")

    word = request.form.get("word", "").strip()
    if not word:
        return redirect("/dashboard?error=Word cannot be empty")

    try:
        data = generate_word_data(word)

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO words
            (user_id, word, phonetic, part_of_speech, meaning, synonyms, antonyms,
            collocations, example_sentence, translation, source_name, source_url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            session["user_id"],
            data["word"],
            data["phonetic"],
            data["part_of_speech"],
            data["meaning"],
            data["synonyms"],
            data["antonyms"],
            data["collocations"],
            data["example_sentence"],
            data["translation"],
            data["source_name"],
            data["source_url"]
        ))

        word_id = cursor.lastrowid

        conn.commit()
        conn.close()

        record_history(session["user_id"], word_id, data["word"], "added")

        return redirect("/dashboard")

    except Exception:
        return redirect("/dashboard?error=Failed to add word")


@app.route("/delete-word/<int:word_id>")
def delete_word(word_id):
    if "user_id" not in session:
        return redirect("/")

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM words WHERE id = ? AND user_id = ?",
            (word_id, session["user_id"])
        )

        conn.commit()
        conn.close()

    except Exception:
        pass
    
    return redirect("/dashboard")


@app.route("/review")
def review():
    if "user_id" not in session:
        return redirect("/")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM words WHERE user_id = ? ORDER BY RANDOM() LIMIT 1",
        (session["user_id"],)
    )

    word = cursor.fetchone()

    if word:
        cursor.execute("""
            UPDATE words
            SET review_count = review_count + 1,
                last_reviewed = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (word[0],))

        conn.commit()

        record_history(
            session["user_id"],
            word[0],
            word[2],
            "reviewed"
        )

    conn.close()

    return render_template("review.html", word=word)
@app.route("/quiz")
def quiz():
    if "user_id" not in session:
        return redirect("/")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, word, phonetic, meaning, example_sentence, translation FROM words WHERE user_id = ? ORDER BY RANDOM() LIMIT 10",
        (session["user_id"],)
    )
    quiz_words = cursor.fetchall()

    cursor.execute(
        "SELECT meaning FROM words WHERE user_id = ?",
        (session["user_id"],)
    )
    all_meanings = [row[0] for row in cursor.fetchall()]

    conn.close()

    if len(quiz_words) < 4:
        return render_template("quiz.html", error="You need at least 4 words to start a real quiz.", questions=[])

    questions = []

    import random

    for word in quiz_words:
        correct_meaning = word[3]

        wrong_options = [m for m in all_meanings if m != correct_meaning]
        wrong_options = random.sample(wrong_options, min(3, len(wrong_options)))

        options = wrong_options + [correct_meaning]
        random.shuffle(options)

        questions.append({
            "word_id": word[0],
            "word": word[1],
            "phonetic": word[2],
            "correct": correct_meaning,
            "options": options,
            "example": word[4],
            "translation": word[5]
        })

    return render_template("quiz.html", questions=questions, error=None)


@app.route("/history")
def history():
    if "user_id" not in session:
        return redirect("/")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT word, action, created_at
        FROM learning_history
        WHERE user_id = ?
        ORDER BY created_at DESC
    """, (session["user_id"],))

    history_items = cursor.fetchall()
    conn.close()

    return render_template("history.html", history_items=history_items)

@app.route("/statistics")
def statistics():
    if "user_id" not in session:
        return redirect("/")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM words WHERE user_id = ?", (session["user_id"],))
    total_words = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM learning_history WHERE user_id = ? AND action = 'added'", (session["user_id"],))
    total_added = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM learning_history WHERE user_id = ? AND action = 'reviewed'", (session["user_id"],))
    total_reviews = cursor.fetchone()[0]

    cursor.execute("""
        SELECT word, review_count
        FROM words
        WHERE user_id = ?
        ORDER BY review_count DESC
        LIMIT 5
    """, (session["user_id"],))
    top_reviewed = cursor.fetchall()

    conn.close()

    return render_template(
        "statistics.html",
        total_words=total_words,
        total_added=total_added,
        total_reviews=total_reviews,
        top_reviewed=top_reviewed
    )

# =====================================================
# OpenClaw / Telegram Agent API
# Commands:
# add abandon
# query abandon
# review
# quiz
# =====================================================

@app.route("/api/agent", methods=["POST"])
def api_agent():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()

    if not message:
        return jsonify({
            "reply": "Please send a command. Available commands: add word, query word, review, quiz"
        })

    parts = message.split()
    command = parts[0].lower()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM users WHERE username = ?",
        ("telegram_user",)
    )
    user = cursor.fetchone()

    if not user:
        cursor.execute(
            "INSERT INTO users(username, email, password) VALUES (?, ?, ?)",
            ("telegram_user", "telegram@example.com", "telegram123")
        )
        conn.commit()
        user_id = cursor.lastrowid
    else:
        user_id = user[0]

    if command == "add" and len(parts) >= 2:
        word = parts[1].strip()

        try:
            info = generate_word_data(word)

            cursor.execute("""
                INSERT INTO words
                (user_id, word, phonetic, part_of_speech, meaning, synonyms, antonyms,
                collocations, example_sentence, translation, source_name, source_url)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                user_id,
                info["word"],
                info["phonetic"],
                info["part_of_speech"],
                info["meaning"],
                info["synonyms"],
                info["antonyms"],
                info["collocations"],
                info["example_sentence"],
                info["translation"],
                info["source_name"],
                info["source_url"]
            ))

            conn.commit()
            conn.close()

            reply = f"""
✅ Word added successfully!

Word: {info["word"]}

Phonetic: {info["phonetic"]}

Part of Speech: {info["part_of_speech"]}

Meaning: {info["meaning"]}

Synonyms: {info["synonyms"]}

Antonyms: {info["antonyms"]}

Collocations: {info["collocations"]}

Example: {info["example_sentence"]}

Translation: {info["translation"]}

Source: {info["source_name"]}
URL: {info["source_url"]}
"""
            return jsonify({"reply": reply})

        except Exception as e:
            conn.close()
            return jsonify({"reply": f"Failed to add word: {str(e)}"})

    elif command == "query" and len(parts) >= 2:
        word = parts[1].strip()

        cursor.execute(
            "SELECT * FROM words WHERE user_id = ? AND word LIKE ? ORDER BY id DESC LIMIT 1",
            (user_id, f"%{word}%")
        )

        result = cursor.fetchone()
        conn.close()

        if not result:
            return jsonify({"reply": f"No vocabulary record found for: {word}"})

        reply = f"""
🔎 Vocabulary Result

Word: {result[2]}

Phonetic: {result[3]}

Part of Speech: {result[4]}

Meaning: {result[5]}

Synonyms: {result[6]}

Antonyms: {result[7]}

Collocations: {result[8]}

Example: {result[9]}

Translation: {result[10]}

Source: {result[11]}
URL: {result[12]}
"""
        return jsonify({"reply": reply})

    elif command == "review":
        cursor.execute(
            "SELECT * FROM words WHERE user_id = ? ORDER BY RANDOM() LIMIT 1",
            (user_id,)
        )

        result = cursor.fetchone()
        conn.close()

        if not result:
            return jsonify({"reply": "No words found. Use 'add word' first."})

        reply = f"""
📖 Review Word

Word: {result[2]}

Meaning: {result[5]}

Example: {result[9]}

Translation: {result[10]}
"""
        return jsonify({"reply": reply})

    elif command == "quiz":
        cursor.execute(
            "SELECT * FROM words WHERE user_id = ? ORDER BY RANDOM() LIMIT 1",
            (user_id,)
        )

        result = cursor.fetchone()
        conn.close()

        if not result:
            return jsonify({"reply": "No words found. Use 'add word' first."})

        reply = f"""
📝 Quiz

What is the meaning of this word?

Word: {result[2]}

Try to answer first.

Answer: {result[5]}
"""
        return jsonify({"reply": reply})

    conn.close()

    return jsonify({
        "reply": "Unknown command. Available commands: add word, query word, review, quiz"
    })


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template("500.html"), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)