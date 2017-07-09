#!/usr/bin/env python2.7
import csv
import sys
import numpy as np
import pandas as pd
from os import listdir, path
from sklearn import preprocessing
from sklearn.svm import SVC
# from sklearn.cluster import KMeans
# from sklearn.neighbors import KNeighborsClassifier
# from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.model_selection import cross_val_score, TimeSeriesSplit
from sklearn.pipeline import make_pipeline


INPUT = sys.argv[1]
OUTPUT = sys.argv[2]


class Stocks:
    def __init__(self, file_in):
        data = pd.read_csv(file_in, dtype=np.float64)
        self.X = data.ix[:, 1:]
        self.y = data.ix[:, 0]
        self.size = len(data)


def learn_stocks(stocks):
    clf = make_pipeline(
        # preprocessing.StandardScaler(),
        # preprocessing.MinMaxScaler(),
        preprocessing.MaxAbsScaler(),
        SVC(C=1, cache_size=2000)
        # KNeighborsClassifier()
        # RandomForestClassifier(n_estimators=100, n_jobs=-1)
        # KMeans(init='k-means++', n_clusters=2, n_init=25, max_iter=500)
    )
    tscv = TimeSeriesSplit(n_splits=5)
    scores = cross_val_score(clf, stocks.X, stocks.y, cv=tscv, verbose=2)
    print("Score: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
    return scores


def write_output(stock_name, scores, size, header):
    out = {
        'stock': stock_name, 'data_size': size,
        'scores_mean': round(scores.mean(), 3),
        'scores_std': round(scores.std() * 2, 3)
    }
    for i in range(len(scores)):
        out['score' + str(i)] = round(scores[i], 3)
    with open(OUTPUT, 'a') as f:
        w = csv.DictWriter(f, out.keys())
        if header:
            w.writeheader()
        w.writerow(out)

files = [f for f in listdir(INPUT) if path.isfile(path.join(INPUT, f))]
header = True
for f in files:
    stock_name = f.split('.')[0]
    print('%s: Starting SVN...' % (stock_name))
    stocks = Stocks(path.join(INPUT, f))
    scores = learn_stocks(stocks)
    print('Writing output...')
    write_output(stock_name, scores, stocks.size, header)
    header = False
