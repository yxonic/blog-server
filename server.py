from http.server import HTTPServer, BaseHTTPRequestHandler


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)

        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        data = f'''<html>
            <body>
                <p>Request path: <code>{self.path}</code></p>
                <p>Request headers: <pre>{self.headers}</pre></p>
            </body>
        </html>'''
        self.wfile.write(data.encode('utf-8'))


if __name__ == '__main__':
    port = 8000
    server_address = ('', port)
    httpd = HTTPServer(server_address, RequestHandler)
    print(f'starting server on port {port}...')
    httpd.serve_forever()
