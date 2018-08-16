from flask import Flask, render_template, request, redirect, url_for, flash
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


# stopped at https://classroom.udacity.com/courses/ud088/createMenuItemlessons/3593308717/concepts/36245586140923


@app.route("/")
@app.route("/restaurants")
def restaurantsIndex():
    session = DBSession()
    restaurants = session.query(Restaurant)
    return render_template('restaurantsIndex.html', restaurants=restaurants)


# Task 1: Create route for newMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/')
def restaurants(restaurant_id):
    session = DBSession()
    print("Query restaurant db")
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).first()
    print("Query Menu db")
    items = session.query(MenuItem).filter_by(restaurantId=restaurant.id)
    return render_template("menu.html", restaurant=restaurant, items=items)


@app.route('/restaurant/<int:restaurant_id>/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    session = DBSession()
    if request.method == "GET":
        return render_template('newMenuItem.html', )
    if request.method == "POST":
        menuItem = MenuItem(name=request.form['name'], description=request.form['description'],
                            price=request.form['price'], course=request.form['course'], restaurantId=restaurant_id)
        session.add(menuItem)
        session.commit()
        flash("New menu item added")
        return redirect(url_for('restaurants', restaurant_id=restaurant_id))


# Task 2: Create route for editMenuItem function here
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    session = DBSession()
    if request.method == "GET":
        restaurant = session.query(Restaurant).filter_by(id=restaurant_id).first()
        menuItem = session.query(MenuItem).filter_by(id=menu_id).first()
        return render_template('editMenuItem.html', menuItem=menuItem, restaurant=restaurant)
    if request.method == "POST":
        menuItem = session.query(MenuItem).filter_by(id=menu_id).first()
        if request.form['name']:
            menuItem.name = request.form['name']
        if request.form['description']:
            menuItem.description = request.form['description']
        if request.form['course']:
            menuItem.course = request.form['course']
        if request.form['price']:
            menuItem.price = request.form['price']

        session.add(menuItem)
        session.commit()
        return redirect(url_for('restaurants', restaurant_id=restaurant_id))


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    session = DBSession()
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).first()
    menuItem = session.query(MenuItem).filter_by(id=menu_id).first()

    if request.method == "GET":
        return render_template('deleteMenuItem.html', restaurant=restaurant, menuItem=menuItem)
    if request.method == "POST":
        session.delete(menuItem)
        session.commit()
        flash("Menu item deleted")
        return redirect(url_for('restaurants', restaurant_id=restaurant_id))


if __name__ == "__main__":
    app.secret_key = "mysecretkey"
    app.debug = True
    app.run(host='localhost', port=5000)
