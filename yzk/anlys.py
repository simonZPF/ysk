# encoding:utf-8

import re
import json
from analysis import *
import matplotlib.pyplot as plt


class Analysis2(Analysis):
    def sentiment(self, sentence):
        i, s, posscore, negscore = 0, 0, 0, 0
        poslist = []
        wordfreq = {}
        for word in sentence:
            if word not in wordfreq.keys():
                wordfreq[word] = 1
            else:
                wordfreq[word] += 1
            if word in self.posdict:
                pos = 1
                if wordfreq[word] < 4:
                    for w in sentence[s:i]:
                        pos = self.cal_score(w, pos)  # 得到消极积极词前面的程度副词，并进行加权
                    poslist.append((pos, word))
                s = i + 1
            elif word in self.negdict:
                neg = -1
                if wordfreq[word] < 4:
                    for w in sentence[s:i]:
                        neg = self.cal_score(w, neg)
                    poslist.append((neg, word))
                s = i + 1
            i += 1
        return poslist


if __name__ == '__main__':
    '''513'''
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False
    a = Analysis2()
    a.sentiment_init()
    sentlist = ["积极", "中立", "消极"]

    wrong2 = 0
    data = pd.read_csv('风险标签数据(2).csv', encoding='GB18030', engine='python')
    ac = pd.read_csv('predata2.csv', encoding='utf8', engine='python')
    aclist = ac['aclist']
    bclist = ac['bclist']
    lablelist = data["情感分类"]
    with open('ignore.txt', 'r', encoding='utf8') as f:
        ignorelist = [i.replace("\n", "").replace(" ", "") for i in f.readlines()]
    a.ignore(ignorelist)
    templist = [t for t in a.deal_wrap('predata.txt')]
    headlist = data["标题"]
    i = 0
    para = [1]
    K = len(para)
    wrong = 0
    string = ""
    for tempstr in templist:
        plist = []
        print(i)
        for x in a.preteat_clause(tempstr, aclist[i]):
            c = a.cutwords_jieba(x, )
            plist += a.sentiment(c)
        ans = sum([k[0] for k in plist])
        slist = [str(k[0]) for k in plist]
        wlist = [k[1] for k in plist]
        name = ["正确", "错误"]
        label = ["right", "wrong"]
        s1 = 0 if ans > 0 else 2
        right = int(lablelist[i]) != s1
        string += f'{i + 1}-{name[right]}-{sentlist[lablelist[i]]}({ans})' + '\n' + ','.join(slist) + '\n'
        string += ','.join(wlist)+'\n'
        wrong += right
        if (i + 1) % 50 == 0 and i:
            print(f"wrong:", wrong, wrong / (i + 1))
        i += 1
    with open("anlys.txt", 'w') as f:
        f.write(string)
