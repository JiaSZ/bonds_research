from ctypes import cdll
from WindPy import w
import numpy as np
import pandas as pd
# from statsmodels.formula.api import ols
import statsmodels.api as sm
import sys


#目录设置
# cd = 'F:/Projects/python Project/citics/2021-12-11'
# sys.path.append(cd)

print(__name__)

#读取Wind数据
#数据时间：由早至晚
def reit(r):
    r=w.wsd(r, "close,pct_chg", start_date, end_date, "")
    return r

#计算胜率并输出
def calc(y,x):
    w.start()
    print('------------------------------------------------------------------------------')
    print("------------------- calc from ",start_date," --> ",end_date,"-------------------")
    print('------------------------------------------------------------------------------')
    print('y=',y,',x=',x)
    
    y=reit(y)
    x=reit(x)

    #这是计算滞后胜率，输入滞后阶数m，但是从0滞后算起，
    n = 0
    while n < m+1:
        if n != 0:
            lagf=lag(y,x,1)
        else:
            lagf=[y,x]
        y=lagf[0]
        x=lagf[1]
        length = len(y.Data[1])
        #计算胜率
        c = 0
        l = length
        while l>0:
            if x.Data[1][l-1]*y.Data[1][l-1]>0: c += 1
            l -= 1
        print("ratio=",'%.3f' % (c/len(y.Data[1])), "| lag=", n, "length=", length)
        n += 1




    # print('------------------------------------------------------------------------------')
    # if results.params[0] > 0:
    #     print("ρ=",'%.3f' % results.rsquared ** 0.5, "| lag=", m, "\n")
    # else: print("ρ=",'%.3f' % (results.rsquared ** 0.5 * (-1)), "| lag=",m,"\n")

#设置分析时间段
def period(a):
    if a=="day":
        t1 = "2021-06-21"
        t2 = "2021-12-10"
    elif a==1:
        t1 = "2021-06-21"
        t2 = "2021-07-14"
    elif a==2:
        t1 = "2021-07-15"
        t2 = "2021-09-10"
    elif a==3:
        t1 = "2021-09-13"
        t2 = "2021-12-10"
    elif a=='2+3':
        t1 = "2021-07-15"
        t2 = "2021-12-10"
    return t1,t2

def lag(y,x,m):
    while m>0:
        m -= 1
        y.Data[1].pop(0)
        x.Data[1].pop(-1)
    return y,x
    


if __name__ == "__main__":

    #预设y，x范围
    r1="180201.sz"    #平安广州广河REIT
    r4="508001.sh"    #浙商沪杭甬REIT
    GSGL="801175.SI"   #高速公路

    r2="508006.sh"    #富国首创水务REIT
    UW="801164.SI"     #水务

    r3="180801.sz"    #中航首钢绿能REIT
    HB="801162.SI"     #环保

    r5="180101.sz"    #博时蛇口产园REIT
    r6="508000.sh"    #华安张江光大REIT
    r8="508027.sh"    #东吴苏园产业REIT
    YQKF="801182.SI"   #园区开发

    r7="180301.sz"    #红土盐田港REIT
    r9="508056.sh"    #中金普洛斯REIT
    WL="801178.SI"    #物流
    
    t = period('2+3')         #可选择'day'，week，1，2，3,'2+3'
    m = 5                 #滞后阶数，默认为0
    start_date = t[0]
    end_date = t[1]

    calc(r2,UW)           #输入y（reit），x（权益类）


    




