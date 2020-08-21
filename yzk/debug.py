# encoding:utf-8

import re
import json
from analysis import *
from test import *

start = 0
end = 2100
debug = 'i'
output = False
outputfile = f"debug\debug{start}-{end}{debug}f.txt"

if __name__ == '__main__':
    a = Analysis()
    a.sentiment_init()
    sentlist = ["积极", "中立", "消极"]
    wrong = 0
    data = pd.read_csv('风险标签数据(2).csv', encoding='GB18030', engine='python')
    content = data['内容']
    pattern = re.compile(r'<(.*?)>')
    ac = pd.read_csv('predata2.csv', encoding='utf8', engine='python')
    aclist = ac['aclist']
    bclist = ac['bclist']
    lablelist = data["情感分类"]
    with open('ignore.txt', 'r', encoding='utf8') as f:
        ignorelist = [i.replace("\n", "").replace(" ", "") for i in f.readlines()]
    if debug == 'i':
        a.ignore(ignorelist)
    i = start
    string = ""
    templist = [preprocessing(t) for t in read_article()]

    long = [0] * 11
    lwrong = [0] * 11
    for tempstr in templist[1 + start:end]:
        print(i)
        sentence_pscore1, sentence_nscore1 = 0, 0
        pos = []
        neg = []
        lg = len(tempstr)
        for j, res in enumerate(tempstr):
            for x in a.preteat_clause(res, aclist[i]):
                # 传统方法
                c = a.cutwords_jieba(x, )
                posscore, negscore, poslist, neglist = a.sentiment(c)
                # if j == lg - 1:  # 520
                #     posscore *= 2
                #     negscore *= 2
                sentence_pscore1 += posscore
                sentence_nscore1 += negscore
                pos += poslist
                neg += neglist
        sentiment = sentence_pscore1 - sentence_nscore1
        s1 = 0 if sentiment > 0 else 2
        str1 = re.sub(pattern, "", content[i]).replace('　', "").replace(" ", "")
        for p in {i[0] for i in pos}:
            str1 = str1.replace(p, f"[{p}]")
        for n in {i[0] for i in neg}:
            str1 = str1.replace(n, "{" + str(n) + "}")
        # if int(lablelist[i]) != s1 or debug == 'o':
        r = int(lablelist[i]) != s1
        wrong += r
        l = len(pos) + len(neg)
        k = myrange(l)
        long[k] += 1
        lwrong[k] += r
        # string += str(i) + f":\n{str1}\n" + str(sentlist[int(lablelist[i])]) + " " + str(sentiment) + "\n"
        # string += f"主题公司：{aclist[i]},提交公司：{bclist[i]}\nposlist: " + str(pos) + "\n" + "neglist: " + str(
        #     neg) + "\n\n"

        i += 1
        if (i - start) % 100 == 0:
            print("wrong:", wrong, wrong / (i - start))
            for j in range(11):
                if long[j]:
                    print(f"worng{j}", lwrong[j], long[j], lwrong[j] / long[j])
    print(wrong, wrong / (end - start))
    for j in range(11):
        if long[j]:
            print(f"worng{j}", lwrong[j], long[j], lwrong[j] / long[j])
    if output:
        with open(outputfile, "w", encoding='utf8') as f:
            f.write(string)
