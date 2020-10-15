from flask import Flask, render_template, request,jsonify
import re, os
import docx
import time
import json
from winnowing import win_check

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

@cal_time('check_str')
def check_str(doc1_str,doc2_str,k=13):
    winnowing = win_check()
    n = k
    t = 9
    if n > len(doc1_str) or n > len(doc2_str):
        return None

    similiarize, dup_text, doc1_01_index, doc1_flag_list = winnowing.get_sim(doc1_str, doc2_str, n, t)


    print('两篇文章的相似度为{:5f}'.format(similiarize))

    dup_dic = {}
    for j, k in enumerate(dup_text):  # 很多个短语，编号从0开始
        dup_dic[j] = k
    doc1_wrap = []
    s = 0
    e = 0
    group_count = 0

    # 给doc1分组 成tuple
    for i in range(1, len(doc1_flag_list)):
        if doc1_flag_list[i - 1] != doc1_flag_list[i]:  # 转折点 装载，并且更新s和e
            if doc1_flag_list[i - 1] != 0:
                doc1_wrap.append(tuple([group_count, s, e]))
                group_count += 1
            else:
                doc1_wrap.append(tuple([-1, s, e]))
            s = i
            e = i
        else:
            e = i  # 没遇到转折点 只更新e 不管s

    if doc1_flag_list[i - 1] != 0:
        doc1_wrap.append(tuple([group_count, s, e]))
        group_count += 1
    else:
        doc1_wrap.append(tuple([-1, s, e]))

    # 给doc2分组
    new_old_dic = {}
    doc2_group = [''] * len(doc2_str)

    for tup in doc1_wrap:
        a, b, c = tup
        if a >= 0:  # 就是匹配的内容  x_y=[-1,-1,0,-1,2,0,2,2,-1,-1]   做一个数组，装着对应的doc1分组
            print('第几组:', a, b, c)
            w_count = 0
            for i in range(b, c + 1):  #
                if doc2_group[doc1_01_index[i]] == '':
                    doc2_group[doc1_01_index[i]] = a
                    w_count += 1  # 记录填入了多少
            if w_count < 13:  # 如果填入的小于13  认为doc1这个句子和已经建立分组的doc1-doc2完全相同，只需要将现在这个组号改成旧的已经建立好的doc1-doc2
                old_group = doc2_group[doc1_01_index[i]]  # doc2组号数组已经赋值了，是前面的组
                new_group = a  # 新组不能覆盖，只能在doc1的tuple分组号的new改成old

                new_old_dic[new_group] = old_group  # 查找如果有new_group组号，就改成old的   有多个new_group ，但只有一个old
    exis_new_group = set(new_old_dic.keys())

    for i in range(len(doc1_wrap)):
        a, b, c = doc1_wrap[i]
        if a in exis_new_group:  # 如果这个组号是New_group 多余的  那就改成old
            doc1_wrap[i] = tuple([new_old_dic[a], b, c])
        # 在给doc2分组 成tuple
        s = 0
        e = 0
        doc2_group_ = []
    for i in range(1, len(doc2_group)):
        if doc2_group[i - 1] != doc2_group[i]:
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

    return [similiarize,dup_text, dup_dic, doc1_str, doc2_str, doc1_wrap, doc2_group_]

# time_,result=check_str('123123123234523452345234523452345234123123123123123234523452345234523452345234','123123123234523452345234523452345234') #有可能文章长度小于k_gram
# print(time_)
# print(result)

app = Flask(__name__)
@app.route('/dup_check', methods=['POST','GET'])  # 用法 r = requests.post(url, files=files)
def dup_check():
    args_dic = request.args
    print('收到的参数字典:',args_dic)
    time_,result = check_str(args_dic['doc1'], args_dic['doc2'],k=13)
    # 文本长度小于k
    print('args_dicdoc1:',args_dic['doc1'])
    if len(args_dic['doc1'])<13 or len(args_dic['doc2']) <13:
        return jsonify(str('错误 : 文本长度太短'))


    print('时间',time_)
    print('结果', result)
    similiarize, dup_text, dup_dic, doc1_str, doc2_str, doc1_wrap, doc2_group_=result

    # return jsonify(json.dumps(result))
    result1=str(similiarize)
    result2=render_template('testHtml.html', name1='doc1', name2='doc2', time=time_, dup_check=similiarize,
                               dup_text=dup_text, dup_dic=dup_dic,doc1_str=doc1_str,doc2_str=doc2_str,doc1_wrap=doc1_wrap,doc2_group_=doc2_group_)
    return jsonify([result1,result2])
    # return jsonify(render_template('testHtml.html', name1='doc1', name2='doc2', time=time_, dup_check=similiarize,
    #                            dup_text=dup_text, dup_dic=dup_dic,doc1_str=doc1_str,doc2_str=doc2_str,doc1_wrap=doc1_wrap,doc2_group_=doc2_group_))

if __name__ == '__main__':
    app.run("0.0.0.0",debug=True,port=5002)