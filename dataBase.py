import sqlite3
import os

def create_database():
    try:
        conn = sqlite3.connect('rim_search.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS rim_links
                     (link TEXT PRIMARY KEY)''')
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Database creation error: {e}")

def save_rim_links_to_db(links):
    try:
        conn = sqlite3.connect('rim_search.db')
        c = conn.cursor()
        for link in links:
            try:
                c.execute("INSERT OR IGNORE INTO rim_links (link) VALUES (?)", (link,))
            except sqlite3.Error as e:
                print(f"Error saving to database: {e}")
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")