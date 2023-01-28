from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import simplejson
import base64
import face_recognition
from glob import glob

hostName = "0.0.0.0"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
    def do_POST(self):
        print("got post!!")
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        test_data = simplejson.loads(post_body)
        print("post_body(%s)" % (test_data))

        with open("imageToSave.jpg", "wb") as fh:
            fh.write(base64.urlsafe_b64decode(test_data['image']))

        in_register = False

        try:
            unknown_image = face_recognition.load_image_file("imageToSave.jpg")
            unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

            registered_images = glob("registered/*jpg")

            for image in registered_images:
                known_image = face_recognition.load_image_file(image)
                known_encoding = face_recognition.face_encodings(known_image)[0]

                if face_recognition.compare_faces([known_encoding], unknown_encoding)[0]:
                    in_register = True
                    break
            

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            if in_register:
                self.wfile.write(bytes("Registered","utf-8"))
            else:
                self.wfile.write(bytes("Not Registered","utf-8"))
        except:
            in_register=False
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            if in_register:
                self.wfile.write(bytes("Registered","utf-8"))
            else:
                self.wfile.write(bytes("Not Registered","utf-8"))


if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")