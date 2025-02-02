import sqlite3
def create_database():


    conn = sqlite3.connect('rim_links.db')
    cursor = conn.cursor()


    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rims (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rim_link TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
def save_rim_links_to_db(rim_links):
    conn = sqlite3.connect('rim_links.db')
    cursor = conn.cursor()


    for link in rim_links:
        cursor.execute('INSERT INTO rims (rim_link) VALUES (?)', (link,))
    conn.commit()
    conn.close()