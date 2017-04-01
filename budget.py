#!/usr/bin/env python

import pandas as pd
import numpy as np
import datetime as dt
import memo_codes as mc

class Statement:
    def __init__(self,csvfile,acct='c'):
        self.statement = self.load_csv(csvfile,acct)
        self.slice = self.statement

    def reset_slice(self):
        self.slice = self.statement

    def load_csv(self,csvfile,acct='c'):
        # Read the csv
        data = pd.read_csv(csvfile,parse_dates=['Date'],index_col=0,low_memory=False)
        if acct == 'c':
            try:
                data = self.clean_credit_memo(data)
            except Exception as E:
                print("This file may not be a (credit) csv.", E)
        elif acct == 'd':
            try:
                data = self.clean_debit_memo(data)
            except Exception as E:
                print("This file may not be a (debit) csv.", E)
        else:
            print("Account Type parameter must be a string:\n\t'c' (credit)\n\t'd' (debit)\nIf ommitted default Account Type is (credit)")
        return data

    def clean_credit_memo(self,df):
        # This function cleans the excessive strings from the Memo field.
        # Once the memo code string is left it is converted to a category
        # using the credit memo codes in memo_codes module
        df['Memo'] = df['Memo'].apply(lambda x: mc.credit_mc[x.split(";")[1].strip()] if str.isdigit(x.split(";")[1].strip()) else mc.credit_mc[str(0)])
        return df

    def clean_debit_memo(self,df):
        df['Memo'] = df['Memo'].apply(lambda x: x.split(".")[2].strip())
        return df

    def get_month(self,mon):
        try:
            parsed = dt.datetime.strptime(mon, "%Y-%m").strftime("%Y-%m")
            self.slice = self.statement[parsed]
            return self.slice
        except Exception as E:
            print("Could not parse date or month out of range: {0}\nPlease Enter a month in 'YYYY-mm' format".format(E))

    def get_stats(self,mon=None):
        if mon is not None:
            df = self.get_month(mon)
            return df.groupby(['Memo'])['Amount'].agg([np.sum, np.mean, np.std])
        else:
            return self.slice.groupby(['Memo'])['Amount'].agg([np.sum, np.mean, np.std])

# Next up:
# finish get_stats
# add a method that shows the sum and sum without an array of spending categories that have the potential to be deducted.

if __name__=="__main__":
    #output the number of rows
    print("Total rows: {0}".format(len(data)))

    #see available headers
    print(list(data))
