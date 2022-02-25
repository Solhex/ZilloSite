import sqlite3

conn = sqlite3.connect(r'website\databases\article_database.db')
c = conn.cursor()

print(c.execute('SELECT * FROM Writer'),c.fetchall())
print(c.execute('SELECT * FROM Article'),c.fetchall())

conn = sqlite3.connect(r'website\databases\email_subscriptions.db')
c = conn.cursor()

print(c.execute('SELECT * FROM Subscription'),c.fetchall())