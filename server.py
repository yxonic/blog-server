import mimetypes

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qsl

from data import BlogData

db = BlogData()
template = open('templates/index.html').read()


class RequestHandler(BaseHTTPRequestHandler):
    def make_nav(self, path):
        items = [
            ('Home', '/'),
            ('Blogs', '/blogs'),
        ]
        return ''.join(
            f'<li class="{"active" if path == href else ""}"><a href="{href}">{text}</a></li>'
            for text, href in items
        )

    def make_page(self, path, title, content):
        nav = self.make_nav(path)
        return template \
            .replace('{{title}}', title) \
            .replace('{{content}}', content) \
            .replace('{{nav}}', nav)

    def send_error(self, code, desc):
        self.send_response(code)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        page = self.make_page(self.path, f'{code} {desc}', f'<h1>{code} {desc}</h1>')
        self.wfile.write(page.encode('utf-8'))

    def do_GET(self):
        # routing
        if self.path.startswith('/public/'):
            try:
                f = open('.' + self.path, 'rb')
                self.send_response(200)
                content_type, _ = mimetypes.guess_type(self.path)
                self.send_header('Content-Type', content_type)
                self.end_headers()
                self.wfile.write(f.read())
                return
            except:
                self.send_error(404, 'Not Found')
        elif self.path == '/':
            title = 'Home'
            content = '<h1>Home</h1><p>Welcome to my website!</p>'
        elif self.path == '/blogs':
            title = 'Blogs'
            blog_list = [
                f'<li><a href="/blog/{blog_id}">{title}</a></li>'
                for blog_id, title in db.get_blog_list()
            ]
            content = f'<h1>Blogs</h1><ul>{"".join(blog_list)}</ul>'
        elif self.path.startswith('/blog/'):
            blog_id = self.path.lstrip('/blog/').rstrip('/edit')
            blog_id = int(blog_id)
            try:
                title, content = db.get_blog(blog_id)
            except:
                self.send_error(404, 'Not Found')
                return
            if self.path.endswith('/edit'):
                content = f'''<form action="#" method="post">
                    <div><input name="title" type="text" value="{title}"></div>
                    <div><textarea name="content" rows="20">{content}</textarea></div>
                    <div><button type="submit">Update</button></div>
                </form>'''
            else:
                content = f'<h1>{title}</h1><p>{content}</p><p><a href="/blog/{blog_id}/edit">edit</a></p>'
        else:
            self.send_error(404, 'Not Found')

        # rendering
        page = self.make_page(self.path, title, content)
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(page.encode('utf-8'))

    def do_POST(self):
        if self.path.startswith('/blog/'):
            content_type = self.headers['Content-Type']
            if not content_type.startswith('application/x-www-form-urlencoded'):
                self.send_error(403, 'Forbidden')
                return

            data = self.rfile.read(int(self.headers['Content-Length']))
            form = {k: v for k, v in parse_qsl(data.decode('utf-8'))}
            title = form['title']
            content = form['content']

            blog_id = self.path.lstrip('/blog/').rstrip('/edit')
            blog_id = int(blog_id)
            db.update_blog(blog_id, title, content)

            self.send_response(301)
            self.send_header('Location', f'/blog/{blog_id}')
            self.end_headers()

if __name__ == '__main__':
    port = 8000
    server_address = ('', port)
    httpd = HTTPServer(server_address, RequestHandler)
    print(f'starting server on port {port}...')
    httpd.serve_forever()
