# Trading Symbol
# Exchange
# Instrument Type
# ISIN (International Securities Identification Number)
# Company Name/Description

import fetch
import pandas as pd

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
    # download_master('Kotak')
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
    return merged_df


def main():
    print(kotak_map())
    # kotak_map()

if __name__ == '__main__':
    main()