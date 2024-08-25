import os
import re
import pandas as pd
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
import datetime
from dateutil.relativedelta import relativedelta
from datetime import datetime
from datetime import datetime, timedelta

# dataset_path = '../../dataset/'
historic_data_path = '../dataset/Historical Price/'
# financials_data_path = '../../dataset/Financial Quarterly Reports/'
# news_data_path = '../../dataset/News Articles/'
# news_wsj_path = '../../dataset/News Articles/WSJ-Header'
# news_nyt_path = '../../dataset/News Articles/NYT/110'
# news_alphav_path = '../../dataset/News Articles/Alpha-V/without text 104'
# news_CMINUS_path = '../../dataset/News Articles/CMIN-US'
dotcsv = '.csv'

def calculate_future_dates(date_str):
    input_date = datetime.strptime(date_str, '%Y-%m-%d')
    date_1_months = input_date + relativedelta(months=1)
    date_3_months = input_date + relativedelta(months=3)
    date_6_months = input_date + relativedelta(months=6)
    return date_1_months.strftime('%Y-%m-%d'), date_3_months.strftime('%Y-%m-%d'), date_6_months.strftime('%Y-%m-%d')

def calculate_past_dates(date_str):
    input_date = datetime.strptime(date_str, '%Y-%m-%d')
    date_1_months = input_date + relativedelta(months=-1)
    date_3_months = input_date + relativedelta(months=-3)
    date_6_months = input_date + relativedelta(months=-6)
    return date_1_months.strftime('%Y-%m-%d'), date_3_months.strftime('%Y-%m-%d'), date_6_months.strftime('%Y-%m-%d')

def get_target(company_ticker, qdate, binn = False):
    try: 
        historical_data = pd.read_csv(historic_data_path+company_ticker+dotcsv)
        historical_data['Date'] = pd.to_datetime(historical_data['Date'])
    except:
        return -1
    
    mo1, mo3, mo6 = calculate_future_dates(qdate)
    fil0 = np.array(historical_data[historical_data['Date'] >= pd.to_datetime(qdate)]['Close'])[0]
    fil1d = np.array(historical_data[historical_data['Date'] >= pd.to_datetime(qdate)]['Close'])[1]
    fil10d = np.array(historical_data[historical_data['Date'] >= pd.to_datetime(qdate)]['Close'])[10]
    fil1 = np.array(historical_data[historical_data['Date'] >= pd.to_datetime(mo1)]['Close'])[0]
    fil3 = np.array(historical_data[historical_data['Date'] >= pd.to_datetime(mo3)]['Close'])[0]
    fil6 = np.array(historical_data[historical_data['Date'] >= pd.to_datetime(mo6)]['Close'])[0]
    
    change1d, change10d = fil1d / fil0 - 1,\
                        fil10d / fil0 - 1
    change1, change3, change6 = fil1 / fil0 - 1,\
                                fil3 / fil0 - 1,\
                                fil6 / fil0 - 1
    if binn:
        change1d, change10d, change1, change3, change6 = True if change1d > 0 else False,\
                True if change10d > 0 else False,\
                True if change1 > 0 else False,\
                True if change3 > 0 else False,\
                True if change6 > 0 else False
    return {'1d': change1d, '10d': change10d, '1m': change1, '3m': change3, '6m': change6}

def get_momentums(company_ticker, qdate, binn = False):
    historical_data = pd.read_csv(historic_data_path+company_ticker+dotcsv)
    historical_data['Date'] = pd.to_datetime(historical_data['Date'])
    
    mo1, mo3, mo6 = calculate_past_dates(qdate)
    
    fil0 = np.array(historical_data[historical_data['Date'] <= pd.to_datetime(qdate)]['Close'])[-1]
    fil1d = np.array(historical_data[historical_data['Date'] <= pd.to_datetime(qdate)]['Close'])[-2]
    fil10d = np.array(historical_data[historical_data['Date'] < pd.to_datetime(qdate)]['Close'])[-10]
    fil1 = np.array(historical_data[historical_data['Date'] <= pd.to_datetime(mo1)]['Close'])[-1]
    fil3 = np.array(historical_data[historical_data['Date'] <= pd.to_datetime(mo3)]['Close'])[-1]
    fil6 = np.array(historical_data[historical_data['Date'] <= pd.to_datetime(mo6)]['Close'])[-1]
    
    change1d, change10d = fil0 / fil1d - 1,\
                        fil0 / fil10d - 1
    change1, change3, change6 = fil0 / fil1 - 1,\
                                fil0 / fil3 - 1,\
                                fil0 / fil6 - 1
    if binn:
        change1d, change10d, change1, change3, change6 =  True if change1d > 0 else False,\
                True if change10d > 0 else False,\
                True if change1 > 0 else False,\
                True if change3 > 0 else False,\
                True if change6 > 0 else False
    return {'1d': change1d, '10d': change10d, '1m': change1, '3m': change3, '6m': change6}

def historic_moving_average_6m(company_ticker, qdate):
    moving_avgs = []
    historical_data = pd.read_csv(historic_data_path+company_ticker+dotcsv)
    historical_data['Date'] = pd.to_datetime(historical_data['Date'])
    end_date = datetime.strptime(qdate, '%Y-%m-%d')
    
    for i in range(6):
        start_date = end_date + relativedelta(months=-1)

        fil0 = historical_data[historical_data['Date'] <= pd.to_datetime(end_date)]
        fil0 = fil0[fil0['Date'] >= pd.to_datetime(start_date)]
        # print('from', start_date, 'to', end_date, 'datapoints: ', len(fil0), 'mean price:', np.mean(fil0['Close']))
        moving_avgs.append(np.nanmean(fil0['Close']))
        end_date = start_date
    return moving_avgs[::-1]


def historic_moving_std_6m(company_ticker, qdate):
    moving_avgs = []
    historical_data = pd.read_csv(historic_data_path+company_ticker+dotcsv)
    historical_data['Date'] = pd.to_datetime(historical_data['Date'])
    end_date = datetime.strptime(qdate, '%Y-%m-%d')
    
    for i in range(6):
        start_date = end_date + relativedelta(months=-1)

        fil0 = historical_data[historical_data['Date'] <= pd.to_datetime(end_date)]
        fil0 = fil0[fil0['Date'] >= pd.to_datetime(start_date)]
        
        # print('from', start_date, 'to', end_date, 'datapoints: ', len(fil0), 'mean price:', np.mean(fil0['Close']))
        moving_avgs.append(np.std(fil0['Close']))
        end_date = start_date
    return moving_avgs[::-1]

def historic_vol_moving_average_6m(company_ticker, qdate):
    moving_avgs = []
    historical_data = pd.read_csv(historic_data_path+company_ticker+dotcsv)
    historical_data['Date'] = pd.to_datetime(historical_data['Date'])
    end_date = datetime.strptime(qdate, '%Y-%m-%d')
    
    for i in range(6):
        start_date = end_date + relativedelta(months=-1)

        fil0 = historical_data[historical_data['Date'] <= pd.to_datetime(end_date)]
        fil0 = fil0[fil0['Date'] >= pd.to_datetime(start_date)]
        
        # print('from', start_date, 'to', end_date, 'datapoints: ', len(fil0), 'mean price:', np.mean(fil0['Close']))
        moving_avgs.append(np.nanmean(fil0['Volume']))
        end_date = start_date
    return moving_avgs[::-1]

def historic_6m(company_ticker, qdate):
    moving_avgs = []
    historical_data = pd.read_csv(historic_data_path+company_ticker+dotcsv)
    historical_data['Date'] = pd.to_datetime(historical_data['Date'])
    end_date = datetime.strptime(qdate, '%Y-%m-%d')
    
    start_date = end_date + relativedelta(months=-6)

    fil0 = historical_data[historical_data['Date'] <= pd.to_datetime(end_date)]
    fil0 = fil0[fil0['Date'] >= pd.to_datetime(start_date)]
    
    return list(fil0['Close'])