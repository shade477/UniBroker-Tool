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
    df = pd.read_csv(path)
    return df

def angel_map():
    # download_master('Angel')
    raw_df = import_file('datasets/angel_one.csv')
    df = raw_df[['token', 'symbol', 'exch_seg', 'instrumenttype', 'name']]
    return df






def main():
    angel_map()

if __name__ == '__main__':
    main()