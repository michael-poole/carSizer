from http.server import HTTPServer, BaseHTTPRequestHandler
import json, urllib
import stlScale, stlParams


def make_body_from_params(params):
    body = '{'
    for param in params:
        body_item = '"' + param.split(": ")[0] + '": "' + param.split(": ")[1] + '"';
        body = body + body_item + ', '

    body = body.rstrip(", ")
    body += '}'
    print(body)
    bytes_body = bytes(body, "utf-8")
    return bytes_body


class MySimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        in_content_length = int(self.headers.__getitem__('Content-length'))
        in_data = self.rfile.read(in_content_length)
        body = bytes('{"Success": "200"}', "utf-8")
        
        decoded_in_data = str(urllib.parse.unquote_to_bytes(in_data))
        type = decoded_in_data.split("type=")[1].split("&")[0]
        if type == "Params":
            myParams = stlParams.main(decoded_in_data)
            body = make_body_from_params(myParams)
            self.send_response(200)
        elif type == "Scale":
            stlScale.main(decoded_in_data)
            self.send_response(200)
        else:
            self.send_response(400)

        self.send_header('Access-Control-Allow-Credentials', 'true')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header("Content-type", "text/json")
        self.send_header("Content-length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

httpd = HTTPServer(('localhost', 8080), MySimpleHTTPRequestHandler)
httpd.serve_forever()