#!/usr/bin/env python3
"""The module for instantiating the Babel object in app"""
from flask import Flask, render_template
from flask_babel import Babel


class Config:
    """The config class that has a LANGUAGES class attribute."""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


@app.route('/')
def helloWorld() -> str:
    """Simply outputs “Welcome to Holberton” as page title """
    return render_template('1-index.html')


if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000)
