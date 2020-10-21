# -*- coding: utf-8 -*-
# 发表了讲话。界正经历百年未有之大变局，科技创新
# 学习，央政治局10月16日下午就量子科技研究和应
# 分析我国量子科技发展形势，更好推进我国量子科

x=r'发表了讲话。界正经历百年未有之大变局，科技创新习近平在主持学习时发表了讲话。界正经历百年未有之大变局，科技创新是其中一个他指出，近年来，量子科技发展突飞猛进，成为新一轮科技革命和产业变革的前沿领域。\n加快发展量子科技，梁成波梁成波梁成波梁成波梁成波对促进高质量发展、保障国家安全具有非常重要的作用。\n安排这次集体学习，央政治局10月16日下午就量子科技研究和应目的是了解世界量子科技发展态势，梁成波梁成波分析我国量子科技发展形势，更好推进我国量子科技发展。'
y=r'境外输入现有确诊病例246例(其中重症病例1例)发表了讲话。界正经历百年未有之大变局，科技创新，现有疑似病例5例。\n累计确诊病例3097例，累计治愈出院病例2851例，无死亡病例学习，央政治局10月16日下午就量子科技研究和应。截至10月16日24时，究和应目的是了解世界量子科技发展态势据31个省(自治区、直辖市)和新疆生产建设兵团报告。\n现有确诊病例259例(其中重症病例5例)，累计治愈出院病例80766例，累计死亡病例4634例，累计报告确诊病例85659例，现有疑似病例5例。\n累计追踪到密切接触者844662人，尚在梁成波梁成波梁成波梁成波梁成波分析我国量子科技发展形势，更好推进我国量子科医学观察的密切接触者8040人。'
# xx=r'牛客网讨论区,互联网求职学习交流社区,为程序员、工程师、产品、运营、留学生提供笔经面经,面试经验,招聘信息,内推,实习信息,校园招聘,社会招聘,职业发展,薪资福利'
# x=r',互联网求职学习交流社区,为程序员、工程师、产品、运营、留学生提供笔经面经,面试经验,招聘信息,内推,实习信息,校园招聘,社会招聘,职'




xx=x.split(r'\n')
y=y.split(r'\n')   #r''里面的\n会变成\\n
print('分组后:',y)
#判''
#判大小
#


def label_doc1(x):
    hash2posi_dic={}
    for duan in range(len(x)):
        # print('长度:',len(x[duan]))
        for num in range(len(x[duan])):
            # print('第几个:',duan,num)
            if not hash2posi_dic.get(x[duan][num]):
                # print('收集:',x[duan][num],duan,num)
                hash2posi_dic[x[duan][num]]=tuple([duan,num])
    return hash2posi_dic





def gengerate_n_gram(string, n=13):
    n_gram = []
    for i in range(len(string) - n + 1):
        n_gram.append(string[i:i + n])
    # print('做成的n_gram', len(n_gram))
    return n_gram

def build_gram(x):
    result=[]
    for duan in range(len(x)):
        gram_temp=gengerate_n_gram(x[duan])
        result.append(gram_temp)
    return result
print('输入前长度:',len(y[0]))
z=build_gram(y)
print('输入后长度:',len(z[0]))


print(len(z))


def calculate_hashing_set(n_gram, Base=17, n=13):
    # print('输入的gram长度:',len(n_gram))
    hashinglist = []
    hash = 0
    first_gram = n_gram[0]
    # 单独计算第一个n_gram的哈希值
    for i in range(n):  # 0到5
        hash += ord(first_gram[i]) * (Base ** (n - i - 1))  # 这个才是最标准的hash计算，后面那些都是加进来
    hashinglist.append(hash)
    Base_n_1 = (Base ** (n - 1))  # 不要每次for循环都计算一次次方，降低复杂度
    for i in range(1, len(n_gram)):  # 主要这里耗时  #前一个和后一个只差一个字符
        pre_gram = n_gram[i - 1]
        this_gram = n_gram[i]
        hash = (hash - ord(pre_gram[0]) * Base_n_1) * Base + ord(this_gram[n - 1])  # 这里重复计算了gram_0
        hashinglist.append(hash)
    return hashinglist  # 每个gram一个hash值

def gram_hash(x):
    result=[]
    for duan in range(len(x)):
        # print('x长度',len(x[duan]),'段:',duan)
        duan_hash=calculate_hashing_set(x[duan])
        result.append(duan_hash)
    return result





z=gram_hash(z)


print('doc2的编码',z)
print(len(z))#3组
print(len(z[0]))#38
print(len(y[0]))
# z={}
# print(z.get(0))

doc2_gram_dic=label_doc1(z)
print('字典:',doc2_gram_dic)

# 开始查询第一段
doc1_gram_=build_gram(xx)
print('doc1_gram_',doc1_gram_)
doc1_hash=gram_hash(doc1_gram_)
print(doc1_hash)

doc2_key_set=set(doc2_gram_dic.keys())
result=[]
result_index2=[]
result_01=[]
conti_condi=0
for i in range(len(doc1_hash)):
    temp=['']*len(xx[i]) #本段的
    temp2 = [''] * len(xx[i])
    temp_01=[0]*len(xx[i])
    for j in range(len(doc1_hash[i])):
        if conti_condi:#连续状态
            pass
        else:#非连续状态
            if doc1_hash[i][j] in doc2_key_set:
                duan, num = doc2_gram_dic[doc1_hash[i][j]]
                for k in range(13):
                    temp[j+k]=y[duan][num+k]
                    temp2[j + k]=tuple([duan,num+k,y[duan][num+k]])
                    temp_01[j + k]=1
                # temp[j]=doc2_gram_dic[doc1_hash[i][j]] # tuple装进temp

    result.append(temp) # temp段 装进文章
    result_index2.append(temp2)
    result_01.append(temp_01)
            # print(i,j)
print(result)
all_result=[]
for i in range(len(result)):
    all_result.append(''.join(result[i]))
print(all_result)

print('result_index2',result_index2)
print('result_01',result_01)
# 给doc1分组

all_group=[]
contin_flag=0
count = 0
group_num = 0

for i in range(0,len(result_01)):
    duan1_group=[]
    s = 0
    e = 0

    for j in range(1,len(result_01[i])):
        if (result_01[i][j]!=result_01[i][j-1]):# 跳变
            # print('段:',duan,j,result_01[i][j-1],result_01[i][j])
            if (result_01[i][j-1]==1):
                duan1_group.append(tuple([group_num,s,e]))   # 取的时候 (s:e+1)
                group_num+=1
            else:
                duan1_group.append(tuple([-1, s, e]))
            s=j
            e=j
        else:
            e=j
    # 如果还有没有tuple包起来的
    if (e!=s):
        if (result_01[i][j - 1] == 1):
            duan1_group.append(tuple([group_num, s, e]))
            group_num +=1
        else:
            duan1_group.append(tuple([-1, s, e]))

    all_group.append(duan1_group)

print('all_group',all_group)

doc2_group_index=[]
#给doc2做index(分组编号)，还没tuple
for i in range(len(y)):
    duan2_group = [-1]*len(y[i])
    doc2_group_index.append(duan2_group)
print('刚建立的doc2_group_index',doc2_group_index)

# 便利doc1_tuple，查出doc1对应doc2的下标


#遍历doc1 tuple  写入到doc2_group_index
latest_group=-1
new_group_old={}
for i in range(len(all_group)):# all_group 是 doc1 tuple
    for j in range(len(all_group[i])):
        a,b,c = all_group[i][j]
        if (a==-1):
            pass
        else:
            # print('非-1')
            w_count = 0
            for k in range(b,c+1):#k是遍历doc1_2_doc2的
                # print('k值',i,k)
                d,e,f=result_index2[i][k] # d是段号  e是第几个   f是字
                if doc2_group_index[d][e]==-1:
                    # print('doc2可以填入',a,d,e,f)
                    doc2_group_index[d][e]=a #给分组标号
                    w_count+=1
                else:
                    latest_group=doc2_group_index[d][e]
            if w_count < 13:#单独属于这个句子的太少了，那就整组转换

                old_group = latest_group#设置阈值，然后做整个组号转化
                new_group = a
                new_group_old[new_group] = old_group

print('改组参考字典L:',new_group_old)
# 给doc1 tuple改组
exis_new_group = set(new_group_old.keys())

for i in range(len(all_group)):
    for j in range(len(all_group[i])):
        a,b,c=all_group[i][j]
        if a in exis_new_group:

            all_group[i][j] = tuple([new_group_old[a], b, c])


print('doc2_group_index',doc2_group_index)
print('修改后的doc1_tuple：',all_group)



# 给doc2分tuple

result_doc2_tuple=[]
for i in range(len(doc2_group_index)):
    s = 0
    e = 0
    temp_tuple=[]
    for j in range(len(doc2_group_index[i])):
        if doc2_group_index[i][j]!=doc2_group_index[i][j-1]:
            temp_tuple.append(tuple([doc2_group_index[i][j-1],s,e]))
            s=j
            e=j
        else:
            e=j
    if e!=s:
        temp_tuple.append(tuple([doc2_group_index[i][j - 1], s, e]))
    result_doc2_tuple.append(temp_tuple)

print('result_doc2_tuple:',result_doc2_tuple)


# print(y[1][31:55])

# 发表了讲话。界正经历百年未有之大变局，科技创新
# 学习，央政治局10月16日下午就量子科技研究和应
# 分析我国量子科技发展形势，更好推进我国量子科

# x=r'境外输入现有确诊病例246例(其中重症病例1例)(发表了讲话。界正经历百年未有之大变局，科技创)新，现有疑似病例5例。\n累计确诊病例3097例，累计治愈出院病例2851例，无死亡病例(学习，央政治局10月16日下午就量子科技研究和应)。截至10月16日24时，(究和应目的是了解世界量子科技发展态)势据31个省(自治区、直辖市)和新疆生产建设兵团报告。\n现有确诊病例259例(其中重症病例5例)，梁成波累计治愈出院病例80766例，累计死亡病例4634例，累计报告确诊病例85659例，现有疑似病例5例。\n累计追踪到密切接触者844662人，尚在(梁成波分析我国量子科技发展形势，更好推进我国量子科)医学观察的密切接触者8040人。'
# xx=r'发表了讲话。界正经历百年未有之大变局，科技创新习近平在主持学习时发表了讲话。界正经历百年未有之大变局，科技创新是其中一个他指出，近年来，量子科技发展突飞猛进，成为新一轮科技革命和产业变革的前沿领域。\n加快发展量子科技，对促进高质量发展、保障国家安全具有非常重要的作用。\n安排这次集体(学习，央政治局10月16日下午就量子科技)研(究和应目的是了解世界量子科技发展态)势，(梁成波分析我国量子科技发展形势，更好推进我国量子科)技发展。'
for i in range(len(result_doc2_tuple)):
    for j in range(len(result_doc2_tuple[i])):
        a,b,c=result_doc2_tuple[i][j]
        if a!=-1:
            print(y[i][b:c+1])