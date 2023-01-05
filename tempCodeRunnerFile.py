if results:
                self.wfile.write(bytes("Registered","utf-8"))
            else:
                self.wfile.write(bytes("Not Registered","utf-8"))