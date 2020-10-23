
from typing import List
from collections import Counter
x1=[['我','要','上','。','要','打','游'],['我','要','上','学','。','打','游','这','个']]

x2=[[0,1,1,1,0,1,0],[0,0,0,1,1,1,0,0,0]]

x3=[[11,11,11,11,11,11,11],[11,11,11,11,11,11,11,11,11]]

def my_split(x_list,x01_list,x3,flag):
    result=[]
    result01=[]
    result3=[]
    tem=[]
    tem01=[]
    tem3=[]
    for i in range(len(x_list)):
        if x_list[i]!=flag :
            tem.append(x_list[i])
            tem01.append(x01_list[i])
            tem3.append(x3[i])

            if i == len(x_list) - 1:
                tem.append(x_list[i])
                tem01.append(x01_list[i])
                tem3.append(x3[i])
                result.append(tem)
                result01.append(tem01)
                result3.append(tem3)
                tem = []
                tem01=[]
                tem3 = []
        else:
            tem.append(x_list[i])
            tem01.append(x01_list[i])
            tem3.append(x3[i])
            result.append(tem)
            result01.append(tem01)
            result3.append(tem3)
            tem=[]
            tem01=[]
            tem3 = []
    return result,result01,result3

arti=[]
arti01=[]
arti3=[]
for duan in range(len(x1)):
    y,y01,y3=my_split(x1[duan],x2[duan],x3[duan],'。')
    arti.append(y)
    arti01.append(y01)
    arti3.append(y3)
print(arti)
print(arti01)
print(arti3)

#计算每个句子的重复率
#这个句子可能有几个组号，这个句子属于哪个组，然后统计这个组号/句子长度

x=[1,2,6,8,98,5,4,3,3]
c=Counter(x)
print(dict(c))
print(c.most_common(1)[0][0])






















