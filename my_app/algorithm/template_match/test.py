


from collections import Counter
import re
x='第4章 章  做个样本'
ptr=r'第(.*?)章'   #非贪心
result=re.findall(ptr,x)
print(result)
if result[0]!='':
    print('有东西')


x=[1,1,1,1,1,2,3,4,5,67,5,8,8]
y=Counter(x)
print(y)
print(y.most_common(1)[0][0])
print(list(dict(y).keys()))



x={'招标公告': 1, '投标人须知': 1, '评标办法': 1, '合同条款及格式（缺失）': 1, '系统实施合同条款(缺失)': 0, '合同生效': 0, '定义': 0, '合同标的': 0, '使用授权': 0, '合同标的总体要求': 0, '交付时间、地点': 0, '质量保证期': 0, '系统升级保证': 0, '知识产权及使用权(顺序错)': 0}

print(x.get('使用授权',None))










