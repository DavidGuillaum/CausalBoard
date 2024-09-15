# most of the code from the book of Matheus Facure "Causal Inference in python

import pandas as pd

def reshape_df(df: pd.DataFrame, treated: str, treatment_year: int) -> pd.DataFrame:
    """Input df should be observations X times matrix and observations should be the indexes"""
    #inverse column and rows
    df = df.transpose()

    df.index = df.index.astype(int)

    y_tr = df[treated]
    y_co = df = df.drop(columns=treated)
    y_pre_tr = y_tr[y_tr.index < treatment_year].to_frame()
    y_pre_co = y_co[y_co.index < treatment_year]
    y_post_tr = y_tr[y_tr.index >= treatment_year].to_frame()
    y_post_co = y_co[y_co.index >= treatment_year]



    return y_pre_tr, y_pre_co, y_post_tr, y_post_co