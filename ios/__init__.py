#!/usr/bin/env python
# -*-encoding: utf-8

from flask import Flask, request, session
import requests
import math
import time
import json
import os

app = Flask(__name__)
path, folder, files = os.walk("./ios/").next()

for f in files:
    if f.startswith("__") or f.split(".")[-1] == 'pyc':
        continue
    try:
        package = f.split(".")[0]
        exec("from . import %s" % package)
    except ImportError:
        print "%s Import Error" % package
    except SyntaxError:
        pass

session_pool = {}
timeout      = 3600

allow_list = ["/", "/status", "/login"]

@app.before_request
def checkLogin():
    if not 'username' in session and not request.path in allow_list:
        return ""
    if 'username' in session:
        obj = session_pool[session['username']]
        if obj['timeout'] <= time.time() and obj['staus']:
            obj['timeout'] += timeout

@app.route("/")
def index():
    return "Hello"

@app.route("/status")
def getStatus():
    return json.dumps([ap.status(), bus.status(), leave.status()])

@app.route("/login", methods=['POST'])
def dologin():
    username = request.form['username']
    password = request.form['password']
    UUID     = request.form['UUID']
    if not username in session_pool:
        session_pool[username] = make_obj(username, password, UUID)
    obj = session_pool[username]
    if obj['timeout'] < time.time() or not obj['status']:
        a = ap.login(obj['ap'], username, password)
        b = bus.login(obj['bus'], username, password)
        l = leave.login(obj['leave'], username, password)
        obj['status'] = (a & b & l)
        obj['timeout'] = time.time() + timeout
    if obj['status']:
        session['username'] = username
    return json.dumps(session_pool[username]['status'])

@app.route("/isLogin", methods=['POST'])
def isLogin():
    try:
        return json.dumps(session_pool[session['username']]['status'])
    except:
        return json.dumps(False)

@app.route("/score", methods=['POST'])
def get_score():
    user = session_pool[session['username']]
    try:
        sms = request.form['sms']
    except:
        sms = "104,1"
    result = ap.score(user['ap'], sms)
    return result

@app.route("/class_room", methods=['POST'])
def get_class_room():
    user = session_pool[session['username']]
    return ap.classroom(user['ap'])

@app.route("/bus_list", methods=['POST'])
def bus_list():
    user = session_pool[session['username']]
    try:
        dates = request.form['date']
    except KeyError:
        dates = time.strftime("%Y-%m-%d")
    date = dates.split("-")
    result = eval("bus.query(%s, %s)" % ("user['bus']", ",".join(date)))
    return json.dumps(result)


def make_obj(user, word, uuid):
    obj = {
        "username": user,
        "password": word,
        "UUID"    : uuid,
        "ap"      : requests.session(),
        "bus"     : requests.session(),
        "leave"   : requests.session(),
        "timeout" : time.time() + timeout,
        "status"  : False,
        "cache"   : {
            "schedule": None,
            "reserved": None,
            "leave"   : None
        }
    }
    return obj
