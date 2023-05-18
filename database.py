import sqlite3

database = sqlite3.connect('database.db')
cursor = database.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS translates(
    translate_id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id INTEGER,
    from_lang TEXT,
    to_lang TEXT,
    original_lang TEXT,
    translated_lang TEXT

)
""")

database.commit()
database.close()
