#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request
from . import app
import requests
import json

@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        class_table = getCourse(login(request.form['user'], request.form['pass']))
        result = []
        for i in class_table:
            c = {
                "daytime": i['daytime'],
                "d1": i['d1']['subjectChineseName'], 
                "d2": i['d2']['subjectChineseName'], 
                "d3": i['d3']['subjectChineseName'], 
                "d4": i['d4']['subjectChineseName'], 
                "d5": i['d5']['subjectChineseName'], 
                "d6": i['d6']['subjectChineseName'],
                "d7": i['d7']['subjectChineseName']
            }
            result.append(c)
        return render_template("class.html", result=result)
    else:
        return render_template("index.html")

def login(user, passwd):
    session = requests.session()
    session.post("http://140.127.113.108/Account/LogOn", data={"UserName": user, "Password": passwd})
    return session

def getCourse(s):
    return json.loads(s.get("http://140.127.113.108/Elective/SelectedCourse/GetStudentSchedule").text)['rows']