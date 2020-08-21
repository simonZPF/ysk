import pandas as pd
import re


def preteat_clause(phase, articlecompany):
    # 分句
    cut_list = list('，。！~？!?…')
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
    return [i for i in reslist if articlecompany in i]


data = pd.read_csv('风险标签数据(2).csv', encoding='GB18030', engine='python')
content = data['内容']
ArticleCompany = data["主体公司"]
ArticleCompany2 = data["提交公司"]

# pattern = re.compile(r'<(.*?)>')
# string = ''
# with open("predata.txt", 'w', encoding='utf-8') as f:
#     for i in content:
#         string += re.sub(pattern, "", i).replace("\n", "").replace(" ", "").replace('　　', "") + "\n"
#     f.write(string)
# rl = []
# for i in content:
#     string = re.sub(pattern, "", i).replace("\n", "").replace(" ", "").replace('　　', "") + "\n"
#     rl.append(string)
# data["content"] = rl
# data[["content", "情感分类"]].to_csv("predata.csv")

pattern = re.compile(r'ArticleCompany\(name=(.*?),')
# matchObj = re.findall(pattern, ArticleCompany[5])
string = ''
aclist = []
bclist = []
for i in range(len(ArticleCompany)):
    if not pd.isnull(ArticleCompany[i]):
        r = re.findall(pattern, ArticleCompany[i])
        aclist.append(r[0])
    else:
        aclist.append("null")
    if not pd.isnull(ArticleCompany2[i]):
        r = re.findall(pattern, ArticleCompany2[i])
        bclist.append(r[0])
    else:
        bclist.append("null")
data['aclist'] = aclist
data['bclist'] = bclist
data[["aclist", "bclist"]].to_csv("predata2.csv")
# with open("label.txt","w") as f:
#     for i in data["情感分类"]:
#         string+=str(i)+'\n'
#     f.write(string)
