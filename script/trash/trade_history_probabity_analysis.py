import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from dateutil import parser

from common_tools import *

def date_difference(d1, d2):
    date1 = parser.parse(str(d1))
    date2 = parser.parse(str(d2))
    return date2 - date1
def how_many_year(d1, d2):
    difference = date_difference(d1, d2)
    if difference.days < 0:
        print("[Warning] date1={} > date2={}".format(d1, d2))
        return 0
    elif difference.days > 365:
        print("[Warning] date1={} < date2={} more than 1 year".format(d1, d2))
    return difference.days / 365.

def earning_performance(input_csv, output_csv):
    commision = 0.026
    yield_1_year = 0.02
    short_rate = 0.03

    df = load_single_df(input_csv, header=0, colums=['call_or_short', 'position_ratio', 'date1', 'price1', 'date2', 'price2'], time_axis='None')
    call = df['call_or_short']
    position_ratio = df['position_ratio']
    date1 = df['date1']
    price1 = df['price1']
    date2 = df['date2']
    price2 = df['price2']

    profit_loss_in_the_position = []
    profit_loss_in_all_position = []
    profit_loss_total = []

    for c, r, d1, p1, d2, p2 in zip(call, position_ratio, date1, price1, date2, price2):
        t = how_many_year(d1, d2)
        if c:
            b = (p2 - commision) / p1 - pow(1 + yield_1_year, t)
        else:
            b = (p1 - commision) / p2 - pow(1 + yield_1_year + short_rate, t)
        profit_loss_in_the_position.append(b)
        profit_loss_in_all_position.append(b * r)
        if len(profit_loss_total):
            profit_loss_total.append((1 + b) * profit_loss_total[-1] * r + (1 - r) * profit_loss_total[-1])
        else:
            profit_loss_total.append((1 + b) * r + 1 - r)
    df['profit_loss_in_the_position'] = profit_loss_in_the_position
    df['profit_loss_in_all_position'] = profit_loss_in_all_position
    df['profit_loss_total'] = profit_loss_total
    df.to_csv(output_csv, index=False)

    max_profit = df['profit_loss_in_the_position'].max()
    max_loss = df['profit_loss_in_the_position'].min()
    average_profit = df[df['profit_loss_in_the_position'] > 0]['profit_loss_in_the_position'].mean()
    average_loss = df[df['profit_loss_in_the_position'] < 0]['profit_loss_in_the_position'].mean()
    success_percentage = len(df[df['profit_loss_in_the_position'] > 0]) / len(df)
    total_trades = len(df)
    positive_num = len(df[df['profit_loss_in_the_position'] > 0])
    negative_num = len(df[df['profit_loss_in_the_position'] < 0])
    stock_profit = (price1.iloc(0)[-1] - price1.iloc(0)[0]) / price1.iloc(0)[0]
    trade_period = date_difference(date2.iloc(0)[-1], date1.iloc(0)[0]).days

    print(f'单笔最大收益{max_profit:.2%}\n'
          f'单笔最大损失{max_loss:.2%}\n'
          f'单笔平均收益{average_profit:.2%}\n'
          f'单笔平均损失{average_loss:.2%}\n'
          f'收益/风险比{abs(average_profit/average_loss):.2%}\n'
          f'胜率{success_percentage:.2%}\n'
          f'总交{total_trades}\n'
          f'盈利次数{positive_num}\n'
          f'亏损次数{negative_num}\n'
          f'交易周期{trade_period}\n'
          f'最终收益{profit_loss_total[-1] - 1:.2%}\n'
          f'大盘收益{stock_profit:.2%}')

    # 绘制损益分布图
    plt.hist(df['profit_loss_in_the_position'], bins=10, color='skyblue', edgecolor='black')
    plt.title('Profit/Loss Distribution')
    plt.xlabel('Profit/Loss')
    plt.ylabel('Number of Trades')
    plt.show()

if __name__ == '__main__':
    earning_performance('/Users/turbo_air/Library/Mobile Documents/com~apple~CloudDocs/沈达云/Analyse/src/ros_ws/src/localization_app/script/ecomonic/trade_process.csv',
                        '/Users/turbo_air/Library/Mobile Documents/com~apple~CloudDocs/沈达云/Analyse/src/ros_ws/src/localization_app/script/ecomonic/trade_process_out.csv')