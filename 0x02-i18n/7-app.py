#!/usr/bin/env python3
"""The module for using appropriate time zone"""
from flask import Flask, render_template, request, g
from flask_babel import Babel
import pytz


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
    return render_template('7-index.html')


@babel.timezoneselector
def get_timezone() -> str:
    """Function that gets the time"""
    tz = request.args.get('timezone')
    if tz:
        try:
            return pytz.timezone(tz).zone
        except pytz.exceptions.UnknownTimeZoneError:
            return app.config['BABEL_DEFAULT_TIMEZONE']
    if g.user:
        try:
            tz = g.user.get('timezone')
            return pytz.timezone(tz).zone
        except pytz.exceptions.UnknownTimeZoneError:
            return app.config['BABEL_DEFAULT_TIMEZONE']

    return app.config['BABEL_DEFAULT_TIMEZONE']


@babel.localeselector
def get_locale() -> str:
    """Function that gets locale from request."""
    suppLocale = request.args.get('locale')
    if suppLocale in app.config['LANGUAGES']:
        return suppLocale
    if g.user:
        userLocale = g.user.get('locale')
        if userLocale and userLocale in app.config['LANGUAGES']:
            return userLocale
    headLocale = request.headers.get('locale', None)
    if headLocale:
        if headLocale in app.config['LANGUAGES']:
            return headLocale
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
