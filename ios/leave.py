#!/usr/bin/env python
# -*-encoding: utf-8

from lxml import etree
import requests
import json

LEAVE_URL        = "https://leave.kuas.edu.tw:446/"
SUBMIT_LEAVE_URL = "https://leave.kuas.edu.tw:446/CK001MainM.aspx"

def status():
    leave_status = False
    session = requests.session()
    response = etree.HTML(session.get(LEAVE_URL).text)
    data = {}
    for i in response.xpath("//input"):
        if 'name' in i.attrib:
            data[i.attrib['name']] = i.attrib['value'] if 'value' in i.attrib else ''
    data['Login1$UserName'] = '1102108132'
    data['Login1$Password'] = '0000'
    try:
        leave_status = "學生個人假單查詢" in session.post(LEAVE_URL, data=data).content
    except:
        pass
    return leave_status


def login(session, username, password):
    response = etree.HTML(session.get(LEAVE_URL).text)
    data = {}
    for i in response.xpath("//input"):
        if 'name' in i.attrib:
            data[i.attrib['name']] = i.attrib['value'] if 'value' in i.attrib else ''
    data['Login1$UserName'] = username
    data['Login1$Password'] = password
    try:
        leave_status = "學生個人假單查詢" in session.post(LEAVE_URL, data=data).content
    except:
        pass
    return leave_status

def getList(session, year="104", semester="2"):
    root = etree.HTML(session.get("https://leave.kuas.edu.tw:446/AK002MainM.aspx").text)
    
    form = {}
    for i in root.xpath("//input"):
        form[i.attrib["name"]] = i.attrib["value"] if "value" in i.attrib else ""

    del form['ctl00$ButtonLogOut']

    form['ctl00$ContentPlaceHolder1$SYS001$DropDownListYms'] = "%s-%s" % (year, semester)
    
    print form

    r = session.post("https://leave.kuas.edu.tw:446/AK002MainM.aspx", data=form)
    
    if "查無%s學年度第%s學期的缺曠請假資料" % (year, semester) in r.content:
        return []

    result = []
    root = etree.HTML(r.text)
    table = root.xpath("//table[@class='mGridDetail']")[0]
    trs = table.xpath(".//tr")
    c = ["A", "1", "2", "3", "4", "B", "5", "6", "7", "8", "C", "11", "12", "13", "14"]
    for tr in trs[1:]:
        passby = {u"事": 0, u"公": 0, u"喪": 0, u"婚": 0, u"病": 0, u"生": 0}
        detail = {u"事": "", u"公": "", u"喪": "", u"婚": "", u"病": "", u"生": ""}
        td = tr.xpath(".//td")
        data = {}
        data['date'] = td[2].text
        data['remark'] = td[3].text
        for i, v in enumerate(td[4:]):
            types = v.text.strip()
            if types == "":
                continue
            passby[types] += 1
            detail[types] += c[i-1]
        data['passby'] = passby
        data['detail'] = detail
        result.append(data)
    return json.dumps(result)