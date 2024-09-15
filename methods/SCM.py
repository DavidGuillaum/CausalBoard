# most of the code from the book of Matheus Facure "Causal Inference in python

import pandas as pd
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.utils.validation import (check_X_y, check_array, check_is_fitted)
import cvxpy as cp
from methods.prepare import reshape_df
import numpy as np

class SyntheticControl():
    def __init__(self,):
        pass
    def fit(self, y_pre_co, y_pre_tr):

       y_pre_co, y_pre_tr = check_X_y(y_pre_co, y_pre_tr)

       w = cp.Variable(y_pre_co.shape[1])

       objective = cp.Minimize(cp.sum_squares(y_pre_co@w - y_pre_tr))
       constraints = [cp.sum(w) == 1, w >= 0]

       problem = cp.Problem(objective, constraints)

       self.loss_ = problem.solve()
       self.w_ = w.value

       self.is_fitted_ = True
       return self
    
    def predict(self, y_co):

        check_is_fitted(self)
        y_co = check_array(y_co)
        return y_co @ self.w_
    
    
def analyse(df: pd.DataFrame, treated: str, treatment_year: int):

    y_pre_tr, y_pre_co, y_post_tr, y_post_co = reshape_df(df=df, treated=treated, treatment_year=treatment_year)

    model = SyntheticControl()
    model.fit(y_pre_co=y_pre_co, y_pre_tr=y_pre_tr.mean(axis=1))

    if model.w_ is None:
        print("Convex hull problem")
        return ("a", "b", "c", "d")
    df_weights = pd.DataFrame(zip(model.w_.round(3), y_pre_co.columns), columns=['weight', 'Coutries'])

    y0_tr_hat = y_post_co.dot(model.w_)

    att = y_post_tr.mean(axis=1) - y0_tr_hat

    df = df.transpose()
    df.index = df.index.astype(int)
    treated = df[treated]
    sc = pd.concat([y_pre_co.dot(model.w_), y0_tr_hat])
    result = pd.DataFrame({ "Treated" : treated, "Synthetic Control" : sc})
    return sc, result, att, df_weights