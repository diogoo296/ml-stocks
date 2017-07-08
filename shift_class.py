#!/usr/bin/env python2.7
import sys
import numpy as np
import pandas as pd


data = pd.read_csv(sys.argv[1], dtype=np.float64)
data.Class = data.Class.shift(-1)
data[:-1].to_csv('VALE5.shifted.csv', index=False)
