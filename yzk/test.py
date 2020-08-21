import numpy as np
import pandas as pd
import re


def read_article():
    with open("predata3.txt", "r", encoding="utf8") as f:
        string = "".join([i for i in f.readlines()])
    results = string.split("%%%%%%%%%%")
    return results


def clean(string):
    cleanlist = ['责任编辑：']
    for i in cleanlist:
        if i in string:
            return True
    return False


def preprocessing(string):
    strlist = string.split('\n')
    result = []
    for i in strlist:
        if i.isdigit():
            continue
        if len(i.replace(' ', '')) == 0:
            continue
        # if clean(string):
        #     continue
        result.append(i)
    return result


def myrange(x):
    ls = [i * 10 for i in range(10)]
    for i, j in enumerate(ls):
        if x < j:
            return i
    return len(ls)


def get_risk(file):
    with open(file, 'r', encoding='utf8') as f:
        string = f.readlines()
        word = [i.replace('"', "") for i in string[0].replace("\n", "").split("+")]
    return word


if __name__ == '__main__':
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
    right = 0
    for i in range(2099):
        if 'p' + data.iloc[i]['max_index'] == data2.iloc[i]['max_index']:
            right += 1
    print(right)
