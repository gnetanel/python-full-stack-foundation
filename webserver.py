from http.server import BaseHTTPRequestHandler, HTTPServer
import time
# import cgi
from urllib.parse import parse_qs


# hostName = "localhost"
# hostPort = 8000


class WebServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<form method='post' action='hello'><input type='text' name='message'><input type='submit' value='Submit'></form>"
                output += "</body></html>"

                self.wfile.write(bytes(output, "utf-8"))
                return
            else:
                self.send_error(404, 'File Not Found: %s' % self.path)
        except:
            print("Exception occur")

    def do_POST(self):
        # try:
        if self.path.endswith("/hello"):
            self.send_response(301)
            self.end_headers()
            # ctype, pdict = cgi.parse_header(self.headers.get('content-type'))

            length = int(self.headers.get('Content-length', 0))
            body = self.rfile.read(length).decode()
            params = parse_qs(body)
            messagecontent = params["message"][0]
            output = "<html><body>"
            output += "Your message is " + messagecontent
            # the form to fill info
            # output += "<form enctype='multipart/form-data'  method='post' action='hello'><input type='text' name='message'><input type='submit' value='Submit'></form>"
            output += "<form method='post' action='hello'><input type='text' name='message'><input type='submit' value='Submit'></form>"
            output += "</body></html>"
            self.wfile.write(bytes(output, "utf-8"))

def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        # print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        # print " ^C entered, stopping web server...."
        server.socket.close()


if __name__ == '__main__':
    main()

#
# class WebServerHandler(BaseHTTPRequestHandler):
#     def do_GET(self):
#         if self.path.endswith("/hello"):
#             self.send_response(200)
#             self.send_header('Content-type', 'text/html')
#             self.end_headers()
#             output = ""
#             output += "<html><body>Hello</body></html>"
#             print(output)
#             self.wfile.write(output)
#             return
#         else:
#             self.send_error(404, "File not found %s" % self.path)
#
#         # self.send_response(200)
#         # self.send_header("Content-type", "text/html")
#         # self.end_headers()
#         # self.wfile.write(bytes("<html><head><title>Title goes here.</title></head>", "utf-8"))
#         # self.wfile.write(bytes("<body><p>This is a test.</p>", "utf-8"))
#         # self.wfile.write(bytes("<p>You accessed path: %s</p>" % self.path, "utf-8"))
#         # self.wfile.write(bytes("</body></html>", "utf-8"))
#
#
# def main():
#     try:
#         port = 8080
#         server = HTTPServer(('', port), WebServerHandler)
#         print("Web Server running on port " + port.__str__())
#         server.serve_forever()
#     except KeyboardInterrupt:
#         print(" ^C entered, stopping web server....")
#         server.socket.close()
#
#
# if __name__ == '__main__':
#     main()
#
