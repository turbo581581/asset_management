import pandas as pd

# 读取数据
df = pd.read_csv("/home/turbo/PycharmProjects/asset_management/data/micro_economic/us/4_market_status/sp500_full.csv")

# 日期转为 datetime，并按时间升序排序（非常重要）
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")

# 计算收盘价日涨跌幅
df["sp500_ret"] = (df["sp_500_Close"].pct_change() * 100).round(2)
df.to_csv('/home/turbo/PycharmProjects/asset_management/data/micro_economic/us/4_market_status/sp500_full_1.csv', index=False)