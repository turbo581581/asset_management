import os
import glob
import pandas as pd
import argparse
import sys
import requests
from bs4 import BeautifulSoup
import re
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select

def clean_percentage(cell_value):
    try:
        result = cell_value.split('%')[-1]
        return result
    except:
        return cell_value

def clean_unit(cell_value):
    try:
        unit = 1.
        if cell_value.find('万亿') != -1:
            unit = 1.e12
        elif cell_value.find('亿') != -1:
            unit = 1.e8
        elif cell_value.find('万') != -1:
            unit = 1.e4
        result = unit * float(cell_value.replace(',', '').replace('亿', '').replace('万', '').replace('--', ''))
        return result
    except:
        if cell_value == '----':
            return 0
        else:
            return cell_value

def KPI(finance_name, country, df):
    df_float = df.applymap(clean_unit)

    #HK
    total_net_sales = '营业总收入'
    gross_profit = '毛利'
    net_income = '除税后溢利'
    total_assets = '总资产'
    total_liabilities = '总负债'
    total_current_assets = '流动资产合计'
    total_current_liabilities = '流动负债合计'
    inventory = '存货'
    accounts_receivable = '应收账款'
    if country == 'US':
        net_income = '除税后利润'
        total_current_liabilities = '流动负债总额'
        accounts_receivable = '应收款项'
    elif country == 'SZ':
        net_income = '净利润'
        total_assets = '资产总计'
        total_liabilities = '负债合计'
        accounts_receivable = '应收票据及应收账款'

    if finance_name == 'income-statement':
        if country == 'SZ':
            df_float.loc[gross_profit] = df_float.loc[total_net_sales] - df_float.loc['营业成本']
        df.loc['毛利率'] = df_float.loc[gross_profit] / df_float.loc[total_net_sales].replace(0, 1)
        df.loc['净利率'] = df_float.loc[net_income] / df_float.loc[total_net_sales].replace(0, 1)
    elif finance_name == 'balance-sheet':
        df.loc['资产负债率'] = df_float.loc[total_liabilities] / df_float.loc[total_assets].replace(0, 1)
        df.loc['波动比率'] = df_float.loc[total_current_assets] / df_float.loc[total_current_liabilities].replace(0, 1)
        try:
            df.loc['速动比率'] = (df_float.loc[total_current_assets] - df_float.loc[inventory] - df_float.loc[accounts_receivable]) / df_float.loc[total_current_liabilities].replace(0, 1)
        except:
            pass
    return df

def request_data(url, finance_name):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    # response = requests.get(url, headers=headers)
    # if response.status_code == 200:
    #     soup = BeautifulSoup(response.text, 'html.parser')
    #
    #     financial_table = soup.find('table')
    #     df = pd.read_html(str(financial_table))[0]
    #     return True, df
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')

        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)

        show_yoy_button = driver.find_element('xpath', "//div[@class='showyoy-select']")
        show_yoy_button.click()
        time.sleep(5)
        driver.implicitly_wait(2)

        # Find and click on the dropdown to expand options
        dropdown = driver.find_element('class name', "period-select")
        dropdown.click()

        # Find and click on the "年报、季报、三季报" option
        annual_option = driver.find_element('xpath', "//div[@class='pouper max-hgt']//div[@class='item'][contains(text(),'季报')]")
        annual_option.click()
        time.sleep(5)
        driver.implicitly_wait(2)  # 5 seconds, adjust as needed

        # Find the table element using its class or other identifier
        table_element = driver.find_element('class name', finance_name)

        # Use Pandas to read the HTML table into a DataFrame
        df = pd.read_html(table_element.get_attribute("outerHTML"))[0]
        df = df.applymap(clean_percentage)
        # Close the browser
        driver.quit()

        return True, df
    except:
        pass

    return False, 0

def get_company_finance_by_futu(symbol, country, output_dir):
    symbol_save_dir = os.path.join(output_dir, country, symbol)
    # if not os.path.exists(symbol_save_dir):
    #     os.makedirs(symbol_save_dir)
    #'income-statement', 'cash-flow', 'balance-sheet', 'key-indicators', 'business-data'
    finance_name_list = ['income-statement', 'cash-flow', 'balance-sheet']

    for finance_name in finance_name_list:
        url = f'https://www.futunn.com/stock/{symbol}-{country}/financial/{finance_name}'
        flag, df = request_data(url, finance_name)
        if flag:
            df = df.set_index(df.columns[0])
            df = KPI(finance_name, country, df)
            df.to_csv(finance_name + '.csv')

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--symbol', type=str, required=True, help='stock symbol')
    parser.add_argument('--country', type=str, required=True, choices=['HK', 'US', 'SZ'])
    parser.add_argument('--output_dir', type=str, required=True)
    parser.add_argument('--match_regex', type=str, default='.csv', required=False)
    parser.add_argument('--delimiter', type=str, default=',', required=False)
    args = parser.parse_args(sys.argv[1::])

    get_company_finance_by_futu(args.symbol, args.country, args.output_dir)
    # df = pd.read_csv('/media/nio/416dc79d-c0e3-4c92-b02e-7c369c44f1e4/nio/data/economic/company_finacial_data/HK/03333/balance-sheet.csv', header=0, index_col=0)
    # KPI('balance-sheet', df)