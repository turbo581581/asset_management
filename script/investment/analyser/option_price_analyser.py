from scipy.stats import norm
import math
import matplotlib.pyplot as plt
from scipy.stats import norm
import numpy as np
def black_scholes_option_price(S, K, T, r, sigma, option_type='call'):
    # S正股价格,K行权价格,T剩余到期时间（年）,r无风险利率,sigma 隐含波动率
    d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)

    if option_type == 'call':
        option_price = S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
    elif option_type == 'put':
        option_price = K * math.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    else:
        raise ValueError("Invalid option type. Use 'call' or 'put'.")

    return option_price

if __name__ == '__main__':

    # 输入参数
    S = 7  # 正股价格
    K = 7  # 行权价格
    T = 15./365  # 剩余到期时间（年）
    r = 0.052  # 无风险利率
    sigma = 0.72  # 隐含波动率

    # # 计算看涨期权价格
    # call_price = black_scholes_option_price(S, K, T, r, sigma, option_type='call')
    # print(f"看涨期权价格：{call_price:.2f}")
    #
    # # 计算看跌期权价格
    # put_price = black_scholes_option_price(S, K, T, r, sigma, option_type='put')
    # print(f"看跌期权价格：{put_price:.2f}")

    # # 创建时间范围（从1天到2年的范围）
    # T_values = np.linspace(1 / 365, 1, 365)  # 1天到2年，100个点
    #
    # # 计算对应的期权价格
    # call_prices = [black_scholes_option_price(S, K, T, r, sigma, 'call') for T in T_values]
    # put_prices = [black_scholes_option_price(S, K, T, r, sigma, 'put') for T in T_values]
    #
    # # 绘制图形
    # plt.figure(figsize=(10, 6))
    # plt.plot(T_values*365, call_prices, label='call', color='blue')
    # plt.plot(T_values*365, put_prices, label='put', color='red')
    # plt.xlabel('T days')
    # plt.ylabel('Cost')
    # plt.title('cost with t')
    # plt.legend()
    # plt.grid(True)
    # plt.show()

    # 创建波动率范围（从1%到200%）
    sigma_values = np.linspace(0.0, 1.0, 101)  # 1%到200%，100个点

    # 计算对应的期权价格
    call_prices = [black_scholes_option_price(S, K, T, r, sigma, 'call') for sigma in sigma_values]
    put_prices = [black_scholes_option_price(S, K, T, r, sigma, 'put') for sigma in sigma_values]

    # 绘制图形
    plt.figure(figsize=(10, 6))
    plt.plot(sigma_values * 100, call_prices, label='call', color='blue')
    plt.plot(sigma_values * 100, put_prices, label='put', color='red')
    plt.xlabel('σ (%)')
    plt.ylabel('Cost')
    plt.title('Cost with σ while T=15days')
    plt.legend()
    plt.grid(True)
    plt.show()