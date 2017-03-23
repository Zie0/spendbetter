#!/usr/bin/env python

import pandas as pd
import numpy as np
import datetime as dt

def load_csv(csvfile):
    # Read the csv
    data = pd.read_csv(csvfile, low_memory=False)
    return data

def clean_memo(df):
    df['Memo'] = df['Memo'].apply(lambda x: x.split(";")[1].strip() if str.isdigit(x.split(";")[1].strip()) else str(0))
    return df

def clean_date(df):
    df['Date'] = df['Date'].apply(lambda x: dt.datetime.strptime(x, "%m/%d/%Y"))
    return df

def clean_df(df):
    df=clean_memo(clean_date(df))
    return df

if __name__=="__main__":
    #output the number of rows
    print("Total rows: {0}".format(len(data)))

    #see available headers
    print(list(data))
