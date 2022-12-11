from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import simplejson
import base64

hostName = "0.0.0.0"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/image':
            self.do_image()
        else:
            self.send_response(200)
            print("got post!!")
            content_len = int(self.headers.get('content-length', 0))
            post_body = self.rfile.read(content_len)
            test_data = simplejson.loads(post_body)
            print("post_body(%s)" % (test_data))

            with open("imageToSave.png", "wb") as fh:
                fh.write(base64.urlsafe_b64decode(test_data['image']))

            self.send_response(200)

    def do_GET(self):
        if self.path == '':
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("Hello","utf-8"))

        else:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("Hello", "utf-8"))




if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")