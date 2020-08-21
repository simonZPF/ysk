# coding:utf8
import pandas as pd

data = pd.read_csv('risk_p.csv')
data2 = pd.read_csv('risk3.csv')
risk_label = ["资本运作风险", '债务风险', '融资风险', '产品质量风险', '关键人才流失风险']
risk_label2 = ['p' + i for i in risk_label]
data = data[risk_label]
data['max_index'] = data.abs().idxmax(axis=1)
data['max_value'] = data[risk_label].abs().max(axis=1)
data2 = data2[risk_label2]
data2['max_index'] = data2.abs().idxmax(axis=1)
data2['max_value'] = data2[risk_label2].abs().max(axis=1)
risk = pd.read_csv("risk_p.csv")
right1, right2 = 0, 0
count1 = 0
count2 = 0
# print(data[:10])
# print(data2[:10])
for i in range(2099):
    if risk.iloc[i]["情感分类"] == 2:
        count1 += 1
        if 'p' + data.iloc[i]['max_index'] == data2.iloc[i]['max_index']:
            right1 += 1
    if risk.iloc[i]["sentiment"] < 0:
        count2 += 1
        if 'p' + data.iloc[i]['max_index'] == data2.iloc[i]['max_index']:
            right2 += 1
print(right1,count1)
print(right2,count2)
