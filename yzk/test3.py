import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
# 数据
"""
<10 133 344 0.3866279069767442
10-19 86 305 0.2819672131147541
20-29 56 293 0.19112627986348124
30-39 47 224 0.20982142857142858
40-49 36 182 0.1978021978021978
50-59 40 173 0.23121387283236994
60-69 28 118 0.23728813559322035
70-79 19 115 0.16521739130434782
80-89 13 78 0.16666666666666666
90< 58 267 0.21722846441947566
516 2100 0.2458313482610767
"""
# x = np.arange(10)
# Bj = [133, 86, 56, 47, 36, 40, 28, 19, 13, 58]
# Sh = [344, 305, 293, 224, 182, 173, 118, 115, 78, 267]
# print(sum(Bj[2:])/sum(Sh[2:]))
data = pd.read_csv('风险标签数据(2).csv', encoding='GB18030', engine='python')
content = data['内容']
with open('anlys.txt', 'r') as f:
    result = [i.replace('\n', '') for i in f.readlines()]
namelist = result[::3]
plist = [[float(j) for j in i.split(",") if j] for i in result[1::3]]
wordlist = result[2::3]
cumlist = [np.cumsum(i) for i in plist]
labellist = [i.split("-", 2) for i in namelist]
pattern = re.compile(r'<(.*?)>')

wrong = 0
wrong2 = 0
count = 0
for i, cum in enumerate(cumlist):
    length = len(cum)
    if length < 20:
        continue
    print(i)
    with open(f"pic\\txts\\{namelist[i]}.txt", 'w',encoding='utf8') as f:
        str1 = re.sub(pattern, "", content[i]).replace('　', "").replace(" ", "")
        f.write(str1)
    # mmax = max(cum)
    # mmin = min(cum)
    # bmax = list(cum).index(mmax)
    # bmin = list(cum).index(mmin)
    # flg1 = 0.8 * length > bmax > 0.2 * length
    # flg2 = 0.8 * length > bmin > 0.2 * length  # 185 668 0.27694610778443113
    # if flg1 and not flg2 or (not flg1 and flg2):
    #     count += 1
    #     if labellist[i][1] == '错误':
    #         wrong += 1
    #         print(i)
    #         # d = cum[-1] - np.average(cum[-10:-2])
    #         # if '消极' in labellist[i][2]:  # 72 185 0.3891891891891892
    #         #     wrong2 += d > 0
    #         #     if d > 0:
    #
    #         # plt.plot(cum)
    #         # plt.title(f'{namelist[i]}')
    #         # plt.savefig(f'pic\\class1\\{namelist[i]}.png')
    #         # plt.close()
    #         # if '积极' in labellist[i][2]:
    #         #     wrong2 += d < 0
    #         #     if d < 0:
    #         #         with open(f"pic\\class2\\{namelist[i]}.txt", 'w') as f:
    #         #             str1 = re.sub(pattern, "", content[i]).replace('　', "").replace(" ", "")
    #         #             f.write(str1)
    #         #         plt.plot(cum)
    #         #         plt.title(f'{namelist[i]}')
    #         #         plt.savefig(f'pic\\class2\\{namelist[i]}.png')
    #         #         plt.close()
# print(wrong, count, wrong / count)
# print(wrong2, wrong, wrong2 / wrong)
# 无转折
# 111 782 0.14194373401534527
# 70 111 0.6306306306306306
# 有转折
# 185 668 0.27694610778443113
# 111 185 0.6
