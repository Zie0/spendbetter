#!/usr/bin/env python

import pandas as pd
import numpy as np
import datetime as dt

class Statement:
    def __init__(self,csvfile,acct='c'):
        self.statement = load_csv(csvfile,acct)

    def load_csv(csvfile,acct='c'):
        # Read the csv
        data = pd.read_csv(csvfile,parse_dates=['Date'],index_col=0,low_memory=False)
        if acct == 'c':
            try:
                data = clean_credit_memo(data)
            except Exception as E:
                print("This file may not be a (credit) csv.", E)
        elif acct == 'd':
            try:
                data = clean_debit_memo(data)
            except Exception as E:
                print("This file may not be a (debit) csv.", E)
        else:
            print("Account Type parameter must be a string:\n\t'c' (credit)\n\t'd' (debit)\nIf ommitted default Account Type is (credit)")
        return data

    def clean_credit_memo(df):
        df['Memo'] = df['Memo'].apply(lambda x: x.split(";")[1].strip() if str.isdigit(x.split(";")[1].strip()) else str(0))
        return df

    def clean_debit_memo(df):
        df['Memo'] = df['Memo'].apply(lambda x: x.split(".")[2].strip())
        return df

    def get_month(self,mon):
        try:
            parsed = dt.datetime.strptime(mon, "%Y-%m").strftime("%Y-%m")
            return self.statement[parsed]
        except Exception as E:
            print("Could not parse date or month out of range: {0}\nPlease Enter a month in 'YYYY-mm' format".format(E))



if __name__=="__main__":
    #output the number of rows
    print("Total rows: {0}".format(len(data)))

    #see available headers
    print(list(data))
