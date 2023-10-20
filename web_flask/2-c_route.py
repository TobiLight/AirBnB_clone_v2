#!/usr/bin/python3
# File: 2-c_route.py()
# Author: Oluwatobiloba Light
"""This script starts a Flask web application"""


from flask import Flask
app = Flask(__name__)
from markupsafe import escape


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


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
