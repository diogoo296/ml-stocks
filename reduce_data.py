#!/usr/bin/env python2.7
import sys
# import csv
import numpy as np
import pandas as pd
from os import listdir


THRESHOLD = float(sys.argv[1])

files = [f for f in listdir('stocks') if f.endswith('.saida.csv')]

for f in files:
    stock = f.split('.')[0]
    print('%s: reducing data...' % (stock))

    data = pd.read_csv('stocks/' + f, dtype=np.float64)

    data = data.dropna(axis=1, how='any')  # drop colums with null
    data = data.loc[:, (data != 0).any(axis=0)]  # drop columns with only zeros

    # Calculate correlation to 'close' and pick indicators above the threshold
    attrs = data.ix[:, 0:-5]
    corr = attrs.corr()['close'][:-1]
    high = {k: v for k, v in corr.iteritems() if abs(v) >= THRESHOLD}

    print('# Indicators: %d/%d' % (len(high.keys()), len(corr.keys())))
    print(pd.DataFrame.from_dict(high.items()))

    # Select high correlated indicators
    newData = {}
    for key in high.keys():
        newData[key] = data[key]
    newData.update(data.ix[:, -6:])

    # Shift next row class to previous row
    newData = pd.DataFrame(newData)
    newData.Class = newData.Class.shift(-1)

    outFile = 'stocks-class/' + stock + '.less.csv'
    newData[:-1].to_csv(outFile, index=False)

    # outFile = 'correlation-below/' + stock + '.corr.csv'
    # with open(outFile, 'wb') as f:
    #     w = csv.DictWriter(f, high.keys())
    #     w.writeheader()
    #     w.writerow(high)
