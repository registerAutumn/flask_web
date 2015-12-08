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
@app.route("/")
def index():
    return "Hello World"

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

@app.route("/leave_list", methods=['POST'])
def leave_list():
    user = session_pool[session['username']]
    try:
        sms = request.form['sms'].split("-")
    except KeyError:
        sms = time.strftime("%Y-%m").split("-")
        sms[0] = str(int(sms[0]) - 1911)
        sms[1] =  str(int(math.ceil(float(sms[1]) / 6.0)))
    print user['leave']
    print "leave.getList(%s, %s)" % ("user['leave']", ",".join(sms))
    result = eval("leave.getList(%s, %s)" % ("user['leave']", ",".join(sms)))
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
