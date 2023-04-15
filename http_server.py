import json
import os
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from database_manager import DatabaseManager


class HttpServer:
    def __init__(
        self,
        host="localhost",
        port=8080,
    ):
        self.http_server = ThreadingHTTPServer((host, port), HttpHandler)

    def start(self):
        threading.Thread(target=self.http_server.serve_forever).start()

    def shutdown(self):
        self.http_server.shutdown()


class HttpHandler(BaseHTTPRequestHandler):
    current_directory = os.path.dirname(__file__)
    TEMPLATE_FILE = "template-food-stock.html"
    TEMPLATE_PATH = os.path.join(current_directory, TEMPLATE_FILE)

    def do_GET(self):
        with open(self.TEMPLATE_PATH, mode="r", encoding="utf-8") as html:
            response_body = html.read()
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(response_body.encode("utf-8"))

    def do_POST(self):
        db = DatabaseManager()
        rows = db.select_all()
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        response_body = json.dumps(rows)
        self.wfile.write(response_body.encode("utf-8"))
        db.close()
