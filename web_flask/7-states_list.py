#!/usr/bin/python3
# File: 6-number_odd_or_even.py
# Author: Oluwatobiloba Light
"""This script starts a Flask web application"""


from flask import Flask, render_template
from markupsafe import escape
from models import storage
from models.state import State


app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_hbnb():
    """Returns Hello HBNB!"""
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """Returns HBNB"""
    return "HBNB"


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


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
