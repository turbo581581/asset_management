import matplotlib.pyplot as plt
import pandas_datareader.data as web
import mplfinance as mpf
import datetime
import pandas as pd

def get_trade_info(trade_df, df):

    df['Signal'] = 0
    df['Call_or_short'] = 0

    for index, trade in trade_df.iterrows():
        date1 = trade['date1']
        price1 = trade['price1']
        date2 = trade['date2']
        price2 = trade['price2']
        call_or_short = trade['call_or_short']

        # 买入点标记为绿色三角形
        if call_or_short == 1:
            df.loc[datetime.datetime.strptime(str(int(date1)), '%Y%m%d').strftime('%Y-%m-%d'), 'Call_or_short'] = 1
            df.loc[datetime.datetime.strptime(str(int(date1)), '%Y%m%d').strftime('%Y-%m-%d'), 'Signal'] = price1
            df.loc[datetime.datetime.strptime(str(int(date2)), '%Y%m%d').strftime('%Y-%m-%d'), 'Call_or_short'] = 0
            df.loc[datetime.datetime.strptime(str(int(date2)), '%Y%m%d').strftime('%Y-%m-%d'), 'Signal'] = price2
        # 卖出点标记为红色三角形
        elif call_or_short == 0:
            df.loc[datetime.datetime.strptime(str(int(date1)), '%Y%m%d').strftime('%Y-%m-%d'), 'Call_or_short'] = 0
            df.loc[datetime.datetime.strptime(str(int(date1)), '%Y%m%d').strftime('%Y-%m-%d'), 'Signal'] = price1
            df.loc[datetime.datetime.strptime(str(int(date2)), '%Y%m%d').strftime('%Y-%m-%d'), 'Call_or_short'] = 1
            df.loc[datetime.datetime.strptime(str(int(date2)), '%Y%m%d').strftime('%Y-%m-%d'), 'Signal'] = price2
    return df

if __name__ == '__main__':
    trade_csv = '/Users/turbo_air/Library/Mobile Documents/com~apple~CloudDocs/沈达云/Analyse/src/ros_ws/src/localization_app/script/ecomonic/trade_process.csv'
    trade_df = pd.read_csv(trade_csv, sep='\t')
    start = (datetime.datetime.strptime(str(int(trade_df['date1'].min())), '%Y%m%d') - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
    end = (datetime.datetime.strptime(str(int(trade_df['date1'].max())), '%Y%m%d') + datetime.timedelta(days=30)).strftime('%Y-%m-%d')

    df = web.StooqDailyReader('SMCI', start, end).read()
    df = df[::-1]
    get_trade_info(trade_df, df)
    figsize = (15, 10)

    mpf.plot(df,
             type='candle',
             style='yahoo',
             addplot=[
                    mpf.make_addplot(df['Signal'], type='scatter', markersize=10, marker=['^' if sig == 1 else 'v' for sig in df['Call_or_short']],
                                     color=['g' if sig == 1 else 'r' for sig in df['Call_or_short']], secondary_y=False)],
             volume=True,
             title='Candlestick Chart with Buy/Sell Signals',
             figsize=figsize)
    mpf.show()