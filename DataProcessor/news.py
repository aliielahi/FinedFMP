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

dataset_path = '../dataset/'
historic_data_path = '../dataset/Historical Price/'
financials_data_path = '../dataset/Financial Quarterly Reports/'
news_data_path = '../dataset/News Articles/'
news_wsj_path = '../dataset/News Articles/WSJ-Header/'
news_nyt_path = '../dataset/News Articles/NYT/110/'
news_alphav_path = '../dataset/News Articles/Alpha-V/without text 104/'
news_CMINUS_path = '../dataset/News Articles/CMIN-US/'
dotcsv = '.csv'

def historic_news_wsj(ticker, qdate, time_frame = '3m'):
    data = pd.read_csv(news_wsj_path+ticker+dotcsv)
    data = data.rename(columns={'Title': 'headline', 'Abstract': 'abstract', 'PubDate': 'pub_date'})    
    data['pub_date'] = pd.to_datetime(data['pub_date'])

    data.sort_values(by='pub_date')
    end_date = datetime.strptime(qdate, '%Y-%m-%d')
    if time_frame[-1] == 'm':
        start_date = end_date + relativedelta(months=-1*int(time_frame[:-1]))
    if time_frame[-1] == 'd':
        start_date = end_date + relativedelta(days=-1*int(time_frame[:-1]))

    fil0 = data[data['pub_date'] <= pd.to_datetime(end_date)]
    fil0 = fil0[fil0['pub_date'] >= pd.to_datetime(start_date)]
    fil0['pub_date'] = pd.to_datetime(fil0['pub_date']).dt.date
    return fil0[['headline', 'abstract', 'pub_date']].to_dict(orient='records')

def historic_news_nyt(ticker, qdate, time_frame = '3m'):
    data = pd.read_csv(news_nyt_path+ticker+dotcsv)
    data['pub_date'] = [i[:10] for i in data['pub_date']]
    data['pub_date'] = pd.to_datetime(data['pub_date'])
    data.sort_values(by='pub_date')
    end_date = datetime.strptime(qdate, '%Y-%m-%d')
    
    if time_frame[-1] == 'm':
        start_date = end_date + relativedelta(months=-1*int(time_frame[:-1]))
    if time_frame[-1] == 'd':
        start_date = end_date + relativedelta(days=-1*int(time_frame[:-1]))

    fil0 = data[data['pub_date'] <= pd.to_datetime(end_date)]
    fil0 = fil0[fil0['pub_date'] >= pd.to_datetime(start_date)]
    fil0 = fil0.rename(columns={'headline': 'headline', 'abstract': 'abstract', 'pub_date': 'pub_date'})
    fil0['pub_date'] = pd.to_datetime(fil0['pub_date']).dt.date
    return fil0[['headline', 'abstract', 'pub_date']].to_dict(orient='records')

def historic_news_cmin(ticker, qdate, time_frame = '3m'):
    data = pd.read_csv(news_CMINUS_path+ticker+dotcsv, sep='\t')
    data = data.rename(columns={'title': 'headline', 'summary': 'abstract', 'date': 'pub_date'})
    data['pub_date'] = pd.to_datetime(data['pub_date'])
    data.sort_values(by='pub_date')
    end_date = datetime.strptime(qdate, '%Y-%m-%d')
    
    if time_frame[-1] == 'm':
        start_date = end_date + relativedelta(months=-1*int(time_frame[:-1]))
    if time_frame[-1] == 'd':
        start_date = end_date + relativedelta(days=-1*int(time_frame[:-1]))

    fil0 = data[data['pub_date'] <= pd.to_datetime(end_date)]
    fil0 = fil0[fil0['pub_date'] >= pd.to_datetime(start_date)]
    fil0['pub_date'] = pd.to_datetime(fil0['pub_date']).dt.date
    return fil0[['headline', 'abstract', 'pub_date']].to_dict(orient='records')

def historic_news_alphav(ticker, qdate, time_frame = '3m', with_sentiment = False):
    data = pd.read_csv(news_alphav_path+ticker+dotcsv)
    data = data.rename(columns={'title': 'headline', 'summary': 'abstract', 'time_published': 'pub_date'})
    data['pub_date'] = pd.to_datetime(data['pub_date'])
    data.sort_values(by='pub_date')
    end_date = datetime.strptime(qdate, '%Y-%m-%d')
    if time_frame[-1] == 'm':
        start_date = end_date + relativedelta(months=-1*int(time_frame[:-1]))
    if time_frame[-1] == 'd':
        start_date = end_date + relativedelta(days=-1*int(time_frame[:-1]))

    fil0 = data[data['pub_date'] <= pd.to_datetime(end_date)]
    fil0 = fil0[fil0['pub_date'] >= pd.to_datetime(start_date)]
    fil0['pub_date'] = pd.to_datetime(fil0['pub_date']).dt.date
    if with_sentiment:
        return fil0[['headline', 'abstract', 'pub_date', 'relevance_score',
                    'ticker_sentiment_score', 'ticker_sentiment_label']].to_dict(orient='records')
    return fil0[['headline', 'abstract', 'pub_date']].to_dict(orient='records')