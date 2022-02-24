import sqlite3

conn = sqlite3.connect(r'website\Databases\article_database.db')
c = conn.cursor()

print(c.execute('SELECT * FROM Writer'),c.fetchall())
print(c.execute('SELECT * FROM Article'),c.fetchall())