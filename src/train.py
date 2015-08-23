# -*- coding: utf-8 -*-

import collections
import sys
from datetime import datetime as dt
import sqlite3

import pandas as pd
from pandas.io import sql
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

def normalize(str):
    return normalize_neologd(str)

def read_data():
    yomiuri_data = pd.read_sql("SELECT * FROM item;", conn)
    yomiuri_data = yomiuri_data[yomiuri_data.HeadLine.map(lambda x: not isinstance(x, list))]
    yomiuri_data_random = yomiuri_data.iloc[np.random.permutation(len(yomiuri_data))]

    return yomiuri_data_random

def train(train_data):
    client.train(train_data.apply(
        lambda l: (l['Genre1'], Datum({u'article':l['article'], u'HeadLine':l['HeadLine']}))
        , axis=1).tolist())

if __name__ == '__main__':
    yomiuri_data = read_data()
    client.clear()
    train(yomiuri_data)
    
