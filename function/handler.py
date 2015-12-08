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

@app.before_request
def handle_request():
    core_part = ['member', 'post']
    url = request.path.split("/")
    if url[1] in core_part and len(url) > 2 and (not url[2] == ''):
        is_login = check_login()
        if not is_login:
            return redirect(url_for("member_index"))
        else:
            if not url[2] == 'security' and 'unchange' in session and session['unchange']:
                return redirect(url_for("member_security"))

def check_login():
    print session
    return 'username' in session