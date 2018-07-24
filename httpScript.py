from http.server import HTTPServer, BaseHTTPRequestHandler
import json, urllib
import stlScale
import stlTranslate


class MySimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        in_content_length = int(self.headers.__getitem__('Content-length'))
        in_data = self.rfile.read(in_content_length)
        decoded_in_data = str(urllib.parse.unquote_to_bytes(in_data))

        # stlScale.main(decoded_in_data)
        stlTranslate.main()

        body = bytes('{"Hello": "World"}', "utf-8")
        self.send_response(200)
        self.send_header('Access-Control-Allow-Credentials', 'true')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header("Content-type", "text/json")
        self.send_header("Content-length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

httpd = HTTPServer(('localhost', 8080), MySimpleHTTPRequestHandler)
httpd.serve_forever()