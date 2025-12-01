import numpy as np
import matplotlib.pyplot as plt

def long_profit_ratio(P0, P, T, a=0.05, c=0.026):
    P0 = P0 * pow(1 + a, T)
    profit_ratio = (P - P0 - c) / (P0 + c)
    return profit_ratio

def short_profit_ratio(P0, P, T, a=0.05, c=0.026, b = 0.03):
    bc = P0 * pow(1 + b, T) - P0
    profit_ratio = (P0 - P - c - bc) / (P0 + c)
    return profit_ratio

def call_profit_ratio(P, K, C, T, a=0.05, c=0.023):
    C = (C + c) * pow(1 + a, T)
    profit_ratio = (max(P - K, 0) - C) / C
    return profit_ratio

def put_profit_ratio(P, K, C, T, a=0.05, c=0.023):
    C = (C + c) * pow(1 + a, T)
    profit_ratio = (max(K - P, 0) - C) / C
    return profit_ratio

def short_call_profit_ratio(P, K, C, T, a=0.05, c=0.023):
    C = (C + c) * pow(1 + a, T)
    profit_ratio = -(max(P - K, 0) - C) / C
    return profit_ratio

def short_put_profit_ratio(P, K, C, T, a=0.05, c=0.023):
    C = (C + c) * pow(1 + a, T)
    profit_ratio = -(max(K - P, 0) - C) / C
    return profit_ratio
def bear_call_spreed_profit_ratio(P, C0, C1, K0, K1, T, a=0.05, c = 0.023):
    C = (C0 - C1 - 2*c) * pow(1 + a, T)
    profit_ratio = (C - max(P - K0, 0) + max(P - K1, 0)) / (C0 + C1 + 2*c)
    return profit_ratio
def plot_long_short_profit(P0, P, t, B, a, name):
    plt.xlabel('sale price')
    plt.ylabel('profit ratio(%)')
    plt.title(f'{name} intial_price={P0}')

    # for t in T:
    #     long_ratio = [long_profit_ratio(P0, p, t, a) for p in P]
    #     plt.plot(P, long_ratio, label=f'lone,T={t}', ls='-')
    for b in B:
        short_ratio = [short_profit_ratio(P0, p, t, a, c=0.026, b=b) for p in P]
        plt.plot(P, short_ratio, label=f'short,T={t:.2f},b={b}', ls='--')

def test_call_put_profit(P0, P, K, C_call, C_put, T, a, name):
    plt.xlabel('sale price')
    plt.ylabel('profit ratio(%)')
    plt.title(f'{name} intial_price={P0}')

    # stock_benefits = [stock_profit_ratio(P0, p, T[0], a) for p in P]
    # plt.plot(P, stock_benefits, label='stock', c='b')

    # for k, c, t in zip(K, C_call, T):
    #     option_benefits = [call_profit_ratio(p, k, c, t, a) for p in P]
    #     plt.plot(P, option_benefits, label=f'call_k={k},c={c}', ls = '-')
    #
    # for k, c, t in zip(K, C_put, T):
    #     option_benefits = [put_profit_ratio(p, k, c, t, a) for p in P]
    #     plt.plot(P, option_benefits, label=f'put_k={k},c={c}', ls='--')

    for k, c, t in zip(K, C_call, T):
        option_benefits = [short_call_profit_ratio(p, k, c, t, a) for p in P]
        plt.plot(P, option_benefits, label=f'short_call_k={k},c={c}', ls='-')

    # for k, c, t in zip(K, C_put, T):
    #     option_benefits = [short_put_profit_ratio(p, k, c, t, a) for p in P]
    #     plt.plot(P, option_benefits, label=f'short_call_k={k},c={c}', ls='-')



def test_bear_call_spreed_profit(P0, P, C0, C1, K0, K1, T, a, name):
    plt.xlabel('sale price')
    plt.ylabel('profit ratio(%)')
    plt.title(f'{name} intial_price={P0}')
    for c0, c1, k0, k1, t in zip(C0, C1, K0, K1, T):
        option_benefits = [bear_call_spreed_profit_ratio(p, c0, c1, k0, k1, t, a) for p in P]
        plt.plot(P, option_benefits, label=f'BCS_C0={c0},C1={c1},k0={k0},K1={k1}', ls='-')
    plt.legend()
    plt.grid()
    plt.show()

def investment_profit(i, w, l, wr, N):
    return pow(i*(1+w) + 1-i, N*wr)*pow(i*(1+l) + 1-i, N*(1-wr))

def plot_investment_profit():
    plt.xlabel('investment profit')
    plt.ylabel('profit ratio(%)')
    plt.title(f'investment')
    w = 4
    l = -1
    wr = 0.52
    N = np.arange(1, 40, 1)
    for i in [0.2, 0.25, 0.3, 0.33, 0.36]:
        option_benefits = [investment_profit(i, w, l, wr, n) for n in N]
        plt.plot(N, option_benefits, label=f'i={i},w={w},l={l},wr={wr}', ls='-')

if __name__ == '__main__':
    name = "NIO"
    a = 0.052
    P0 = 7.04
    P = np.arange(P0-2, P0+2, 0.01)
    B = [0, 0.03, 0.10, 0.35]
    # plot_long_short_profit(P0, P, 1, B, a, name)

    # C_call = [1.05, 0.6,    0.275, 0.125, 0.065]
    # C_put  = [0.015, 0.055, 0.235, 0.585, 1.025]
    # K      = [6.0,   6.5,   7.0,   7.5,   8.0]
    # T = [7./365, 7./365, 7./365, 7./365, 7./365]
    # # test_call_put_profit(P0, P, K, C_call, C_put, T, a, name)
    #
    # C0 = [1.05, 0.6, 0.275, 0.125, 0.065]
    # C1 = [0.6, 0.275, 0.125, 0.065, 0.035]
    # K0 = [6.0, 6.5, 7.0, 7.5, 8.0]
    # K1 = [6.5, 7.0, 7.5, 8.0, 8.5]
    # test_bear_call_spreed_profit(P0, P, C0, C1, K0, K1, T, a, name)

    plot_investment_profit()

    plt.legend()
    plt.grid()
    plt.show()