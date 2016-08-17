#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals  # unicode by default

from flask.ext.sqlalchemy import SQLAlchemy

from viratoken import SignerVerifier
# from browser import ESicLivre


# print("Importing Extensions")
db = SQLAlchemy()
sv = SignerVerifier()
# browser = ESicLivre()
# print(db, sv)
