



import pandas as pd
import statsmodels.api as sm

def lag(y,x,m):
    if m == 0: return y,x
    else:
        b = y[m:]
        a = x[:-m]
        return b,a


def main():
    df = pd.read_excel('reits(2)_py.xlsx', sheet_name = 'Sheet5')
    y = df['C-REITs指数：综合'].tolist()
    x = df['10债收益率：变动'].tolist()

    lag_index = 21
    ylag = lag(y,x, lag_index)[0]
    xlag = lag(y,x, lag_index)[1]
    results = sm.OLS(ylag, sm.add_constant(xlag)).fit()

    print(results.summary(), 'lag = ', lag_index)

    

    print('----------------all circumstances--------------------')

    while lag_index >= 0:
        ylag = lag(y,x, lag_index)[0]
        xlag = lag(y,x, lag_index)[1]
        results = sm.OLS(ylag, sm.add_constant(xlag)).fit()
        if results.params[1] > 0:
            print("ρ=",'%.3f' % results.rsquared ** 0.5, 'params =', '%.2f' % results.params[1], "| lag=", lag_index)
        else: print("ρ=",'%.3f' % (results.rsquared ** 0.5 * (-1)), 'params =', '%.2f' % results.params[1], "| lag=", lag_index)
        lag_index -= 1
    




if __name__ == '__main__':
    main()


