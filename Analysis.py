import matplotlib.pyplot
import numpy as np
import pandas as pd
from sklearn import linear_model
df = pd.read_csv('stock_data.csv', header=None).T
df.columns = df.iloc[0]
df = df.iloc[1:]

#predicting the differences
ys = df['GOOG'].diff()
clf.fit(df.iloc[1:150], ys[1:150])
ys_pred = clf.predict(df.iloc[150:])

clf.score(df.iloc[150:], ys[150:])