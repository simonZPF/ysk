# encoding:utf-8
import codecs, jieba
from gensim import corpora
from collections import defaultdict
from stanfordcorenlp import StanfordCoreNLP
import pandas as pd
import scipy.special
import os


class Analysis:
    def preteat_clause(self, phase, articlecompany):
        # 分句
        cut_list = list('。！~？!?…')
        reslist, i, start = [], 0, 0
        for word in phase:
            if word in cut_list:
                if phase[start:i] != '':
                    reslist.append(phase[start:i])  # 如果这一段字符不为空，放入reslist中
                start = i + 1
                i += 1
            else:
                i += 1
            # 通过上述来控制去除cut_list内容，将划分好的语段放入reslist中
        if start < len(phase):  # 说明一整段没有分隔符
            reslist.append(phase[start:])
        return [i for i in reslist]  # 返回分割好的语段列表

    def cutwords_jieba(self, sentence, stopwords='dict/stopwords.txt'):
        stropw = []

        # stropw = [line.strip() for line in open(stopwords,'r',encoding='utf-8').readlines()]

        # frequency = defaultdict(int)
        l = list(jieba.cut(sentence))  # 对sentence切分之后的结果存到l中
        return l

    # self.move_stopwords(l)
    # for t in l:
    # 	frequency[t] += 1
    #
    # texts = [token for token in frequency if frequency[token] > 0]
    #
    # rtexts = list(set(texts)-set(stropw))
    # return rtexts
    def deal_wrap(self, filedict):
        temp = []
        for x in open(filedict, 'r', encoding='utf-8').readlines():
            temp.append(x.strip())  # strip() 方法用于移除字符串头尾指定的字符（默认为空格或换行符）
        return temp  # 得到去除空格的字符串列表

    def deal_zw(self, filedict):
        temp = []
        with codecs.open(filedict, 'r+', encoding='utf8') as f:
            preline = ''  # 存当前行的上一行
            for line in f:
                if not line.startswith('<zw') and not line.startswith(
                        '<pl') and line != "" and line != '\n' and preline.startswith('<zw'):
                    temp.append(line.replace('\n', "").strip())  # line.replace('\n', "").strip()行尾的换行符去掉后，移除字符串头尾指定字符
                preline = line
        return temp

    # 创建停用词list
    def stopwordslist(self, filepath):
        stopwords = [line.strip() for line in codecs.open(filepath, 'r', encoding='utf-8').readlines()]
        return stopwords  # 从文件中读取出停用词（优化格式后的)

    # 对句子去除停用词
    def move_stopwords(self, sentence):
        stopwords = self.stopwordslist(u'dict\stopwords.txt')  # 这里加载停用词的路径
        for i in range(len(sentence))[::-1]:  # 取从后向前（相反）的元素
            if sentence[i] in stopwords:
                del sentence[i]
        return sentence

    def ignore(self, iglist):
        for i in iglist:
            while i in self.posdict:
                self.posdict.remove(i)
            while i in self.negdict:
                self.negdict.remove(i)

    def sentiment_init(self):
        # 情感词典

        jieba.load_userdict("dict/userdict.txt")  # 添加自定义词典
        jieba.load_userdict("dict/emotion_dict/neg_all_dict.txt")
        jieba.load_userdict("dict/emotion_dict/pos_all_dict.txt")
        jieba.load_userdict("dict/emotion_dict/stop_words.txt")
        # os.path.dirname(__file__)所在脚本是以完整路径被运行的， 那么将输出该脚本所在的完整路径
        self.posdict = self.deal_wrap(os.path.dirname(__file__) + '\\' + os.path.normpath(
            'dict/emotion_dict/pos_all_dict.txt'))  # os.path.normpath(path) 规范path字符串形式
        self.negdict = self.deal_wrap(os.path.dirname(__file__) + '\\' + os.path.normpath(
            'dict/emotion_dict/neg_all_dict.txt'))  # neg_all_dict-原.txt是记载原数据
        # 得到了消极和积极的词典
        # 程度副词词典
        self.mostdict = self.deal_wrap(
            os.path.dirname(__file__) + '\\' + os.path.normpath('dict/degree_dict/most.txt'))  # 权值为2
        self.verydict = self.deal_wrap(
            os.path.dirname(__file__) + '\\' + os.path.normpath('dict/degree_dict/very.txt'))  # 权值为1.5
        self.moredict = self.deal_wrap(
            os.path.dirname(__file__) + '\\' + os.path.normpath('dict/degree_dict/more.txt'))  # 权值为1.25
        self.ishdict = self.deal_wrap(
            os.path.dirname(__file__) + '\\' + os.path.normpath('dict/degree_dict/ish.txt'))  # 权值为0.5
        self.insufficientdict = self.deal_wrap(
            os.path.dirname(__file__) + '\\' + os.path.normpath('dict/degree_dict/insufficiently.txt'))  # 权值为0.25
        self.inversedict = self.deal_wrap(
            os.path.dirname(__file__) + '\\' + os.path.normpath('dict/degree_dict/inverse.txt'))  # 权值为-1
        # 同理得到程度副词的词典
        self.nlp = StanfordCoreNLP(r'stanford-corenlp-full-2016-10-31', lang='zh')

    def cal_score(self, word, sentence_score):
        if word in self.mostdict:
            sentence_score *= 2.0
        elif word in self.verydict:
            sentence_score *= 1.75
        elif word in self.moredict:
            sentence_score *= 1.5
        elif word in self.ishdict:
            sentence_score *= 1.2
        elif word in self.insufficientdict:
            sentence_score *= 0.5
        elif word in self.inversedict:
            sentence_score *= -1
        return sentence_score

    # 根据程度副词的情况和权值进行加权

    def sentiment(self, sentence):
        i, s, posscore, negscore = 0, 0, 0, 0
        poslist = []
        neglist = []
        for word in sentence:
            if word in self.posdict:
                poslist.append(word)
                posscore += 1
                for w in sentence[s:i]:
                    posscore = self.cal_score(w, posscore)  # 得到消极积极词前面的程度副词，并进行加权
                s = i + 1  # 计算

            elif word in self.negdict:
                negscore += 1
                neglist.append(word)
                for w in sentence[s:i]:
                    negscore = self.cal_score(w, negscore)
                s = i + 1
            i += 1
        return posscore, negscore

    # 生成每个词的子节点字典
    def get_parser_dict(self, words, tuples):
        child_dict = dict()
        tuplelist = tuples[1:]
        for index, arc in enumerate(
                tuplelist):  # enumerate() 函数用于将一个可遍历的数据对象(如列表、元组或字符串)组合为一个索引序列，同时列出数据和数据下标，一般用在 for 循环当中
            if words[arc[1] - 1] in child_dict:
                tuple = (arc[0], words[arc[-1] - 1])  # 第一个元素是关系，第二个元素是子节点词
                child_dict[words[arc[1] - 1]].append(tuple)
            else:
                child_dict[words[arc[1] - 1]] = []
                tuple = (arc[0], words[arc[-1] - 1])  # 第一个元素是关系，第二个元素是子节点词
                child_dict[words[arc[1] - 1]].append(tuple)
        return child_dict

    # 得到递归子节点字典

    def sentiment_by_rules(self, sentence, dependency):
        # 利用nlp提供的依存关系方法及分词方法来对其进行处理计算
        posscore, negscore = 0, 0
        deps = self.get_parser_dict(sentence, dependency)
        poslist = []
        neglist = []
        for word in sentence:
            if word in self.posdict:
                pos = 1
                if word in deps:
                    for w in deps[word]:
                        pos = self.cal_score(w[1], pos)
                posscore += pos
                poslist.append((word, pos))
            elif word in self.negdict:
                neg = 1
                if word in deps:
                    for w in deps[word]:
                        neg = self.cal_score(w[1], neg)
                negscore += neg
                neglist.append((word, neg))

        return posscore, negscore, poslist, neglist

    # view.py中的sentiment_by_rules方法引入过来
    def percentofsentiment_by_rules(self, comment):
        seg = self.nlp.word_tokenize(comment)
        posscore, negscore, poslist, neglist = self.sentiment_by_rules(seg, self.nlp.dependency_parse(comment))
        ppos = scipy.special.expit(float(posscore) - float(negscore))  # 正向可能性  sigmoid判断积极可能性大还是消极
        return ppos


if __name__ == '__main__':
    ''' 524 '''
    a = Analysis()
    a.sentiment_init()
    string = ""
    start = 0
    end = 2100
    debug = 'i'
    output = True
    outputfile = f"debug\debug{start}-{end}{debug}f.txt"

    data = pd.read_csv('风险标签数据(2).csv', encoding='GB18030', engine='python')
    lablelist = data["情感分类"]
    content = data['内容']
    ac = pd.read_csv('predata2.csv', encoding='utf8', engine='python')
    aclist = ac['aclist']
    bclist = ac['bclist']
    sentlist = ["积极", "中立", "消极"]
    with open('ignore.txt', 'r', encoding='utf8') as f:
        ignorelist = [i.replace("\n", "").replace(" ", "") for i in f.readlines()]
    a.ignore(ignorelist)
    i = start
    wrong = 0
    nlp = StanfordCoreNLP(r'stanford-corenlp-full-2016-10-31', lang='zh')
    templist = [i for i in a.deal_wrap('predata.txt')]
    for tempstr in templist[start:end]:
        print(i)
        sentence_pscore, sentence_nscore = 0, 0
        pos = []
        neg = []
        str1 = content[i]
        for x in a.preteat_clause(tempstr, aclist[i]):
            if x != "":
                posscore, negscore, poslist, neglist = a.sentiment_by_rules(nlp.word_tokenize(x),
                                                                            nlp.dependency_parse(x))
                sentence_pscore += posscore
                sentence_nscore += negscore
                pos += poslist
                neg += neglist
        sentiment = sentence_pscore - sentence_nscore
        for p in {i[0] for i in pos}:
            str1 = str1.replace(p, f"[{p}]")
        for n in {i[0] for i in neg}:
            str1 = str1.replace(n, "{" + str(n) + "}")
        s1 = 0 if sentiment > 0 else 2
        wrong += int(lablelist[i]) != s1
        if int(lablelist[i]) != s1 or debug == 'o':
            string += str(i) + f":\n{str1}\n" + str(sentlist[int(lablelist[i])]) + " " + str(sentiment) + "\n"
            string += f"主题公司：{aclist[i]},提交公司：{bclist[i]}\nposlist: " + str(pos) + "\n" + "neglist: " + str(
                neg) + "\n\n"
        i += 1
        if (i - start) % 50 == 0 and i - start:
            print("wrong:", wrong, wrong / (i - start))
    if output:
        with open(outputfile, "w", encoding='utf8') as f:
            f.write(string)
