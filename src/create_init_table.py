# -*- coding: utf-8 -*-
import pandas as pd
from pandas.io import sql
import numpy as np
import sqlite3

from normalize_neologd import normalize_neologd

def normalize(str):
    return normalize_neologd(str)

def read_data(file):
    yomiuri_data = pd.read_json(file)
    yomiuri_data = yomiuri_data[yomiuri_data.HeadLine.map(lambda x: not isinstance(x, list))]

    yomiuri_data.HeadLine = yomiuri_data.HeadLine.map(lambda x: normalize(x))
    yomiuri_data.article = yomiuri_data.article.map(lambda x: normalize('\n'.join(x)))

    return yomiuri_data

if __name__ == '__main__':
    yomiuri_data = read_data('../data/articles.json')
    conn = sqlite3.connect('../data/sqlite.db')
    cur = conn.cursor()
    sql.to_sql(yomiuri_data, name='item', con=conn)
    conn.commit()
    conn.close()
