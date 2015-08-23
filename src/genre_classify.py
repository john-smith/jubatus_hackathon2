# -*- coding: utf-8 -*-

import collections
import sys
from datetime import datetime as dt
import sqlite3

import pandas as pd
import numpy as np
import jubatus
from jubatus.common import Datum

from normalize_neologd import normalize_neologd


host = '127.0.0.1'
port = 9199
name = 'yomiuri'

client = jubatus.Classifier(host, port, name)

conn = sqlite3.connect('../data/sqlite.db')
cur = conn.cursor()

def predict_min(l):
    res = client.classify([Datum({u'article':l['article'], u'HeadLine':l['HeadLine']})])
    pred = min(res[0], key = lambda x: x.score)
    return pred.label, pred.score


def main_contents():
    print u'これはとっても素敵なシステムです'
    print u'あなたを退屈な日常から解き放ち、新たなる境地へと導いてくれます'

    yomiuri_data = pd.read_sql("SELECT * FROM item ORDER BY DateLine DESC LIMIT 10;", conn)
    
    print u'----------------------------------------------------------'
    print u'早速気になるニュースを選んでみよう\n'

    data = yomiuri_data

    for i in range(5):
        print data['HeadLine']
        print '> ',
        selected = int(sys.stdin.readline())

        print u'----------------------------------------------------------'
        print data.ix[selected, 'HeadLine'], '\n\n'
        print data.ix[selected, 'article'], '\n\n'

        print u'----------------------------------------------------------'
        print u'この記事に関連なさそうなもの', '\n'

        no_related_genre = predict_min(yomiuri_data.ix[selected, :])[0]
        print no_related_genre

        data = pd.read_sql(u"SELECT * FROM item WHERE Genre1 = '{}' ORDER BY DateLine DESC LIMIT 10;".format(no_related_genre), conn)

    print u'\n\n＿人人人人人人＿'
    print u'＞　仕事しろ　＜'
    print u'￣Y^Y^Y^Y^Y^Y^￣\n\n'

if __name__ == '__main__':
    main_contents()
    conn.close()
    
