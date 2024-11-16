import os
import re
import pandas as pd
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
import datetime
from collections import defaultdict
from dateutil.relativedelta import relativedelta
from datetime import datetime
from datetime import datetime, timedelta

dataset_path = '../dataset/'
historic_data_path = '../dataset/Historical Price/'
financials_data_path = '../dataset/Financial Quarterly Reports/'
news_data_path = '../dataset/News Articles/'
news_wsj_path = '../dataset/News Articles/WSJ-Header/'
news_nyt_path = '../dataset/News Articles/NYT/110/'
news_alphav_path = '../dataset/News Articles/Alpha-V/without text 104/'
news_CMINUS_path = '../dataset/News Articles/CMIN-US/'
dotcsv = '.csv'


def financials_nq(company_ticker, qdate, num_quarters = 4):
    moving_avgs = []
    data = pd.read_csv(financials_data_path+company_ticker+dotcsv)
    data['Date'] = pd.to_datetime(data['Date'])
    data = data.rename(columns={'price': 'averageMarketPrice'})
    end_date = datetime.strptime(qdate, '%Y-%m-%d')

    fil0 = data[data['Date'] <= pd.to_datetime(end_date)]
    
    fil0.sort_values(by='Date', ascending=True)
    important_features = ['Date', 'totalRevenue', 'costOfRevenue', 'netIncome',
     'totalAssets','averageMarketPrice', 'EPS', 'FCF', 'BookValueToMarketCapRatio',
     'AccrualsRatio', 'QuarterlyEPSGrowth', 'YearlyEPSGrowth', 'CFO2TA', 'CAPX2TA',
     'CurrentRatio', 'DebtToEquityRatio', 'QuickRatio', 'ReturnOnEquity',
     'OperatingMargin', 'PE_Ratio', 'QuickAssets']
    fil0 = fil0[important_features]
    fil0 = fil0.rename(columns = {'Date': 'date', 'totalRevenue': 'total revenue',
                                  'costOfRevenue': 'cost of revenue', 'netIncome': 'net income',
                                  'totalAssets': 'total assets', 'price': 'average market price',
                                  'EPS': 'earning per share', 'FCF': 'free cash flow',
                                  'BookValueToMarketCapRatio': 'book value to market cap',
                                  'AccrualsRatio': 'accruals', 'QuarterlyEPSGrowth': 'quarterly EPS growth',
                                  'YearlyEPSGrowth': 'yearly EPS growth', 'CFO2TA': 'cashflow to assets',
                                  'CAPX2TA': 'cap expenditure to assets','CurrentRatio': 'current ratio',
                                  'DebtToEquityRatio': 'debt To qquity', 'QuickRatio': 'quick ratio',
                                  'ReturnOnEquity': 'return on equity', 'OperatingMargin': 'operating margin',
                                  'PE_Ratio': 'price to earning', 'QuickAssets': 'quick assets'})
    
    fil0_dict = fil0.to_dict(orient='records')
    fil0_dict.sort(key=lambda x: x['date'])
    fil0_dict = fil0_dict[-1*num_quarters:]
    
    result = defaultdict(list)
    for d in fil0_dict:
        for key, value in d.items():
            result[key].append(value)
    result = dict(result)
    
    return result