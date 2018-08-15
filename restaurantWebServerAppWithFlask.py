from flask import Flask
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

app = Flask(__name__)

# stopped at https://classroom.udacity.com/courses/ud088/lessons/3593308717/concepts/36245586140923


@app.route("/")
@app.route("/index")
def printall():
    session = DBSession()
    restaurant = session.query(Restaurant).first()
    menuItems = session.query(MenuItem).filter_by(restaurantId=restaurant.id)

    output = ""
    output += "<h1>Restaurant " + restaurant.name + "</h1>"
    output += "</br>Menu</br>"

    for menuItem in menuItems:
        output += menuItem.name + ", " + menuItem.course + ", " + menuItem.description + ", " + menuItem.price
        output += "</br>"
    return output

# Task 1: Create route for newMenuItem function here


def newMenuItem(restaurant_id):
    return "page to create a new menu item. Task 1 complete!"

# Task 2: Create route for editMenuItem function here


def editMenuItem(restaurant_id, menu_id):
    return "page to edit a menu item. Task 2 complete!"

# Task 3: Create a route for deleteMenuItem function here


def deleteMenuItem(restaurant_id, menu_id):
return "page to delete a menu item. Task 3 complete!"


if __name__ == "__main__":
    app.debug = True
    app.run(host ='localhost', port = 5000)

