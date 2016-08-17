#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals  # unicode by default
import os

from flask import Flask, send_file, send_from_directory
from flask.ext.cors import CORS
from flask.ext.restplus import apidoc

from extensions import db, sv
from views import api
from browser import ESicLivre


def create_app():
    # App
    app = Flask(__name__)
    app.config.from_pyfile('../settings/common.py', silent=False)
    app.config.from_pyfile('../settings/local_settings.py', silent=False)
    configure_logging(app)
    CORS(app, resources={r"*": {"origins": "*"}})

    # DB
    db.init_app(app)

    # Signer/Verifier
    sv.config(pub_key_path="settings/keypub")

    # Browser
    browser = ESicLivre()
    browser.config(
        firefox=app.config['FIREFOX_PATH'],
        email=app.config['ESIC_EMAIL'],
        senha=app.config['ESIC_PASSWORD'],
        pasta=app.config['DOWNLOADS_PATH'],
        logger=app.logger,
        app=app,
        )
    app.browser = browser

    # API
    api.init_app(app)
    app.register_blueprint(apidoc.apidoc)
    api.browser = browser

    # TODO: colocar isso em um lugar descente...
    @app.route('/static/<path:path>')
    def send_templates(path):
        return send_from_directory('static/', path)

    @app.route('/captcha')
    def send_captcha():
        return send_file('static/captcha.jpg')

    return app


def configure_logging(app):
    """Configure file(info) and email(error) logging."""

    if app.debug or app.testing:
        # Skip debug and test mode. Just check standard output.
        return

    import logging
    import logging.handlers

    # Set info level on logger, which might be overwritten by handers.
    # Suppress DEBUG messages.
    app.logger.setLevel(logging.INFO)

    info_log = os.path.join(app.config['LOG_FOLDER'], 'info.log')
    info_file_handler = logging.handlers.RotatingFileHandler(
        info_log, maxBytes=100000, backupCount=10)
    info_file_handler.setLevel(logging.INFO)
    info_file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]')
    )
    app.logger.addHandler(info_file_handler)
