from http.server import BaseHTTPRequestHandler, HTTPServer
import time
# import cgi
from urllib.parse import parse_qs

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
from database_setup import engine, Base

Base.metadata.bind=engine
DBSession = sessionmaker(bind=engine)


class WebServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        session = DBSession()
        if self.path.endswith("/restaurants/new"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            output = ""
            output += "<html><body>"
            output += "<h1>Create a New Restaurant</h1>"
            output += "</body></html>"
            output += "<form method='post' action=''><input type='text' name='restaurant_name'><input type='submit' value='Submit'></form>"
            output += "</body></html>"
            self.wfile.write(bytes(output, "utf-8"))

        if self.path.endswith("/delete"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            restaurantIdPath = self.path.split("/")[2]
            myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIdPath).first()

            output = ""
            output += "<html><body>"
            output += "<h1>Are you sure you want to delete " + myRestaurantQuery.name + "?</h1>"
            output += "</br>"
            output += "<form method='post' action=''><input type='submit' value='Delete'></form>"
            output += "</body></html>"
            self.wfile.write(bytes(output, "utf-8"))

        if self.path.endswith("/edit"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            restaurantIdPath = self.path.split("/")[2]
            myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIdPath).first()

            output = ""
            output += "<html><body>"
            output += "<h1>Update Restaurant" + myRestaurantQuery.name + "</h1>"
            output += "</body></html>"
            output += "<form method='post' action=''><input type='text' name='restaurant_name' placeholder='%s'><input type='submit' value='Rename'></form>" % myRestaurantQuery.name
            output += "</body></html>"
            output += "</body></html>"
            self.wfile.write(bytes(output, "utf-8"))

        if self.path.endswith("/restaurants"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            output = ""
            output += "<html><body>"
            output += "<a href='/restaurants/new'>Create a new restaurant</a>"

            restaurants = session.query(Restaurant).all()
            for restaurant in restaurants:
                output += "<h1>Restaurant</h1>"
                output += restaurant.name
                output += "</br>"
                #output += "<a href='/restaurants/%s/edit>Edit</a>" % restaurant.id
                output += "<a href='/restaurants/%s/edit'>Edit</a>" % restaurant.id
                output += "</br>"
                output += "<a href='/restaurants/%s/delete'>Delete</a>" % restaurant.id
                output += "</br>"
            output += "</body></html>"
            self.wfile.write(bytes(output, "utf-8"))

    def do_POST(self):
        session = DBSession()

        # try:
        if self.path.endswith("/restaurants/new"):
            # ctype, pdict = cgi.parse_header(self.headers.get('content-type'))

            length = int(self.headers.get('Content-length', 0))
            body = self.rfile.read(length).decode()
            params = parse_qs(body)
            messagecontent = params["restaurant_name"][0]

            restaurant = Restaurant(name=messagecontent)
            session.add(restaurant)
            session.commit()
            self.send_response(301)
            self.send_header('content-type', 'text/html')
            self.send_header('Location', '/restaurants')
            self.end_headers()

            # output = "<html><body>"
            # output += "Your message is " + messagecontent
            # # the form to fill info
            # # output += "<form enctype='multipart/form-data'  method='post' action='hello'><input type='text' name='message'><input type='submit' value='Submit'></form>"
            # output += "<form method='post' action='hello'><input type='text' name='message'><input type='submit' value='Submit'></form>"
            # output += "</body></html>"
            # self.wfile.write(bytes(output, "utf-8"))


        if self.path.endswith("/edit"):
            self.send_response(301)
            self.send_header('content-type', 'text/html')
            self.send_header('Location', '/restaurants')
            self.end_headers()

            restaurantIdPath = self.path.split("/")[2]
            myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIdPath).first()

            length = int(self.headers.get('Content-length', 0))
            body = self.rfile.read(length).decode()
            params = parse_qs(body)
            messagecontent = params["restaurant_name"][0]

            # Update in database
            myRestaurantQuery.name = messagecontent
            session.add(myRestaurantQuery)
            session.commit()

        if self.path.endswith("/delete"):
            self.send_response(301)
            self.send_header('content-type', 'text/html')
            self.send_header('Location', '/restaurants')
            self.end_headers()

            restaurantIdPath = self.path.split("/")[2]
            myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIdPath).first()

            # Delete entry from database
            session.delete(myRestaurantQuery)
            session.commit()

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

