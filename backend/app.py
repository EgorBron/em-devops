from os import getenv
from http.server import HTTPServer, BaseHTTPRequestHandler

host = getenv("BACKEND_HOST", "localhost")
port = getenv("BACKEND_PORT", "8080")

class EMHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(b"Hello from Effective Mobile!")

server = HTTPServer((host, int(port)), EMHandler)
print(f"serviing on http://{host}:{port}")
server.serve_forever()
