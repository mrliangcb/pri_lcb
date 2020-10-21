import time
from my_app.algorithm.winnowing import win_check


def cal_time(item):
    def out_wrape(func):
        def in_wrape(*args,**kwargs):
            s=time.time()
            result=func(*args,**kwargs)
            e=time.time()
            print('[ {} ]的耗时:{}'.format(item,e-s))
            return e-s,result #返回func结果和运行时间
        return in_wrape
    return out_wrape


def dup_dict(dup_text):
    dup_dic = {}
    for j, k in enumerate(dup_text):  # 很多个短语，编号从0开始
        dup_dic[j] = k
    return dup_dic


def doc1_tuple(doc1_01_list):
    doc1_wrap = []
    s = 0
    e = 0
    group_count = 0

    # 给doc1分组 成tuple
    for i in range(1, len(doc1_01_list)):
        if (doc1_01_list[i - 1] != doc1_01_list[i]):  # 转折点 装载，并且更新s和e
            if (doc1_01_list[i - 1] != 0):
                doc1_wrap.append(tuple([group_count, s, e]))
                group_count += 1
            else:
                doc1_wrap.append(tuple([-1, s, e]))
            s = i
            e = i
        else:
            e = i  # 没遇到转折点 只更新e 不管s
    if (doc1_01_list[i] != 0):
        doc1_wrap.append(tuple([group_count, s, e]))
        group_count += 1
    else:
        doc1_wrap.append(tuple([-1, s, e]))
    return doc1_wrap


# doc2分组
def doc2_2_group(
        doc2_str,doc1_wrap,doc1_from_doc2):
    new_old_dic = {}
    doc2_group = [''] * len(doc2_str)
    for tup in doc1_wrap:
        a, b, c = tup
        if a >= 0:  # 就是匹配的内容  x_y=[-1,-1,0,-1,2,0,2,2,-1,-1]   做一个数组，装着对应的doc1分组
            print('第几组:', a, b, c)
            w_count = 0
            for i in range(b, c + 1):  #
                # print(type(i),type(b),type(c))
                # print('doc1_01_index[i]是什么',doc1_01_index[i])
                if doc2_group[doc1_from_doc2[i]] == '':
                    doc2_group[doc1_from_doc2[i]] = a
                    w_count += 1  # 记录填入了多少
            if w_count < 13:  # 如果填入的小于13  认为doc1这个句子和已经建立分组的doc1-doc2完全相同，只需要将现在这个组号改成旧的已经建立好的doc1-doc2
                old_group = doc2_group[doc1_from_doc2[i]]  # doc2组号数组已经赋值了，是前面的组
                new_group = a  # 新组不能覆盖，只能在doc1的tuple分组号的new改成old
                new_old_dic[new_group] = old_group

    return doc2_group,new_old_dic

# doc2_tuple
def doc2_tuple(
        doc2_group):
    s = 0
    e = 0
    doc2_group_ = []
    for i in range(1, len(doc2_group)):  # 0~24
        # print('第几个',i)
        if doc2_group[i - 1] != doc2_group[i]:  # 状态转变
            if doc2_group[i - 1] == '':
                doc2_group_.append(tuple([-1, s, e]))  # 分组号  起点  终点
            else:
                doc2_group_.append(tuple([doc2_group[i - 1], s, e]))
            s = i
            e = i
        elif doc2_group[i - 1] == doc2_group[i]:
            e = i
    if doc2_group[i - 1] == '':
        doc2_group_.append(tuple([-1, s, e]))  # 分组号  起点  终点
    else:
        doc2_group_.append(tuple([doc2_group[- 1], s, e]))
    return doc2_group_

def calll():
    print('尝试读外部函数')




@cal_time('check_str')
def check_str(
        doc1_str,doc2_str,k=13):

    winnowing = win_check()
    n = k
    t = 9
    if n > len(doc1_str) or n > len(doc2_str):
        return None

    similiarize,duplicate,doc1_from_doc2,doc1_01_list = winnowing.get_sim(doc1_str, doc2_str, n, t)
    print('两篇文章的相似度为{:5f}'.format(similiarize))

    dup_dic=dup_dict(duplicate)
    doc1_wrap=doc1_tuple(doc1_01_list) # doc1计算tuple

    #doc2 分组
    doc2_group,new_old_dic=doc2_2_group(doc2_str,doc1_wrap,doc1_from_doc2)  # doc2_str,doc1_wrap,doc1_from_doc2

    # 改doc1:
    exis_new_group = set(new_old_dic.keys())

    for i in range(len(doc1_wrap)):
        a, b, c = doc1_wrap[i]
        if a in exis_new_group:  # 如果这个组号是New_group 多余的  那就改成old
            doc1_wrap[i] = tuple([new_old_dic[a], b, c])

    # doc2_tuple
    doc2_wrap=doc2_tuple(doc2_group)

    print('doc2_wrap是什么?',doc2_wrap)
    return [similiarize, duplicate, dup_dic, doc1_str, doc2_str, doc1_wrap, doc2_wrap]





