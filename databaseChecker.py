# WARNING this file is a temp file not to be used within the final product
# this is just used to check if the databases are in working order and 
# the infromation within them.

# This file is NOT needed for the program to work and SHOULD be deleted if
# it is still present here

import sqlite3

conn = sqlite3.connect(r'website\databases\article_database.db')
c = conn.cursor()

print(c.execute('SELECT * FROM Writer'),c.fetchall())
print(c.execute('SELECT * FROM Article'),c.fetchall())

conn = sqlite3.connect(r'website\databases\email_subscriptions.db')
c = conn.cursor()

print(c.execute('SELECT * FROM Subscription'),c.fetchall())

conn = sqlite3.connect(r'website\databases\event_database.db')
c = conn.cursor()

print(c.execute('SELECT * FROM Event'),c.fetchall())

conn = sqlite3.connect(r'website\databases\volunteer_database.db')
c = conn.cursor()

print(c.execute('SELECT * FROM Volunteer'),c.fetchall())