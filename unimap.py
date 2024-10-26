# Trading Symbol
# Exchange
# Instrument Type
# ISIN (International Securities Identification Number)
# Company Name/Description

import fetch
import pandas as pd
import re


## Fetch the data
def download_datasets():
    fetch.fetch_all()

def download_master(broker):
    fetch.fetch(broker)

def import_file(path):
    chunks = pd.read_csv(path, chunksize=10000, delimiter=',', on_bad_lines='skip')
    df = pd.concat(chunks, ignore_index=True)  # Combine chunks into a single DataFrame
    return df

def angel_map():
    # download_master('Angel')
    raw_df = import_file('datasets/angel_one.csv')
    df = raw_df[['token', 'symbol', 'exch_seg', 'instrumenttype', 'name']]
    return df

def zerodha_map():
    # download_master('Zerodha')
    raw_df = import_file('datasets/zerodha_master_scrip.csv')
    df = raw_df[['instrument_token', 'exchange_token', 'exchange', 'instrument_type', 'name']]
    return df

def load_dirs(path, files):
    dfs = []
    for file in files:
        raw_df = import_file(f'{path}/{file}.csv')
        dfs.append(raw_df)
    return dfs

def kotak_map():
    download_master('Kotak')
    path = 'datasets/Kotak'
    raw_dfs = load_dirs(path, ['cash', 'futures'])
    headers = ['instrumentToken','instrumentName','name',
               'lastPrice','expiry','strike',
               'tickSize','lotSize','instrumentType',
               'segment','exchange','isin',
               'multiplier','exchangeToken','OptionType'
    ]
    for raw_df in raw_dfs:
        raw_df.columns = headers
    
    merged_df = pd.concat(raw_dfs, axis=0, ignore_index=True)
    selected_df = merged_df[['instrumentToken', 'instrumentName', 'exchange', 'instrumentType', 'name', 'isin']]
    return selected_df

def fyer_map():
    # download_master('Fyers')
    path = 'datasets/Fyers'
    raw_dfs = load_dirs(path, ['NSE_CD', 'NSE_FO', 'NSE_CM', 'BSE_CM', 'BSE_FO', 'MCX_COM'])
    merged_df = pd.concat(raw_dfs, axis=0, ignore_index=True)
    selected_df = merged_df[['fytoken', 'underlying_symbol', 'symbol_ticker', 'isin', 'symbol_details']]
    selected_df['exchange'] = selected_df['symbol_ticker'].apply(get_exchange)
    selected_df['instrumenttype'] = selected_df['symbol_ticker'].apply(get_instrumenttype)
    selected_df.drop(columns=['symbol_ticker'], inplace=True)
    return selected_df

def get_exchange(symbol_ticker):
    return symbol_ticker.split(':')[0]

def get_instrumenttype(symbol_ticker):
    match = re.search(r'([A-Z]+)$', symbol_ticker)
    return match.group(1) if match else None

def icici_map():
    # download_master('ICICI')
    path = 'datasets/icici'
    raw_dfs = load_dirs(path, ['BSEScripMaster', 'CDNSEScripMaster', 'FOBSEScripMaster', 'FONSEScripMaster', 'NSEScripMaster'])
    # raw_dfs[0][['exchange']] = raw_dfs[2][['exchange']] = 'BSE'
    
    raw_dfs[0] = raw_dfs[0].assign(exchange='BSE')
    raw_dfs[2] = raw_dfs[2].assign(exchange='BSE')
    
    # raw_dfs[1][['ISINCode']] = raw_dfs[2][['ISINCode']] = raw_dfs[3][['ISINCode']] = ''
    # raw_dfs[1][['exchange']] = raw_dfs[3][['exchange']] = raw_dfs[4][['exchange']] = 'NSE'

    # Set ISINCode to an empty string where needed
    for i in [1, 2, 3]:
        raw_dfs[i] = raw_dfs[i].assign(ISINCode='')

    # Assign NSE exchange values
    for i in [1, 3, 4]:
        raw_dfs[i] = raw_dfs[i].assign(exchange='NSE')

    
    # selected_dfs = []
    # selected_dfs.append(raw_dfs[0][['Token', 'ExchangeCode', 'exchange', 'Series', 'CompanyName', 'ISINCode']])
    # selected_dfs.append(raw_dfs[1][['Token', 'ExchangeCode', 'exchange', 'OptionType', 'InstrumentName', 'ISINCode']])
    # selected_dfs.append(raw_dfs[2][['Token', 'ExchangeCode', 'exchange', 'OptionType', 'CompanyName', 'ISINCode']])
    # selected_dfs.append(raw_dfs[3][['Token', 'ExchangeCode', 'exchange', 'OptionType', 'CompanyName', 'ISINCode']])
    # selected_dfs.append(raw_dfs[4][['Token', 'ExchangeCode', 'exchange', 'Series', 'CompanyName', 'ISINCode']])

    raw_dfs[4].columns = raw_dfs[4].columns.str.lstrip().str.strip('"')

    selected_dfs = [
        raw_dfs[0][['Token', 'ExchangeCode', 'exchange', 'Series', 'CompanyName', 'ISINCode']],
        raw_dfs[1][['Token', 'ExchangeCode', 'exchange', 'OptionType', 'InstrumentName', 'ISINCode']],
        raw_dfs[2][['Token', 'ExchangeCode', 'exchange', 'OptionType', 'CompanyName', 'ISINCode']],
        raw_dfs[3][['Token', 'ExchangeCode', 'exchange', 'OptionType', 'CompanyName', 'ISINCode']],
        raw_dfs[4][['Token', 'ShortName', 'exchange', 'Series', 'CompanyName', 'ISINCode']]
    ]
    
    # To diagnose not matching headers
    # columns = ['Token', 'ShortName', 'exchange', 'Series', 'CompanyName', 'ISINCode']
    # for name in raw_dfs[3].columns:
    #     if name not in columns:
    #         print(name)

    merge_df = pd.concat(selected_dfs, axis=0, ignore_index=True)
    return merge_df

