from analysis import *
from snownlp import SnowNLP

if __name__ == '__main__':
    data = pd.read_csv('风险标签数据(2).csv', encoding='GB18030', engine='python')
    lablelist = data["情感分类"]
    string = ""
    templist = [t for t in data["标题"]]
    clist = [SnowNLP(r).sentiments for r in templist]
    wrong = 0
    for i in range(len(clist)):
        print(templist[i], clist[i], lablelist[i])
        c = 0 if clist[i] >= 0.6 else 2
        wrong += c != int(lablelist[i])
    print(wrong, wrong / 2100)
