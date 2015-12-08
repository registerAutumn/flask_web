#!/usr/bin/env python
# -*-encoding: utf-8

from . import app
from flask import Flask, render_template, request

@app.route("/post/new", methods=['GET'])
def create_event():
    return render_template('post/index.html')