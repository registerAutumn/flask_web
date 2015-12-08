#!/usr/bin/env python
# -*- encoding: utf-8

from flask import Flask, render_template, request
from flask.ext.cors import cross_origin
from flask_socketio import SocketIO, emit
from PIL import Image, ImageDraw, ImageFont
import sqlite3
import random
import time
import os
import re

DB_NAME = "backend"
color = ["673AB7", "5E35B1", "512DA8", "4527A0", "311B92", "0097A7", "00838F", "006064", "8E24AA", "7B1FA2", "6A1B9A", "4A148C", "1E88E5", "1976D2", "1565C0", "0D47A1"]
app = Flask(__name__)

@app.route("/")
def index():
    result = doing_sql("select * from message order by time desc", ())
    r = []
    for msg in result:
        (nick, title, content, times) = msg
        temp = {
            "color": random.choice(color),
            "img": nick[:1].upper(),
            "nick": nick[1:],
            "title": title,
            "content": content.split("\n"),
            "times": times
        }
        r.append(temp)
    return render_template("index.html", result=r)

@app.route("/submit")
def submit():
    return render_template("submit.html")

@app.route("/leave_msg", methods=['POST'])
@cross_origin(supports_credentials=True)
def leave_message():
    nickname = request.form['nick']
    title    = request.form['title']
    content  = request.form['content']
    doing_sql("insert into message values(?, ?, ?, ?)", (nickname, title, content, current_time()))
    sock.emit("new_message", make_response(random.choice(color), nickname[:1].upper(), nickname[1:], title, content, current_time()), broadcast=True)
    return "true"

def make_response(color, img, nick, title, content, times):
    return render_template("card.html", color=color, img=img, nick=nick, title=title, content=content.split("\n"), times=times)

def current_time():
    return time.strftime("%Y-%m-%d %H:%M:%S")

def doing_sql(sql, args):
    database = sqlite3.connect("./%s" % DB_NAME)
    cursor = database.cursor()
    cursor.execute(sql, args)
    result = cursor.fetchall()
    if re.match(r"^select.+", sql.lower()) == None:
        database.commit()
    return result

if __name__ == '__main__':
    sock = SocketIO(app)
    sock.run(app, host="127.0.0.1", port=8888, debug=True)
