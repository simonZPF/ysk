import pandas as pd
import re

data = pd.read_csv('风险标签数据(2).csv', encoding='GB18030', engine='python')
content = data['内容']
category = data['情感分类']
pattern = re.compile(r'<(.*?)>')

string = ''
with open("predata3.txt", 'w', encoding='utf-8') as f:
    for i, str1 in enumerate(content):
        string += f"\n%%%%%%%%%%{i+1}\n"
        string += re.sub(pattern, "", str1).replace(" ", "").replace('　　', "") + "\n"
    f.write(string)

rl = []
# for i in content:
#     string = re.sub(pattern, "", i).replace("\n", "").replace(" ", "").replace('　　', "") + "\n"
#     rl.append(string)
