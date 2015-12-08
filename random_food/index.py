#-*- encoding: utf-8 -*-
from . import app, DB_NAME
from flask import render_template, request, url_for
from flask import redirect
from flask_cors import *
from hashlib import sha512
import requests
import sqlite3
import random
import json
import re

session = requests.session()

detail = {
    "資工".decode('utf-8', 'ignore') : "http://ppt.cc/fwVQ", "機械".decode('utf-8', 'ignore') : "http://ppt.cc/FPUJ",
    "觀光".decode('utf-8', 'ignore') : "http://ppt.cc/Zfu0", "應外".decode('utf-8', 'ignore') : "http://ppt.cc/EEyS",
    "會計".decode('utf-8', 'ignore') : "http://ppt.cc/pwN5", "電機".decode('utf-8', 'ignore') : "http://ppt.cc/lnVn7",
    "電子".decode('utf-8', 'ignore') : "http://ppt.cc/yz1O", "化材".decode('utf-8', 'ignore') : "http://ppt.cc/U~sO",
    "工管".decode('utf-8', 'ignore') : "http://ppt.cc/xU32", "土木".decode('utf-8', 'ignore') : "http://ppt.cc/au0C",
    "模具".decode('utf-8', 'ignore') : "http://ppt.cc/ZoO3", "國企".decode('utf-8', 'ignore') : "http://ppt.cc/MIV8",
    "財管".decode('utf-8', 'ignore') : "http://ppt.cc/FSXe", "會計".decode('utf-8', 'ignore') : "http://ppt.cc/pwN5",
    "金融".decode('utf-8', 'ignore') : "http://ppt.cc/E4EG", "企管".decode('utf-8', 'ignore') : "http://ppt.cc/qcIn",
    "資管".decode('utf-8', 'ignore') : "http://ppt.cc/DiUx", "人資".decode('utf-8', 'ignore') : "http://ppt.cc/3HqY"

}

@app.route("/class")
def _class():
    return render_template('class.html', data=detail)

@app.route("/")
def main():
    data = []
    result = do_sql("select f_name, f_address from food_map where f_check=1 order by random()", ())
    for record in result:
        (name, address) = record
        data.append({"name": name, "addr": address})
    return render_template('index.html', data=data)

@app.route("/list")
def lists():
    data = []
    result = do_sql("select f_name, f_address from food_map where f_check=1 order by random()", ())
    for record in result:
        (name, address) = record
        data.append({"name": name, "addr": address})
    return render_template("list.html", data=data)

@app.route("/getContent", methods=['POST'])
@cross_origin(supports_credentials=True)
def gc():
    if request.method == 'POST':
        key = sha512(request.form['name'])
        result = do_sql("select f_content from food_map where f_check=1 and f_id=? limit 1", (key))
        for record in result:
            (content) = record
            return content
    return redirect(url_for("main"))

@app.route("/comment")
def comment():
    return render_template('comment.html')

@app.route("/add", methods=['POST'])
@cross_origin(supports_credentials=True)
def add():
    if request.method == 'POST':
        name = request.form['name'].strip()
        addr = request.form['addr'].strip()
        tags = request.form['tags'].strip()
        content = request.form['content'].strip()
        key  = sha512(name).hexdigest()
        do_sql("insert into food_map values(?, ?, ?, ?, ?, 0)", (key, name, addr, content, tags))
        return redirect(url_for("comment"))

@app.route("/query")
@cross_origin(supports_credentials=True)
def query():
    i = conn.food.find()
    n = list(i)
    new_list = []
    for q in n:
        q['_id'] = str(q['_id'])
        if not 'check' in q:
            new_list.append(q)
    return json.dumps(new_list)

@app.route("/<int:user>/<int:password>")
def pass_in(user, password):
    #43690
    if user ^ password == 43690:
        data = []
        result = do_sql("select * from food_map where f_check=0", ())
        for record in result:
            (_id, name, address, content, tags, check) = record
            data.append({"_id": _id, "name": name, "addr": address, "content": content, "check": check})
        return render_template('check.html', data = data)
    else:
        return redirect(url_for("main"))

@app.route("/modify", methods=['POST'])
@cross_origin(supports_credentials=True)
def modify():
    if request.method == 'POST':
        _id = str(request.form['id'])
        do_sql("update food_map set f_check=1 where f_id=?", (_id, ))
        return "True"

@app.route("/del", methods=['POST'])
@cross_origin(supports_credentials=True)
def dels():
    if request.method == 'POST':
        _id = str(request.form['id'])
        do_sql("delete from food_map where f_id=?", (_id, ))
        return "True"

def do_sql(sql, args):
    database = sqlite3.connect(DB_NAME)
    cursor = database.cursor()
    cursor.execute(sql, args)
    result = cursor.fetchall()
    if re.match(r"^select.+", sql.lower()) == None:
        database.commit()
    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)
