import sqlite3
from pyprojroot import here


def create_user_info():
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect(here("data/chatbot.db"))
    cursor = conn.cursor()

    # Create Tables
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS user_info (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        occupation TEXT NOT NULL,
        location TEXT NOT NULL,
        age INTEGER NOT NULL,
        gender TEXT NOT NULL,
        interests TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        question TEXT NOT NULL,
        answer TEXT NOT NULL,
        session_id TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES user_info(id)
    );

    CREATE TABLE IF NOT EXISTS summary (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        session_id TEXT NOT NULL,
        summary_text TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES user_info(id)
    );
    """)

    # Insert Sample User if Not Exists
    cursor.execute("""
    INSERT INTO user_info (name, last_name, occupation, country)
    SELECT 'farzad', 'roozitalab', 'senior ML engineer', 'Canada'
    WHERE NOT EXISTS (SELECT 1 FROM user_info);
    """)

    # Commit changes and close the connection
    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_user_info()
