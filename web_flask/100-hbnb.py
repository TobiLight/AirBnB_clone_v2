#!/usr/bin/python3
# File: 100-hbnb.py
# Author: Oluwatobiloba Light
"""This script starts a Flask web application"""


from flask import Flask, render_template
from markupsafe import escape
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.user import User


app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_hbnb():
    """Returns Hello HBNB!"""
    return "Hello HBNB!"


# @app.route("/hbnb", strict_slashes=False)
# def hbnb():
#     """Returns HBNB"""
#     return "HBNB"


@app.route("/c/<path:text>", strict_slashes=False)
def c_text(text):
    """
    Display “C ” followed by the value of the text variable.

        Args:
                text (str): _description_

        Returns:
                _type_: _description_
    """
    text = text.replace("_", " ")
    return f"C {escape(text)}"


@app.route("/python/", strict_slashes=False)
@app.route("/python/<path:text>", strict_slashes=False)
def python_text(text="is cool"):
    """
    Display “Python ” followed by the value of the text variable.

        Args:
                text (str, optional): _description_. Defaults to "is cool".

        Returns:
                _type_: _description_
    """
    text = text.replace("_", " ")
    return f"Python {escape(text)}"


@app.route("/number/<int:n>", strict_slashes=False)
def number(n):
    """
    Display “n is a number” only if n is an integer

    Args: n (int): A number

    Returns:
                _type_: _description_
    """
    return f"{n} is a number"


@app.route("/number_template/<int:n>", strict_slashes=False)
def number_template(n):
    """
    Renders a HTML template only if n is an integer

    Args: n (int): A number

    Returns:
                _type_: _description_
    """
    return render_template('5-number.html', n=n)


@app.route("/number_odd_or_even/<int:n>", strict_slashes=False)
def number_odd_or_even(n):
    """
    Renders a HTML template only if n is an integer and if n is odd or even

    Args: n (int): A number

    Returns:
                _type_: _description_
    """
    odd_or_even = "even" if n % 2 == 0 else "odd"
    return render_template('6-number_odd_or_even.html', n=n,
                           odd_or_even=odd_or_even)


@app.route("/states_list", strict_slashes=False)
def states_list():
    """Displays a HTML Page with list of all states"""
    states = [state.to_dict() for key, state in storage.all(State).items()]
    return render_template("7-states_list.html", states=states)


@app.route("/cities_by_states", strict_slashes=False)
def cities_by_states():
    """Displays a HTML Page with list of all cities of a state"""
    states = [state for key, state in storage.all(State).items()]
    return render_template("8-cities_by_states.html", states=states)


@app.route("/states", strict_slashes=False)
@app.route("/states/<id>", strict_slashes=False)
def state_by_id(id=None):
    """Displays a HTML Page with a state using ID"""
    has_id = True
    if id is None:
        states = [state for key, state in storage.all(State).items()]
        has_id = False
    else:
        has_id = True
        states = [state for key, state in storage.all(
            State).items() if state.to_dict()['id'] == id]
    return render_template("9-states.html", states=states, has_id=has_id)


@app.route("/hbnb_filters", strict_slashes=False)
def hbnb_filters():
    """Displays a HTML Page with states, cities and amenities"""
    states = [state for key, state in storage.all(State).items()]
    amenities = [amenity.to_dict()
                 for key, amenity in storage.all(Amenity).items()]
    return render_template("10-hbnb_filters.html",
                           states=states, amenities=amenities)


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """Displays a HTML Page with states, cities, amenities and place"""
    states = [state for key, state in storage.all(State).items()]
    amenities = [amenity.to_dict()
                 for key, amenity in storage.all(Amenity).items()]
    places = [place.to_dict() for key, place in storage.all(Place).items()]
    return render_template("100-hbnb.html",
                           states=states, amenities=amenities, places=places)


@app.teardown_appcontext
def teardown(error):
    """Closes a database connection"""
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
