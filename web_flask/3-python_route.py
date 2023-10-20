#!/usr/bin/python3
# File: 3-python_route.py
# Author: Oluwatobiloba Light
"""This script starts a Flask web application"""


from flask import Flask
from markupsafe import escape


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
    """Display “C ” followed by the value of the text variable """
    text = text.replace("_", " ")
    return f"C {escape(text)}"


@app.route("/python/<path:text>", strict_slashes=False)
def python_text(text):
    """Display “Python ” followed by the value of the text variable """
    text = text.replace("_", " ")
    return f"Python {escape(text)}"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
