import mimetypes
from http.server import HTTPServer, BaseHTTPRequestHandler


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        code = 200

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
                code = 404
                title = '404 not found'
                content = '<h1>404 not found</h1>'
        elif self.path == '/':
            title = 'Home'
            content = '<h1>Home</h1><p>Welcome to my website!</p>'
        elif self.path == '/blogs':
            title = 'Blogs'
            blog_list = [f'<li><a href="{url}">{title}</a></li>' for title, url in [
                ('blog 1', '/blog/1'),
                ('blog 2', '/blog/2'),
                ('blog 3', '/blog/3'),
            ]]
            content = f'<h1>Blogs</h1><ul>{"".join(blog_list)}</ul>'
        elif self.path.startswith('/blog/'):
            blog_id = int(self.path.lstrip('/blog/'))
            title = f'Blog {blog_id}'
            content = f'<h1>Blog {blog_id}</h1><p>dummy blog content</p>'
        else:
            code = 404
            title = '404 Not Found'
            content = '<h1>404 Not Found</h1>'

        # rendering
        template = open('templates/index.html').read()
        nav = self.make_nav()
        page = template \
            .replace('{{title}}', title) \
            .replace('{{content}}', content) \
            .replace('{{nav}}', nav)

        self.send_response(code)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(page.encode('utf-8'))

    def make_nav(self):
        items = [
            ('Home', '/'),
            ('Blogs', '/blogs'),
        ]
        return ''.join(
            f'<li class="{"active" if self.path == href else ""}"><a href="{href}">{text}</a></li>'
            for text, href in items
        )


if __name__ == '__main__':
    port = 8000
    server_address = ('', port)
    httpd = HTTPServer(server_address, RequestHandler)
    print(f'starting server on port {port}...')
    httpd.serve_forever()
