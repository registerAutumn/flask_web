#!/usr/bin/env python
# -*- encoding: utf-8

from . import app
from flask import render_template, request, Response, redirect
from flask import url_for, session

@app.errorhandler(404)
def page_not_found(e):
    return render_template("handle/404.html"), 404

@app.errorhandler(500)
def service_crash(e):
    return render_template("handle/500.html"), 500