# -*- coding: utf-8 -*-

import lxml.html
import requests

target_url = 'http://www.yomiuri.co.jp/'
target_html = requests.get(target_url).text

root = lxml.html.fromstring(target_html)

for i in root.cssselect('.list-top li'):
    for j in i.cssselect('a'):
        print j.attrib['href']

for i in root.cssselect('.list-main-news li'):
    for j in i.cssselect('a'):
        print j.attrib['href']

