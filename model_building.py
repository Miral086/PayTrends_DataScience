# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 19:00:23 2023

@author: miral
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 12:08:44 2023

@author: miral
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("D:\ResumeThings\PayTrends_DataScience\EDA_data.csv")

# choose relevant columns
print(df.columns)

df_model = df[['Rating', 'Location', 'Size',  'Type of ownership',
       'Industry', 'Sector', 'Revenue', 'avg_salary',
        'excel', 'nosql', 
       'Job_simpler', 'seniority', 'desc_len']]

# get dummy data
df_dum = pd.get_dummies(df_model)

# train test split
from sklearn.model_selection import train_test_split

X = df_dum.drop('avg_salary', axis = 1)
y = df_dum['avg_salary']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.33, random_state = 42)
 
# multiple linear regression
import statsmodels.api as sm

X_sm = X = sm.add_constant(X)
model = sm.OLS(y,X_sm)
model.fit().summary()
   
from sklearn.linear_model import LinearRegression, Lasso
from sklearn.model_selection import cross_val_score


# Linear regression
lm = LinearRegression() 
lm.fit(X_train, y_train)

np.mean(cross_val_score(lm, X_train, y_train, scoring = 'neg_mean_absolute_error', cv=3))


# lasso regression

lm_l = Lasso(alpha = 0.12) 
lm_l.fit(X_train, y_train)

np.mean(cross_val_score(lm_l, X_train, y_train, scoring = 'neg_mean_absolute_error', cv = 3))

alpha = []
error = []

for i in range(1,100):
    alpha.append(i/100)
    lml = Lasso(alpha = i/100)
    error.append(np.mean(cross_val_score(lml, X_train, y_train, scoring = 'neg_mean_absolute_error', cv = 3)))
    
plt.plot(alpha,error)

err = tuple(zip(alpha,error))
df_err = pd.DataFrame(err, columns=['alpha','error'])
df_err[df_err.error == max(df_err.error)] 


# random forest
from sklearn.ensemble import RandomForestRegressor
rf = RandomForestRegressor()
np.mean(cross_val_score(rf, X_train, y_train, scoring = 'neg_mean_absolute_error', cv = 3))


# tune models GridSearchCV
from sklearn.model_selection import GridSearchCV
parameters = {'n_estimators':range(10,300,10), 'criterion':('squared_error', 'absolute_error'), 'max_features':(1.0,)}

gs = GridSearchCV(rf, parameters, scoring='neg_mean_absolute_error', cv = 3, error_score='raise')
try:
    gs.fit(X_train, y_train)
except Exception as e:
    print("An error occurred during the GridSearchCV process:")
    print(e)

gs.best_score_
gs.best_estimator_

# test ensembles

tpred_lm = lm.predict(X_test)
tpred_lml = lm_l.predict(X_test)
tpred_rf = gs.best_estimator_.predict(X_test)

from sklearn.metrics import mean_absolute_error

mean_absolute_error(y_test, tpred_lm)
mean_absolute_error(y_test, tpred_lml)
mean_absolute_error(y_test, tpred_rf)

mean_absolute_error(y_test, (tpred_lml+tpred_rf)/2)

import pickle
pickl = {'model': gs.best_estimator_}
pickle.dump(pickl, open('model_file' + ".p", "wb"))

file_name = "model_file.p"
with open(file_name, 'rb') as pickled:
    data = pickle.load(pickled)
    model = data['model']

model.predict(X_test.iloc[1,:].values.reshape(1,-1))

X_test.iloc[1,:].values

list(X_test.iloc[1,:])
