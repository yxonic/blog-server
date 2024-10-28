import sqlite3


class BlogData:
    def __init__(self):
        self.connection = sqlite3.connect('blogs.db')
        self.cursor = self.connection.cursor()

    def get_blog_list(self):
        self.cursor.execute('SELECT id, title FROM blogs')
        return self.cursor.fetchall()

    def get_blog(self, blog_id):
        self.cursor.execute('SELECT title, content FROM blogs WHERE id = ?', (blog_id,))
        return self.cursor.fetchone()

    def update_blog(self, blog_id, title, content):
        self.cursor.execute('UPDATE blogs SET title = ?, content = ? WHERE id = ?', (title, content, blog_id))
        self.connection.commit()


if __name__ == '__main__':
    data = BlogData()
    print(data.get_blog_list())

    title, content = data.get_blog(3)
    print(title, content)

    data.update_blog(3, title, content + ' And make a website.')
    title, content = data.get_blog(3)
    print(title, content)
