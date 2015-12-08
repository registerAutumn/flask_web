#!/usr/bin/env python
# -*- encoding: utf-8

from lxml import etree
import requests
import json

AP_LOGIN     = "http://140.127.113.227/kuas/perchk.jsp"
SCORE_URL    = "http://140.127.113.227/kuas/ag_pro/ag008.jsp?"
SCHEMA_LOGIN = "http://140.127.113.109/Account/LogOn?ReturnUrl="
SCHEMA_URL   = "http://140.127.113.109/Elective/SelectedCourse/GetStudentSchedule"

def status():
    response = requests.post(AP_LOGIN, data={'uid': 'guest', 'pwd': '123'})
    return 'f_index.html' in response.content and response.status_code == 200

def login(session, username, password):
    response = session.post(AP_LOGIN, data={'uid': username, 'pwd': password})
    score    = session.post(SCHEMA_LOGIN, data={"UserName": username, "Password": password})
    return 'f_index.html' in response.content and response.status_code == 200 and \
           '使用者姓名' in score.content and score.status_code == 200

def score(session, sms="104,1"):
    payload = {
        "yms": sms,
        "spath": "ag_pro/ag008.jsp?",
        "arg01": sms.split(",")[0],
        "arg02": sms.split(",")[1]
    }
    result = []
    resp = etree.HTML(session.post(SCORE_URL, data=payload).content)
    table = resp.xpath("//form//table")[0]
    trs = table.xpath(".//tr")
    for tr in trs[1:]:
        td = tr.xpath(".//td")
        data = {}
        data['subject']     = td[1].text.strip()
        data['credit']      = td[2].text.strip()
        data['mid_score']   = td[6].text.strip()
        data['final_score'] = td[7].text.strip()
        result.append(data)
    return json.dumps(result)

def classroom(session):
    return json.dumps(json.loads(session.post(SCHEMA_URL, data={"id1":"id1", "id2":"id2"}).content)['rows'])
