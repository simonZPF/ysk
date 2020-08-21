# encoding:utf-8
import codecs, jieba
import pandas as pd
import re

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
        return [i for i in reslist if articlecompany in i]  # 返回分割好的语段列表

    def cutwords_jieba(self, sentence, stopwords='dict/stopwords.txt'):
        l = list(jieba.cut(sentence))  # 对sentence切分之后的结果存到l中
        return l

    def deal_wrap(self, filedict):
        temp = []
        try:
            for x in open(filedict, 'r', encoding='utf8').readlines():
                temp.append(x.strip())
        except Exception:
            for x in open(filedict, 'r', encoding='gbk').readlines():
                temp.append(x.strip())
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

    def sentiment_init(self):
        # 情感词典
        jieba.load_userdict("dict/userdict.txt")  # 添加自定义词典
        jieba.load_userdict("dict/emotion_dict/neg_all_dict.txt")
        jieba.load_userdict("dict/emotion_dict/pos_all_dict.txt")
        jieba.load_userdict("dict/emotion_dict/stop_words.txt")
        self.posdict = self.deal_wrap('dict/emotion_dict/pos_all_dict.txt')  # os.path.normpath(path) 规范path字符串形式
        self.negdict = self.deal_wrap('dict/emotion_dict/neg_all_dict.txt')
        # 程度副词词典
        self.mostdict = self.deal_wrap('dict/degree_dict/most.txt')  # 权值为2
        self.verydict = self.deal_wrap('dict/degree_dict/very.txt')  # 权值为1.5
        self.moredict = self.deal_wrap('dict/degree_dict/more.txt')  # 权值为1.25
        self.ishdict = self.deal_wrap('dict/degree_dict/ish.txt')  # 权值为0.5
        self.insufficientdict = self.deal_wrap('dict/degree_dict/insufficiently.txt')  # 权值为0.25
        self.inversedict = self.deal_wrap('dict/degree_dict/inverse.txt')  # 权值为-1
        # 同理得到程度副词的词典

    def cal_score(self, word, sentence_score):
        if word in self.mostdict:
            sentence_score *= 2.0
        elif word in self.verydict:
            sentence_score *= 1.5
        elif word in self.moredict:
            sentence_score *= 1.25
        elif word in self.ishdict:
            sentence_score *= 1.125
        elif word in self.insufficientdict:
            sentence_score *= 0.5
        elif word in self.inversedict:
            sentence_score *= -1
        return sentence_score

    def sentiment(self, sentence):
        '''
            723 34.4
        '''
        i, s, posscore, negscore = 0, 0, 0, 0
        poslist = []
        neglist = []
        for word in sentence:
            if word in self.posdict:
                pos = 1
                for w in sentence[s:i]:
                    pos = self.cal_score(w, pos)  # 得到消极积极词前面的程度副词，并进行加权
                s = i + 1  # 计算
                poslist.append((word, pos))
                posscore += pos
            elif word in self.negdict:
                neg = 1
                for w in sentence[s:i]:
                    neg = self.cal_score(w, neg)
                negscore += neg
                neglist.append((word, neg))
                s = i + 1
            i += 1
        return posscore, negscore, poslist, neglist


if __name__ == '__main__':
    a = Analysis()
    a.sentiment_init()
    string = ""
    sentlist = ["积极", "中立", "消极"]
    with open("predata2.txt", "r", encoding='utf-8') as f:
        aclist = [i.replace("\n", "") for i in f.readlines()]
    i = 0
    wrong = 0

    data = pd.read_csv('风险标签数据(2).csv', encoding='GB18030', engine='python')
    content = data['内容']
    pattern = re.compile(r'<(.*?)>')

    with open("label.txt", 'r') as f:
        lablelist = [i.replace("\n", "") for i in f.readlines()]
    for tempstr in a.deal_wrap('predata.txt'):
        print(i)
        if i <= 1400:
            i+=1
            continue
        sentence_pscore1, sentence_nscore1 = 0, 0
        pos = []
        neg = []
        for x in a.preteat_clause(tempstr, aclist[i]):
            # 传统方法
            c = a.cutwords_jieba(x, )
            posscore, negscore, poslist, neglist = a.sentiment(c)
            sentence_pscore1 += posscore
            sentence_nscore1 += negscore
            pos += poslist
            neg += neglist
        sentiment = sentence_pscore1 - sentence_nscore1
        s1 = 0 if sentiment > 0 else 2
        str1 = re.sub(pattern, "", content[i]).replace('　', "").replace(" ", "")
        for p in set(pos):
            str1 = str1.replace(p[0], f"[{p[0]}]")
        for n in set(neg):
            str1 = str1.replace(n[0], f"{{{n[0]}}}")
        if int(lablelist[i]) != s1:
            wrong += 1
            string += str(i) + f":\n{str1}\n" + str(sentlist[int(lablelist[i])]) + " " + str(sentiment) + "\n"
            string += "poslist: " + str(pos) + "\n" + "neglist: " + str(neg) + "\n\n"
        i += 1
        if i % 50 == 0:
            print("wrong:", wrong, wrong / i)
    print(wrong, wrong / 1400)
    with open("debug4.txt", "w") as f:
        f.write(string)

'''
400+
256
'''
