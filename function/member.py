#!/usr/bin/env python
# -*- encoding: utf-8
from . import app
from lxml import etree
from flask import render_template, request, session
from flask import redirect, url_for
from hashlib import sha512
import requests
import database

@app.route("/member/", methods=['POST', 'GET'])
def member_index():
    if request.method == 'POST':
        try:
            username = request.form['user']
            password = request.form['pass']
            if database.doing_sql("select * from user_info where u_id=? limit 1", (username,)) == []:
                s = requests.session()
                payload = {
                    'uid': username,
                    'pwd': password
                }
                result = s.post('http://140.127.113.231/kuas/perchk.jsp', data=payload).content
                if 'f_index.html' in result:
                    tree = etree.HTML(s.get('http://140.127.113.231/kuas/f_head.jsp').content)
                    info = tree.xpath("//div//span")
                    session['uid'] = username
                    session['username'] = info[2].text
                    session['class'] = info[1].text
                    session['unchange'] = True
                    return redirect(url_for('member_security'))
                else:
                    message = u"帳號/密碼錯誤"
            else:
                password = sha512(password).hexdigest()
                user = database.doing_sql("select * from user_info where u_id=? and u_pass=? limit 1", (username, password, ))
                if user == []:
                    message = u"帳號/密碼錯誤"
                else:
                    user = user[0]
                    (uid, passwd, name, _class, club) = user
                    session['uid'] = uid
                    session['username'] = name
                    session['class'] = _class
                    return redirect(url_for("index_index"))
        except KeyError:
            message = u"登入資訊錯誤"
        return render_template('member/index.html', message=message, type='error')
    else:
        return render_template('member/index.html')

@app.route("/member/security", methods=['POST', 'GET'])
def member_security():
    if not ('unchange' in session and session['unchange']):
        return redirect(url_for('index_index'))
    if request.method == 'POST':
        new_password = request.form['pass']
        if new_password.strip() == "":
            return render_template('member/security.html', message=u"請輸入新密碼", type="error")
        database.doing_sql("insert into user_info values(?, ?, ?, ?, '')", (session['uid'], sha512(new_password).hexdigest(), session['username'], session['class'],))
        del session['unchange']
        return redirect(url_for("index_index"))
    else:
        return render_template('member/security.html')

@app.route("/member/logout")
def logout():
    if 'username' in session:
        del session['username']
    return redirect(url_for('index_index'))

@app.route("/member/history")
def history():
    return render_template('member/index.html', message=u"歷史紀錄", type='success')

@app.route("/member/illegal")
def illegal():
    return render_template('member/index.html', message=u"違規紀錄", type='error')

@app.route("/member/detail")
def detail():
    return render_template('member/index.html', message=u"登入成功", type='success')