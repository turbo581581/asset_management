import matplotlib.pyplot as plt
import pandas_datareader.data as web
import pandas_datareader.wb as wb
import argparse
import sys
import os
import tushare as ts
import pandas as pd

def download_us_ecomonic(save_path, start, end):
    folder_1 = "1_balance_of_payment"
    folder_2 = "2_monetary_and_fiscal_policy"
    folder_3 = "3_economic_status"
    folder_4 = "4_market_status"
    if not os.path.exists(save_path):
        os.makedirs(os.path.join(save_path, folder_1))
        os.makedirs(os.path.join(save_path, folder_2))
        os.makedirs(os.path.join(save_path, folder_3))
        os.makedirs(os.path.join(save_path, folder_4))
    ## 1_balance_of_payment
    # current account
    current_account = web.DataReader('USAB6BLTT02STSAQ', 'fred', start, end)
    current_account.to_csv(os.path.join(save_path, folder_1, "current_account.csv"), header=['current_account'])
    # govement debt
    government_debt = web.DataReader('GFDEGDQ188S', 'fred', start, end)
    government_debt.to_csv(os.path.join(save_path, folder_1, "government_debt.csv"), header=['government_debt'])
    # private debt
    private_debt = web.DataReader('DDDM03USA156NWDB', 'fred', start, end)
    private_debt.to_csv(os.path.join(save_path, folder_1, "private_debt.csv"), header=['private_debt'])
    # capital_inflow
    capital_inflow = web.DataReader('NETFI', 'fred', start, end)
    capital_inflow.to_csv(os.path.join(save_path, folder_1, "capital_inflow.csv"), header=['capital_inflow'])

    ## 2_monetary_and_fiscal_policy
    # rate
    rate = web.DataReader('FEDFUNDS', 'fred', start, end)
    rate.to_csv(os.path.join(save_path, folder_2,"rate.csv"), header=['rate'])
    # m0
    m0 = web.DataReader('M1SL', 'fred', start, end)
    m0.to_csv(os.path.join(save_path, folder_2, "m1.csv"), header=['m1'])
    # government budget
    fed_surplus = web.DataReader('FYFSGDA188S', 'fred', start, end)
    fed_surplus.to_csv(os.path.join(save_path, folder_2, "fed_surplus.csv"), header=['fed_surplus'])
    # bonds
    bonds_10y = web.DataReader('DGS10', 'fred', start, end)
    bonds_10y.to_csv(os.path.join(save_path, folder_2, "bonds_10y.csv"), header=['bonds_10y'])
    bonds_1y = web.DataReader('DGS1', 'fred', start, end)
    bonds_1y.to_csv(os.path.join(save_path, folder_2, "bonds_1y.csv"), header=['bonds_1y'])

    ## 3_economic_status
    # gdp
    gdp = wb.download(indicator='NY.GDP.MKTP.CD', country='USA', start=start, end=end)
    gdp['gdp'] = gdp['NY.GDP.MKTP.CD'] / 1.e12
    gdp.to_csv(os.path.join(save_path, folder_3, "gdp.csv"))
    # gdp growth
    gdp_growth = wb.download(indicator='NY.GDP.MKTP.KD.ZG', country='USA', start=start, end=end)
    gdp_growth.to_csv(os.path.join(save_path, folder_3, "gdp_growth.csv"))
    # core inflation rate
    core_inflation_rate = web.DataReader('CORESTICKM159SFRBATL', 'fred', start, end)
    core_inflation_rate.to_csv(os.path.join(save_path, folder_3, "core_inflation_rate.csv"), header=['core_inflation_rate'])
    # unemployment_rate
    unemployment_rate = web.DataReader('UNRATE', 'fred', start, end)
    unemployment_rate.to_csv(os.path.join(save_path, folder_3, "unemployment_rate.csv"), header=['unemployment_rate'])

    # 4_market_status
    # stock
    sp500 = web.StooqDailyReader('^SPX', start, end).read()
    sp500.to_csv(os.path.join(save_path, folder_4, "sp500_full.csv"), header=['Open', 'High', 'Low', 'sp_500_Close', 'Volume'])
    # gold and silver
    xagusd_df = pd.read_csv("https://stooq.com/q/d/l/?s=xagusd&i=d")
    # xagusd_df['Date'] = pd.to_datetime(xagusd_df['Date'])
    xagusd_df.to_csv(os.path.join(save_path, folder_4, "xagusd.csv"), header=['Date', 'Open', 'High', 'Low', 'xagusd_Close'], index=False)
    xauusd_df = pd.read_csv("https://stooq.com/q/d/l/?s=xauusd&i=d")
    # xauusd_df['Date'] = pd.to_datetime(xauusd_df['Date'])
    xauusd_df.to_csv(os.path.join(save_path, folder_4, "xauusd.csv"), header=['Date', 'Open', 'High', 'Low', 'xauusd_Close'], index=False)
    # oil
    crude_oil_price = web.DataReader('DCOILWTICO', 'fred', start, end)
    crude_oil_price.to_csv(os.path.join(save_path, folder_4, "crude_oil_price.csv"), header=['crude_oil_price'])
    # exchange
    us_cn_exchange = web.DataReader('DEXCHUS', 'fred', start, end)
    us_cn_exchange.to_csv(os.path.join(save_path, folder_4, "us_cn_exchange.csv"), header=['us_cn_exchange'])


def download_cn_ecomonic(save_path, start, end):
    if not os.path.exists(save_path):
        os.makedirs(os.path.join(save_path, "1_debt"))
        os.makedirs(os.path.join(save_path, "2_monetary_and_fiscal_policy"))
        os.makedirs(os.path.join(save_path, "3_economic_status"))
        os.makedirs(os.path.join(save_path, "4_market_status"))
        os.makedirs(os.path.join(save_path, "5_balance_of_payment"))

    ## 1_debt
    # govement debt
    government_debt = web.DataReader('GGGDTACNA188N', 'fred', start, end)
    government_debt.to_csv(os.path.join(save_path, "1_debt", "government_debt.csv"), header=['government_debt'])
    # private debt
    private_debt = web.DataReader('DDDM03CNA156NWDB', 'fred', start, end)
    private_debt.to_csv(os.path.join(save_path, "1_debt", "private_debt.csv"), header=['private_debt'])
    # international debt
    international_debt = web.DataReader('DDDM07CNA156NWDB', 'fred', start, end)
    international_debt.to_csv(os.path.join(save_path, "1_debt", "international_debt.csv"), header=['international_debt'])

    ## 2_monetary_and_fiscal_policy
    # rate
    rate = web.DataReader('INTDSRCNM193N', 'fred', start, end)
    rate.to_csv(os.path.join(save_path, "2_monetary_and_fiscal_policy", "rate.csv"), header=['rate'])
    # m0
    m0 = web.DataReader('MYAGM0CNM189N', 'fred', start, end)
    m0.to_csv(os.path.join(save_path, "2_monetary_and_fiscal_policy", "m0.csv"), header=['m0'])
    # government budget
    fed_surplus = web.DataReader('CHNGGXCNLG01GDPPT', 'fred', start, end)
    fed_surplus.to_csv(os.path.join(save_path, "2_monetary_and_fiscal_policy", "fed_surplus.csv"), header=['fed_surplus'])

    ## 3_economic_status
    # gdp
    gdp = wb.download(indicator='NY.GDP.MKTP.CD', country='CHN', start=start, end=end)
    gdp['gdp'] = gdp['NY.GDP.MKTP.CD'] / 1.e12
    gdp.to_csv(os.path.join(save_path, '3_economic_status', "gdp.csv"))
    # gdp growth
    gdp_growth = wb.download(indicator='NY.GDP.MKTP.KD.ZG', country='CHN', start=start, end=end)
    gdp_growth.to_csv(os.path.join(save_path, '3_economic_status', "gdp_growth.csv"))
    # core inflation rate
    core_inflation_rate = web.DataReader('CPALTT01CNM659N', 'fred', start, end)
    core_inflation_rate.to_csv(os.path.join(save_path, '3_economic_status', "core_inflation_rate.csv"), header=['core_inflation_rate'])
    # unemployment_rate
    unemployment_rate = web.DataReader('SLUEM1524ZSCHN', 'fred', start, end)
    unemployment_rate.to_csv(os.path.join(save_path, '3_economic_status', "unemployment_rate.csv"), header=['unemployment_rate'])

    ## 4_market_status
    # stock
    SZ399001 = ts.get_hist_data('399001', start, end, ktype='W')
    SZ399001_filter = SZ399001['close']
    SZ399001_filter.to_csv(os.path.join(save_path, '4_market_status', "SZ399001.csv"), header=['sz399001'])

    # bonds
    # bonds_10y = web.DataReader('DGS10', 'fred', start, end)
    # bonds_10y.to_csv(os.path.join(save_path, '4_market_status', "bonds_10y.csv"), header=['bonds_10y'])
    # bonds_1y = web.DataReader('DGS1', 'fred', start, end)
    # bonds_1y.to_csv(os.path.join(save_path, '4_market_status', "bonds_1y.csv"), header=['bonds_1y'])
    # gold
    # todo
    # oil
    crude_oil_price = web.DataReader('DCOILWTICO', 'fred', start, end)
    crude_oil_price.to_csv(os.path.join(save_path, '4_market_status', "crude_oil_price.csv"), header=['crude_oil_price'])
    # exchange
    us_cn_exchange = web.DataReader('DEXCHUS', 'fred', start, end)
    us_cn_exchange.to_csv(os.path.join(save_path, '4_market_status', "us_cn_exchange.csv"), header=['us_cn_exchange'])

    ## 5_balance_of_payment
    # current account
    current_account = web.DataReader('CHNB6BLTT02STSAQ', 'fred', start, end)
    current_account.to_csv(os.path.join(save_path, '5_balance_of_payment', "current_account.csv"), header=['current_account'])


def download_gdp(save_path, start, end):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    # GDP
    countries = ['USA', 'CHN', 'JPN', 'DEU', 'IND', 'GBR', 'FRA', 'RUS', 'CAN', 'ITA']
    for country in countries:
        gdp_data = wb.download(indicator='NY.GDP.MKTP.CD', country=[country], start=start, end=end)
        gdp_data[country + '_GDP'] = gdp_data['NY.GDP.MKTP.CD'] / 1.e12
        gdp_data.to_csv(os.path.join(save_path, country + "_gdp.csv"))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--save_path', type=str)

    args = parser.parse_args(sys.argv[1::])

    # 设置起始和结束日期
    start = '1900-01-01' #1990-01-01
    end = '2026-12-31' #2023-12-31

    download_us_ecomonic(os.path.join(args.save_path, 'us'), start, end)
    # download_cn_ecomonic(os.path.join(args.save_path, 'cn'), start, end)

    plt.show()