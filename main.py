
import pandas as pd
import numpy as ny
from datetime import datetime,timedelta
import os
from WindPy import w
from time import time
from multiprocessing import Process
from os import getpid

#将时间转换为标准月
def get_month(t):
    t = pd.Timestamp(t)
    t = t.to_period(freq = 'M')
    return t

#对（标准月，期限）求和
def sum_month(t1, t2, p):
    sum = 0
    num =  0
    for i in range(len(t_series)):
        if (get_month(t_series[i]) >= t1
        and get_month(t_series[i]) <= t2
        and limitDday_series[i] == p 
        and billType_series[i] == '银票'
        ):
            sum += turnOver_series[i]
            num += 1
    return sum

#输出指定期间 t1 ---> t2 的期限结构，输入标准月
def ratio(t1, t2):
    #1M,3M,6M,9M,1Y
    #初始化
    sum_1M = 0; sum_3M = 0; sum_6M = 0
    sum_9M = 0; sum_1Y = 0
    
    sum_1M += sum_month(t1, t2, '1M')
    sum_3M += sum_month(t1, t2, '3M')
    sum_6M += sum_month(t1, t2, '6M')
    sum_9M += sum_month(t1, t2, '9M')
    sum_1Y += sum_month(t1, t2, '1Y')

    sum = sum_1M + sum_3M + sum_6M + sum_9M + sum_1Y
    r_1M = sum_1M/sum; r_3M = sum_3M/sum
    r_6M = sum_6M/sum; r_9M = sum_9M/sum
    r_1Y = sum_1Y/sum
    return r_1M, r_3M, r_6M, r_9M, r_1Y

#设置计算期限结构所使用的交易数据时间段，输str'2021-06'
def ratio_period(predict_month, len_month):
    ratio_t1 = predict_month - len_month
    ratio_t2 = predict_month - last_month
    return ratio_t1, ratio_t2

#获取wind数据：.Data[0]贴现承兑余额:电子银票, .Data[1]票据贴现发生额:电子银票
def bill(m1, m2):
    ef1 = time()
    w.start()
    # bill = w.edb("M0329670,M0329682", m1, m2,"Fill=Previous")
    bill = w.edb("M0331243,M0329686", m1, m2,"Fill=Previous")
    ef2 = time()
    print('...2.Wind data loaded, ~ Time:', '%.3f' % (ef2 - ef1))
    return bill

#计算实际票据到期额，输入标准月
def due(t):
    num = 0
    for i in bill_data.Times:
        if get_month(i) == get_month(t):
            break
        else: num += 1
    k = bill_data.Data
    due_amount = k[0][num-1] + k[1][num] - k[0][num]
    return due_amount

#预测到期量，输入标准月
def due_predict(t):
    num = 0
    #获得预测月份的索引num
    for i in bill_data.Times:
        if get_month(i) == t: break
        else: num += 1
    #.Data[1]票据承兑发生额:电子银票
    d = bill_data.Data[1]
    #1M,3M,6M,9M,1Y
    ratio_t = ratio_period(t, len_month)
    r = ratio(ratio_t[0], ratio_t[1])
    predict_amount = (r[0]*d[num-1] + r[1]*d[num-3] 
                    + r[2]*d[num-6] + r[3]*d[num-9]
                    + r[4]*d[num-12])
    return predict_amount

if __name__ == '__main__':

    # print('cd=', os.getcwd())

    #读取数据文件，series后缀为列数据
    #时间数据需要使用get_month()来标准化
    ef1 = time()
    df = pd.read_excel('预测模型_底稿_2.xlsx', sheet_name = 'trade')
    ef2 = time()
    print('...1.xslx data loaded, ~ Time:', '%.3f' % (ef2 - ef1))
    t_series = df['dateTime']
    limitDday_series = df['limitDayType']
    billType_series = df['billType']
    turnOver_series = df['turnOver 成交量（亿）']

    #参数设置
    # predict_month = '2021-07'
    len_month = 12   #预测使用过去6个月的交易数据产生的期限结构
    last_month = 4   #默认为1，即过去12个月到上月，共计12个月
    bill_data = bill('2017-06', '2021-12')   #获取wind数据
    # ratio_period(predict_month, len_month)

    print('     latest wind data:   ', get_month(bill_data.Times[-1]))
    print('...3.Predict period:      2021-01 --->', get_month(bill_data.Times[-1])+1)
    print('     trading data use: last',last_month, '--->',len_month,'months\' data')
    
    #从2021-11倒算回2021-01
    t = get_month('2021-11')
    print('...4.Results:')
    ef1 = time()
    while t > get_month('2020-12'):

        t_predict = due_predict(t)
        file = open('results.txt', 'a')
        file.write('%.2f' % t_predict + '\n')
        print(t, 'due_predict:', '%.2f' % t_predict)
        t -= 1
    ef2= time()
    print('... ~ Calc Time:', '%.3f' % (ef2 - ef1))
    file.write('---above: from ' + str(last_month) + ' to ' + str(len_month) + ' months---\n')
    file.close()






    # print('predict_month =     ', predict_month)
    # print('ratio_month from:   ', start_month, '-->', end_month)

    # r = ratio('2021-01','2021-06')
    # print('The structure of limitDayType (1M/3M/6M/9M/1Y) is:')
    # for i in range(5):
    #     print('%.3f' % r[i])

