# bonds_research
票据研究，reits研究


使用交易数据对到期量进行预测  

①时间戳管理  
pd.Timestamp
pd.Timestamp.to_period

②df加总及遍历  
df['turnOver 成交量（亿）'][index]  
for index, value in enumerate(t)
for index, row in d.iterrows()
X = func.iloc[:, 1:]

③w.edb()使用  

④read_excel  
df = pd.read_excel('预测模型_底稿_2.xlsx', sheet_name = 'trade')  

⑤write txt  
