# -*- coding: utf-8 -*-

import sqlite3
import sys

import lxml.html
import requests
import sqlite3

import jubatus
from jubatus.common import Datum

from normalize_neologd import normalize_neologd

# http://www.yomiuri.co.jp/sports/etc/20150823-OYT1T50040.html
# http://www.yomiuri.co.jp/national/20150822-OYT1T50191.html

host = '127.0.0.1'
port = 9199
name = 'yomiuri'

client = jubatus.Classifier(host, port, name)

conn = sqlite3.connect('../data/sqlite.db')
cur = conn.cursor()


while True:
    try:
        print '> ',
        target_url = sys.stdin.readline()
        target_html = requests.get(target_url).text

        root = lxml.html.fromstring(target_html)
        Genre1 = root.cssselect('li.nth-1')[0].text_content().strip()
        HeadLine = normalize_neologd(root.cssselect('.article article h1')[0].text_content())
        article = ''
        for i in root.cssselect('.article article p'):
            article += normalize_neologd(i.text_content())
            article += '\n'
        DateLine = root.cssselect('time')[0].text_content().replace(u'年', u'-').replace(u'月', u'-').replace(u'日', u'').replace(u'時', u':').replace(u'分', u':') + u'00'

        print u'Add Data'
        print Genre1
        print HeadLine
        print DateLine
        print article
        client.train([(Genre1, Datum({u'aricel':article, u'HeadLine':HeadLine}))])
        cur.execute(u"INSERT INTO item(Genre1, HeadLine, DateLine, article) VALUES('{0}', '{1}', '{2}', '{3}')".format(Genre1, HeadLine, DateLine, article))
        conn.commit()
    except requests.exceptions.MissingSchema:
        print 'error'

conn.close()
