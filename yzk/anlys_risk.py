# encoding:utf-8

import re
import json
from analysis import *
from test import *

start = 0
end = 2100
debug = 'i'
output = False
outputfile = f"risk.csv"

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
    risk = ['capital', 'debt', 'financing', 'quality', 'talent']
    risk_label = ["资本运作风险", '债务风险', '融资风险', '产品质量风险', '关键人才流失风险']
    risk_word = [get_risk(f'risk\\{k}.txt') for k in risk]
    # with open("risk.txt", 'r', encoding='utf8') as f:
    #     templist = [t.replace("\n","") for t in f.readlines()]
    templist = [preprocessing(t) for t in read_article()]
    alpha = 0.8
    beta = 1
    gamma = 0.5
    risklist = []
    sentlist=[]
    for tempstr in templist[1 + start:end + 1]:
        print(i)
        sentence_pscore1, sentence_nscore1 = 0, 0
        risk_score = [0] * 5
        risk_count = [0] * 5
        article_score = []
        sentence_score = []
        for j, res in enumerate(tempstr):
            article_sentiment = 0
            sentence_sentiment = []
            for x in a.preteat_clause(res, aclist[i]):
                # 传统方法
                c = a.cutwords_jieba(x, )
                posscore, negscore, poslist, neglist = a.sentiment(c)
                sentence_pscore1 += posscore
                sentence_nscore1 += negscore
                score = posscore - negscore
                article_sentiment += score
                sentence_sentiment.append(score)
                for k, words in enumerate(risk_word):
                    for w in words:
                        if w in x:
                            risk_count[k] += 1
                            risk_score[k] += score * gamma
            article_score.append(article_sentiment)
            sentence_score.append(sentence_sentiment)
            # for k, words in enumerate(risk_word):
            #     for w in words:
            #         if w in res:
            #             risk_score[k] += article_sentiment * beta

        sentiment = sentence_pscore1 - sentence_nscore1
        sentlist.append(sentiment)
        s1 = 0 if sentiment > 0 else 2
        risklist.append([risk_score[k] for k in range(5)])
        i += 1
    data = pd.concat([data, pd.DataFrame(columns=risk_label)])[start:end]
    data[risk_label] = risklist
    data['sentiment'] = sentlist
    data[['内容','情感分类','sentiment']+risk_label].to_csv(outputfile,index=False,encoding="utf_8_sig")
