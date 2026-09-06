import os
from http.server import HTTPServer, SimpleHTTPRequestHandler

def run():
    port = int(os.environ.get('PORT', 8080))
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f"Feri app running on http://0.0.0.0:{port}")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
