#!/usr/bin/env python2.7
import sys
import numpy as np
import pandas as pd
from sklearn import preprocessing, metrics
from sklearn.svm import SVC
# from sklearn.cluster import KMeans
# from sklearn.neighbors import KNeighborsClassifier
# from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn.pipeline import make_pipeline


class Stocks:
    def __init__(self):
        rawData = pd.read_csv(sys.argv[1], dtype=np.float64)
        self.data = rawData.ix[:, 0:-2]
        # self.data = preprocessing.MaxAbsScaler().fit_transform(
        #    rawData.ix[:, 0:-2])
        self.target = np.array(rawData[['Class']]).ravel()
        self.size = len(self.data)

stocks = Stocks()

# clf = svm.SVC()
# clf = AdaBoostClassifier()
# clf = RandomForestClassifier(n_estimators=100, n_jobs=-1)
clf = make_pipeline(
    preprocessing.StandardScaler(),
    SVC(C=1, cache_size=2000)
    # KNeighborsClassifier()
    # RandomForestClassifier(n_estimators=100, n_jobs=-1)
    # KMeans(init='k-means++', n_clusters=2, n_init=25, max_iter=500)
)

# clf.fit(X_train, y_train)
scores = cross_val_score(clf, stocks.data, stocks.target, cv=5)
predicted = cross_val_predict(clf, stocks.data, stocks.target, cv=5)
accuracy = metrics.accuracy_score(stocks.target, predicted)
report = metrics.classification_report(stocks.target, predicted)

print("Score: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
print("Acciracy: %.3f" % (accuracy))
print("Classification report for classifier %s:\n%s\n" % (clf, report))

# classifier.fit(
#     stocks.data[:stocks.size // 2], stocks.target[:stocks.size // 2]
# )
#
# expected = stocks.target[stocks.size // 2:]
# predicted = classifier.predict(stocks.data[stocks.size // 2:])
#
# print("Classification report for classifier %s:\n%s\n" % (
#     classifier, metrics.classification_report(expected, predicted)))
# print("Confusion matrix:\n%s" % metrics.confusion_matrix(expected, predicted))
# print(classifier.score(stocks.data[stocks.size // 2:], expected))
