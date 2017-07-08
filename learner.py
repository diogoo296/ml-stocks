#!/usr/bin/env python2.7
import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.svm import SVC
# from sklearn.cluster import KMeans
# from sklearn.neighbors import KNeighborsClassifier
# from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import TimeSeriesSplit
from sklearn.pipeline import make_pipeline
from os import listdir
import csv


class Stocks:
    def __init__(self, file_in):
        data = pd.read_csv(file_in, dtype=np.float64)
        self.X = data.ix[:, 1:]
        self.y = data.ix[:, 0]
        self.size = len(data)


def learn_stocks(stocks):
    # Fit and calculate score
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
    with open('results_noidc.csv', 'a') as f:
        w = csv.DictWriter(f, out.keys())
        if header:
            w.writeheader()
        w.writerow(out)

files = [f for f in listdir('stocks-class') if f.endswith('.less.csv')]
header = True
for f in files:
    stock_name = f.split('.')[0]
    print('%s: Starting SVN...' % (stock_name))
    stocks = Stocks('stocks-class/' + f)
    scores = learn_stocks(stocks)
    print('Writing output...')
    write_output(stock_name, scores, stocks.size, header)
    header = False

# scores = []
# accuracies = []
# for train_idx, test_idx in tscv.split(stocks.data):
#     X_train = stocks.data.iloc[train_idx]
#     X_test = stocks.data.iloc[test_idx]
#     y_train = stocks.target.iloc[train_idx]
#     y_test = stocks.target.iloc[test_idx]
#     clf.fit(X_train, y_train)
#     predicted = clf.predict(X_test)
#     scores.append(clf.score(X_test, y_test))
#     report = metrics.classification_report(y_test, predicted)
#     accuracies.append(metrics.accuracy_score(y_test, predicted))
# scores = pd.DataFrame(scores)

# predicted = cross_val_predict(clf, stocks.data, stocks.target, cv=tscv)
# accuracy = metrics.accuracy_score(stocks.target, predicted)
# report = metrics.classification_report(stocks.target, predicted)

# print("Accuracy: %.3f" % (accuracy))
# print("Classification report for clf %s:\n%s\n" % (clf, report))

# clf.fit(
#     stocks.data[:stocks.size // 2], stocks.target[:stocks.size // 2]
# )

# expected = stocks.target[stocks.size // 2:]
# predicted = clf.predict(stocks.data[stocks.size // 2:])

# print("Classification report for clf %s:\n%s\n" % (
#     clf, metrics.classification_report(expected, predicted)))
# print("Confusion matrix:\n%s" % metrics.confusion_matrix(expected, predicted))
# print(clf.score(stocks.data[stocks.size // 2:], expected))
