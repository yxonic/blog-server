import sqlite3

# Connect to the SQLite database
connection = sqlite3.connect('blogs.db')

# Create a cursor object to interact with the database
cursor = connection.cursor()

# Create the blogs table
cursor.execute('''
CREATE TABLE IF NOT EXISTS blogs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL
)
''')

# Insert some fake data into the blogs table
fake_data = [
    ("The Joy of Python", "Python is a versatile language loved by many."),
    ("Understanding SQL", "SQL is essential for database management."),
    ("Web Development Basics", "Learn how the internet works."),
    ("Data Science Intro", "Data science is revolutionizing various industries."),
    ("The Art of Programming", "Programming is both a skill and an art form.")
]

cursor.executemany('''
INSERT INTO blogs (title, content)
VALUES (?, ?)
''', fake_data)

# Commit the changes to the database
connection.commit()

# Print the inserted data
cursor.execute('SELECT * FROM blogs')
rows = cursor.fetchall()

for row in rows:
    print(row)

# Close the connection
connection.close()
