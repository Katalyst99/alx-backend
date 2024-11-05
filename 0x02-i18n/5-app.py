#!/usr/bin/env python3
"""The module for mock logging in"""
from flask import Flask, render_template, request, g
from flask_babel import Babel


class Config:
    """The config class that has a LANGUAGES class attribute."""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


@app.route('/')
def helloWorld() -> str:
    """Simply outputs “Welcome to Holberton” as page title """
    return render_template('5-index.html')


@babel.localeselector
def get_locale() -> str:
    """Function that gets locale from request."""
    suppLocale = request.args.get('locale')
    if suppLocale in app.config['LANGUAGES']:
        return suppLocale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


def get_user():
    """Function that returns a user dictionary or None"""
    userId = request.args.get('login_as')
    if not userId:
        return None
    return users.get(int(userId))


@app.before_request
def before_request():
    """Should use get_user to find a user if any"""
    g.user = get_user()


if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000)
