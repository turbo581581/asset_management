import os
import argparse
import sys
import pandas_datareader.data as web
import numpy as np
import pandas as pd
import datetime
from tqdm import tqdm
import time

def download(stock_symbol, output_dir, delimieter):
    # start = '1900-01-01'  # 1990-01-01
    # end = '2023-12-31'  # 2023-12-31
    end = datetime.datetime.now().strftime('%Y-%m-%d')
    end_date = datetime.datetime.strptime(end, '%Y-%m-%d')
    start_date = end_date - datetime.timedelta(days=36500)
    start = start_date.strftime('%Y-%m-%d')

    df = web.StooqDailyReader(stock_symbol, start, end).read()
    time.sleep(0.3)
    if len(df) == 0:
        print('request failed in {}'.format(stock_symbol))
        return
    df.to_csv(os.path.join(output_dir, stock_symbol + '.csv'), sep=delimieter)

def stock_downloader(input_csv, output_dir, delimieter):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    df = pd.read_csv(input_csv, header=0, delimiter=delimieter)
    symbols = df['symbol']
    progress_bar = tqdm(total=len(symbols))
    for symbol in symbols:
        download(symbol, output_dir, delimieter)
        progress_bar.update(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_csv', type=str, required=True)
    parser.add_argument('--output_dir', type=str, required=True)
    parser.add_argument('--delimiter', type=str, default=',', required=False)
    args = parser.parse_args(sys.argv[1::])
    stock_downloader(args.input_csv, args.output_dir, args.delimiter)