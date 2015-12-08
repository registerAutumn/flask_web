#!/usr/bin/env python
# -*- encoding: utf-8

from . import app
from flask import render_template
from flask.ext.cors import cross_origin

@app.route("/")
def index_index():
    return render_template("index.html")