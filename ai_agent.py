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
    if not HF_API_KEY:
        return {
            "word": word,
            "phonetic": "/demo/",
            "part_of_speech": "unknown",
            "meaning": "HF_API_KEY missing",
            "synonyms": "",
            "antonyms": "",
            "collocations": "",
            "example_sentence": "",
            "translation": "",
            "source_name": "Demo",
            "source_url": "https://huggingface.co",
            "added_at": datetime.now().isoformat(),
            "last_reviewed": None
        }

    prompt = f"""
Return ONLY valid JSON for this English word: "{word}".

Use exactly these keys:
word, phonetic, part_of_speech, meaning, synonyms, antonyms, collocations, example_sentence, translation, source_name, source_url

Rules:
- meaning must be in Chinese
- translation must be in Chinese
- example_sentence must be natural English
- synonyms must be comma-separated English words
- antonyms must be comma-separated English words
- collocations must be comma-separated English phrases
- source_name must be "Hugging Face AI"
- source_url must be "https://huggingface.co"
"""

    try:
        response = requests.post(
            "https://router.huggingface.co/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {HF_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "Qwen/Qwen3-32B",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a vocabulary assistant. Return only valid JSON. No markdown."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.2,
                "max_tokens": 600
            },
            timeout=60
        )

        result = response.json()

        if "error" in result:
            raise Exception(result["error"])

        if "choices" not in result:
            raise Exception(f"Unexpected HF response: {result}")

        content = result["choices"][0]["message"]["content"]
        content = content.replace("```json", "").replace("```", "").strip()

        start = content.find("{")
        end = content.rfind("}")
        if start != -1 and end != -1:
            content = content[start:end + 1]

        data = json.loads(content)

        return {
            "word": data.get("word", word),
            "phonetic": data.get("phonetic", ""),
            "part_of_speech": data.get("part_of_speech", ""),
            "meaning": data.get("meaning", ""),
            "synonyms": data.get("synonyms", ""),
            "antonyms": data.get("antonyms", ""),
            "collocations": data.get("collocations", ""),
            "example_sentence": data.get("example_sentence", ""),
            "translation": data.get("translation", ""),
            "source_name": data.get("source_name", "Hugging Face AI"),
            "source_url": data.get("source_url", "https://huggingface.co"),
            "added_at": datetime.now().isoformat(),
            "last_reviewed": None
        }

    except Exception as e:
        return {
            "word": word,
            "phonetic": "/error/",
            "part_of_speech": "unknown",
            "meaning": f"AI request failed: {str(e)}",
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
    word = review_random_word(user_id)

    if not word:
        return None

    return {
        "word": word[2],
        "meaning": word[5]
    }