import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv
import sqlite3

load_dotenv()
HF_API_KEY = os.getenv("HF_API_KEY")
DB_PATH = "instance/vocabulary.db"

def generate_word_data(word):
    """Hugging Face API üzerinden kelime verisi üretir."""
    if not HF_API_KEY:
        return {
            "word": word,
            "phonetic": "/demo/",
            "part_of_speech": "unknown",
            "meaning": "Demo mode: HF_API_KEY missing",
            "synonyms": "",
            "antonyms": "",
            "collocations": "",
            "example_sentence": "",
            "translation": "",
            "source_name": "Demo",
            "source_url": "https://example.com"
        }

    prompt = f"""
You are an English vocabulary assistant.

Generate vocabulary data for the word "{word}".
Return ONLY JSON with keys:
word, phonetic, part_of_speech, meaning, synonyms, antonyms, collocations, example_sentence, translation, source_name, source_url.

- meaning in Chinese
- translation in Chinese
- example_sentence natural English
- synonyms comma-separated
- antonyms comma-separated
- collocations comma-separated
- source_name: Hugging Face AI
- source_url: https://huggingface.co
"""

    try:
        response = requests.post(
            "https://router.huggingface.co/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {HF_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "moonshotai/Kimi-K2-Instruct-0905",
                "messages": [
                    {"role": "system", "content": "You are a vocabulary assistant. Return JSON only."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.3,
                "max_tokens": 500
            },
            timeout=40
        )

        result = response.json()
        content = result["choices"][0]["message"]["content"]
        content = content.replace("```json", "").replace("```", "").strip()
        data = json.loads(content)
        data["word"] = word
        data["added_at"] = datetime.now().isoformat()
        data["last_reviewed"] = None
        return data

    except Exception as e:
        # API başarısız olursa demo veri
        return {
            "word": word,
            "phonetic": "/error/",
            "part_of_speech": "unknown",
            "meaning": f"AI request failed: {e}",
            "synonyms": "",
            "antonyms": "",
            "collocations": "",
            "example_sentence": "",
            "translation": "",
            "source_name": "HF API Error",
            "source_url": "https://huggingface.co",
            "added_at": datetime.now().isoformat(),
            "last_reviewed": None
        }

def add_word_to_db(user_id, data):
    """Verilen kelimeyi SQLite DB'ye ekler."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO words
        (user_id, word, phonetic, part_of_speech, meaning, synonyms, antonyms, collocations,
         example_sentence, translation, source_name, source_url, added_at, last_reviewed)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        data["word"],
        data.get("phonetic", ""),
        data.get("part_of_speech", ""),
        data.get("meaning", ""),
        data.get("synonyms", ""),
        data.get("antonyms", ""),
        data.get("collocations", ""),
        data.get("example_sentence", ""),
        data.get("translation", ""),
        data.get("source_name", ""),
        data.get("source_url", ""),
        data.get("added_at"),
        data.get("last_reviewed")
    ))
    conn.commit()
    conn.close()

def review_random_word(user_id):
    """Rastgele bir kelime seçer ve last_reviewed tarihini günceller."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM words WHERE user_id = ? ORDER BY RANDOM() LIMIT 1",
        (user_id,)
    )
    word = cursor.fetchone()
    if word:
        cursor.execute(
            "UPDATE words SET last_reviewed=? WHERE id=?",
            (datetime.now().isoformat(), word[0])
        )
        conn.commit()
    conn.close()
    return word

def query_word(user_id, word):
    """DB'den kelimeyi getirir."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM words WHERE user_id=? AND word LIKE ? ORDER BY id DESC LIMIT 1",
        (user_id, f"%{word}%")
    )
    result = cursor.fetchone()
    conn.close()
    return result

def generate_quiz(user_id):
    """Rastgele bir kelime seçip quiz için döndürür."""
    word = review_random_word(user_id)
    if not word:
        return None
    return {
        "word": word[2],
        "meaning": word[5]
    }