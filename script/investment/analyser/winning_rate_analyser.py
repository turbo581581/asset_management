import matplotlib.pyplot as plt
import numpy as np

def final_profits(profit_percentage, loss_percentage, n, ratio):
    return pow(1 + profit_percentage, n * ratio) * pow(1 - loss_percentage, n * (1 - ratio))

def winning_chance():
    profit_percentage = np.arange(0, 1, 0.01)
    loss_percentage = 0.5 * profit_percentage
    N = 10
    for r in np.arange(0.3, 0.6, 0.05):
        final = []
        for profit, loss in zip(profit_percentage, loss_percentage):
            final.append(final_profits(profit, loss, N, r))
        plt.plot(profit_percentage, final, label="N={},win chance={:.2f}".format(N, r))
    plt.xlabel("profit, loss=0.5*profit")
    plt.ylabel('final_profits')
    plt.legend()
    plt.grid()
    plt.show()

if __name__ == '__main__':
    winning_chance()