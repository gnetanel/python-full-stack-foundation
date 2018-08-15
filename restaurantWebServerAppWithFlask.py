from flask import Flask, render_template
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
# import cgi
from urllib.parse import parse_qs

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
from database_setup import engine, Base

Base.metadata.bind = engine
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

    return render_template("menu.html", restaurant=restaurant, items=menuItems)
    # return output


# Task 1: Create route for newMenuItem function here

@app.route('/restaurant/<int:restaurant_id>/new')
def newMenuItem(restaurant_id):
    output = ""
    output += "<form method='post' action=''>" \
              "<br>Name:" \
              " <input type='text' name='name'>" \
              "<br>Description:" \
              " <input type='text' name='description'>" \
              "<br>Price:" \
              " <input type='text' name='price'>" \
              "<br>Course:" \
              " <input type='text' name='course'>" \
              "<br>" \
              " <input type='submit' value='Submit'>" \
              "</form>"
    return output


# Task 2: Create route for editMenuItem function here
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit')
def editMenuItem(restaurant_id, menu_id):
    output = ""
    output += "<form method='post' action=''>" \
              "<br>Name:" \
              " <input type='text' name='name'>" \
              "<br>Description:" \
              " <input type='text' name='description'>" \
              "<br>Price:" \
              " <input type='text' name='price'>" \
              "<br>Course:" \
              " <input type='text' name='course'>" \
              "<br>" \
              " <input type='submit' value='Submit'>" \
              "</form>"
    return output


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete')
def deleteMenuItem(restaurant_id, menu_id):
    return "page to delete a menu item. Task 3 complete!"


if __name__ == "__main__":
    app.debug = True
    app.run(host='localhost', port=5000)
