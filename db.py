import sqlite3 

con = sqlite3.connect("url.db")
cursor = con.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS urls (id INTEGER PRIMARY KEY , main_url TEXT NOT NULL, short_url TEXT UNIQUE NOT NULL);")
con.commit()
con.close()