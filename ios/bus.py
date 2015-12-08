#!/usr/bin/env python
# -*-encoding: utf-8

from . import app
import collections
import unicodedata
import requests
import datetime
import execjs
import urllib
import json
import os

def init(session):
    with open("./ios/bus.js") as r:
        js_function = r.read()
    session.get('http://bus.kuas.edu.tw/')
    js = execjs.get("Node").compile(js_function + session.get('http://bus.kuas.edu.tw/API/Scripts/a1').content)
    return js

def login(session, username, password):
    js = init(session)
    data = {}
    data['account'] = username
    data['password'] = password
    data['n'] = js.call('loginEncryption', str(data['account']), str(data['password']))
    bus_status = json.loads(session.post('http://bus.kuas.edu.tw/API/Users/login', data=data).content)['success']
    return bus_status

def status():
    s = requests.session()
    js = init(s)
    data = {}
    data['account'] = "1102108132"
    data['password'] = "0000"
    data['n'] = js.call('loginEncryption', str(data['account']), str(data['password']))
    bus_status = json.loads(s.post('http://bus.kuas.edu.tw/API/Users/login', data=data).content)['success']
    return bus_status

def query(session, y, m, d, operation="全部"):
    data = {
        'data':'{"y": \'%s\',"m": \'%s\',"d": \'%s\'}' % (y, m, d),
        'operation': operation,
        'page':1,
        'start':0,
        'limit':90
    }
    res = session.post('http://bus.kuas.edu.tw/API/Frequencys/getAll', data=data)
    resource = json.loads(res.content)
    returnData = []
    if not resource['data']:
        return []

    for i in resource['data']:
        Data = {}
        Data['EndEnrollDateTime'] = getRealTime(i['EndEnrollDateTime'])
        Data['runDateTime'] = getRealTime(i['runDateTime'])
        Data['Time'] = Data['runDateTime'][-5:]
        Data['endStation'] = i['endStation']
        Data['busId'] = i['busId']
        Data['reserveCount'] = i['reserveCount']
        Data['limitCount'] = i['limitCount']
        Data['isReserve'] = i['isReserve']
        returnData.append(Data)

    return returnData

def booked(session):
    data = {
        "page":1,
        "start":0,
        "limit":15
    }
    result = json.loads(session.post("http://bus.kuas.edu.tw/API/Reserves/getOwn", data=data).content)
    return result['data']

def book(session, kid, action=None):
    with open("./ios/bus.js") as r:
        js = execjs.get("Node").compile(r.read())
    if not action:
        res = session.post('http://bus.kuas.edu.tw/API/Reserves/add', data="{busId:"+ kid +"}")
    else:
        kid['reserveId'] = int(kid['key'])
        res = session.post('http://bus.kuas.edu.tw/API/Reserves/remove?_dc='+str(js.call('getTime')), data=json.dumps(kid))

    resource = json.loads(res.content)

    return resource['message']


def getRealTime(timestamp):
    return datetime.datetime.fromtimestamp(int(timestamp)/10000000 - 62135596800).strftime("%Y-%m-%d %H:%M")
