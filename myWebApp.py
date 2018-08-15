from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
from database_setup import engine, Base
from flask import Flask

Base.metadata.bind=engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

restaurnt1 = Restaurant(name="Pizza place3")
restaurnt2 = Restaurant(name="dummy restaurant3")


session.add(restaurnt1)
session.add(restaurnt2)
session.commit()

session = DBSession()
firstResult = session.query(Restaurant).filter_by(name="Pizza place3").first()
firstResult.name = "Pizza place_was_exxx"
session.add(firstResult)
session.commit()

session = DBSession()
myrestaurntItems = session.query(Restaurant).all()

for myrest in myrestaurntItems:
    print(myrest.name)

# items = session.query(Restaurant).all()
# for item in items:
#     print("about to delete " + item.name)
#     session.delete(item)


# session.commit()