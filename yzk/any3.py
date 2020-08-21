# encoding:utf-8
import codecs, jieba
import time
import json
import random
from sklearn import metrics


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
        self.pos = {i: 1 for i in self.posdict}
        self.neg = {i: 1 for i in self.negdict}
        # 程度副词词典
        self.mostdict = self.deal_wrap('dict/degree_dict/most.txt')  # 权值为2
        self.verydict = self.deal_wrap('dict/degree_dict/very.txt')  # 权值为1.5
        self.moredict = self.deal_wrap('dict/degree_dict/more.txt')  # 权值为1.25
        self.ishdict = self.deal_wrap('dict/degree_dict/ish.txt')  # 权值为0.5
        self.insufficientdict = self.deal_wrap('dict/degree_dict/insufficiently.txt')  # 权值为0.25
        self.inversedict = self.deal_wrap('dict/degree_dict/inverse.txt')  # 权值为-1
        # 同理得到程度副词的词典
        self.advdict = {}
        # self.advdict.update({i: 2 for i in self.mostdict})
        # self.advdict.update({i: 1.5 for i in self.verydict})
        # self.advdict.update({i: 1.25 for i in self.moredict})
        # self.advdict.update({i: 1.125 for i in self.ishdict})
        # self.advdict.update({i: 0.25 for i in self.insufficientdict})
        self.advdict.update({i: -1 for i in self.inversedict})

    def cal_score(self, word, sentence_score):
        if word in self.advdict.keys():
            sentence_score *= self.advdict[word]
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
                pos = self.pos[word]
                for w in sentence[s:i]:
                    pos = self.cal_score(w, pos)  # 得到消极积极词前面的程度副词，并进行加权
                s = i + 1  # 计算
                poslist.append((word, pos))
                posscore += pos
            elif word in self.negdict:
                neg = self.neg[word]
                for w in sentence[s:i]:
                    neg = self.cal_score(w, neg)
                negscore += neg
                neglist.append((word, neg))
                s = i + 1
            i += 1
        return posscore, negscore, poslist, neglist

    def train_init(self):
        with open("predata2.txt", "r", encoding='utf-8') as f:
            self.aclist = [i.replace("\n", "") for i in f.readlines()]
        with open("label.txt", 'r') as f:
            self.lablelist = [i.replace("\n", "") for i in f.readlines()]
        self.tempstrlist = []
        for tempstr in a.deal_wrap('predata.txt'):
            self.tempstrlist.append(tempstr)
        iter = 0
        self.cutlist = []
        for tempstr in self.tempstrlist:
            cut = []
            for x in self.preteat_clause(tempstr, self.aclist[iter]):
                c = self.cutwords_jieba(x, )
                cut.append(c)
            self.cutlist.append(cut)
            iter += 1
        self.k = 0

    def train(self, times=30, ahpla=0.002, k=300):
        self.alpha = ahpla
        self.k = k
        for i in range(times):
            print(i)
            self.run()

    def run(self):
        wrong = 0
        iter = 0
        posoffset = {}
        negoffset = {}
        start = time.time()
        y_true = []
        y_pred = []
        for cut in self.cutlist:
            if iter > self.k:
                break
            poslist = []
            neglist = []
            sentence_pscore1, sentence_nscore1 = 0, 0
            for c in cut:
                posscore, negscore, poslist, neglist = a.sentiment(c)
                sentence_pscore1 += posscore
                sentence_nscore1 += negscore
            sentiment = sentence_pscore1 - sentence_nscore1
            s1 = 0 if sentiment > 0 else 1
            label = int(self.lablelist[iter])
            label /= 2
            y_true.append(label)
            y_pred.append(s1)
            if label != s1:
                poslen = len(poslist)
                # possum = sum([float(i[1]) for i in poslist])
                neglen = len(neglist)
                if poslen + neglen:
                    offset = sentiment / (poslen + neglen)
                    # negsum = sum([float(i[1]) for i in neglist])
                    for i in poslist:
                        if poslen:
                            if i[0] in posoffset.keys():
                                posoffset[i[0]] -= self.alpha * offset
                            else:
                                posoffset[i[0]] = -self.alpha * offset
                    for i in neglist:
                        if neglen:
                            if i[0] in negoffset.keys():
                                negoffset[i[0]] += self.alpha * offset
                            else:
                                negoffset[i[0]] = self.alpha * offset
                wrong += 1
            iter += 1
            if iter % 100 == 0:
                print(iter, "wrong:", wrong, wrong / iter)
                end = time.time()
                print("循环运行时间:%.2f秒" % (end - start))
                start = end
        print(wrong, wrong / iter)
        print("accuracy_score:", metrics.accuracy_score(y_true=y_true, y_pred=y_pred))
        print("average_precision_score:", metrics.average_precision_score(y_true=y_true, y_score=y_pred))
        print("Precision:", metrics.precision_score(y_true, y_pred))
        print("Recall:", metrics.recall_score(y_true, y_pred))
        print("F1-score:", metrics.f1_score(y_true, y_pred))
        flag = 0
        for i in posoffset.keys() & self.pos.keys():
            self.pos[i] += posoffset[i]
            flag = 1
        for i in negoffset.keys() & self.neg.keys():
            self.neg[i] += negoffset[i]
            flag = 1
        if flag:
            print("update!")

    def dictprint(self):
        print({k: v for k, v in self.pos.items() if v != 1})
        print({k: v for k, v in self.neg.items() if v != 1})

    def predict(self):
        wrong = 0
        iter = 0
        y_true = []
        y_pred = []
        for cut in self.cutlist:
            if iter <= self.k:
                iter += 1
                continue
            sentence_pscore1, sentence_nscore1 = 0, 0
            for c in cut:
                posscore, negscore, poslist, neglist = a.sentiment(c)
                sentence_pscore1 += posscore
                sentence_nscore1 += negscore
            sentiment = sentence_pscore1 - sentence_nscore1
            s1 = 0 if sentiment > 0 else 1
            label = int(self.lablelist[iter])
            label /= 2
            y_true.append(label)
            y_pred.append(s1)
            if label != s1:
                wrong += 1
            iter += 1
            if iter % 100 == 0:
                print(iter, "wrong:", wrong, wrong / (iter - self.k))
        print(wrong, wrong / (2100 - self.k))
        print("accuracy_score:", metrics.accuracy_score(y_true=y_true, y_pred=y_pred))
        print("average_precision_score:", metrics.average_precision_score(y_true=y_true, y_score=y_pred))
        print("Precision:", metrics.precision_score(y_true, y_pred))
        print("Recall:", metrics.recall_score(y_true, y_pred))
        print("F1-score:", metrics.f1_score(y_true, y_pred))

    def save(self):
        with open('pospara.json', 'w') as f:
            js = json.dumps(self.pos)
            f.write(js)
        with open('negpara.json', 'w') as f:
            js = json.dumps(self.neg)
            f.write(js)

    def ignore(self, iglist):
        for i in iglist:
            while i in self.posdict:
                self.posdict.remove(i)
            while i in self.negdict:
                self.negdict.remove(i)


if __name__ == '__main__':
    start = time.time()
    a = Analysis()
    a.sentiment_init()
    a.train_init()
    with open('ignore.txt', 'r', encoding='utf8') as f:
        ignorelist = [i.replace("\n", "").replace(" ", "") for i in f.readlines()]
    a.ignore(ignorelist)
    a.train(k=700, times=30, ahpla=0.002)
    a.predict()
    a.save()
    end = time.time()
    print("循环运行时间:%.2f秒" % (end - start))
"""
300 20 0.008 608 0.3377777777777778
1000 10 0.008 385 0.35
2.0版本
300  10 0.008 595 0.33055555555555555
300  10 0.002 566 0.31444444444444447(全文本无操作 674 0.32095238095238093 )
300  30 0.002 302 0.27454545454545454
3.0版本
不计算副词 654 0.31142857142857144
计算负面副词 661 0.31476190476190474
"""
