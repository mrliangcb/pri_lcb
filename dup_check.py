from flask import jsonify,Blueprint,request,render_template
from my_app.forms import check_args_validation
from . import web
from my_app.algorithm.dup_check_algo import check_str
from my_app.algorithm.duan_winnowing import paragraph_winnowing
# -*- coding: utf-8 -*-
 #把注册好的蓝图拿来用



@web.route('/NLP/Algorithm/base/dup_check/winnowing2', methods=['POST','GET'])
def dup_check():
    # args_dic = request.args  # 这个是不可变字典，如果转成普通字典
    print('当前路由winnowing2')
    args_dic=request.form.to_dict()

    try:
        dic=request.args.to_dict()
        doc1=dic['doc1']
        doc2=dic['doc2']
        a, b = check_args_validation(dic)
    except:
        dic=request.form.to_dict()
        doc1=dic['doc1']
        doc2=dic['doc2']
        a, b = check_args_validation(dic)
    if not a:
        return b

    time_, result = check_str(str(doc1), str(doc2), k=13)
    similiarize, dup_text, dup_dic, doc1_str, doc2_str, doc1_wrap, doc2_wrap = result

    result1 = str(similiarize)
    result2 = dup_dic
    result3 = render_template('testHtml.html', name1='doc1', name2='doc2', time=time_, dup_check=similiarize,
                              dup_text=dup_text, dup_dic=dup_dic, doc1_str=doc1_str, doc2_str=doc2_str,
                              doc1_wrap=doc1_wrap, doc2_group_=doc2_wrap)
    result4 = render_template('add_href_doc1.html', doc1_wrap=doc1_wrap, doc1_str=doc1_str)
    result5 = render_template('add_href_doc2.html', doc2_group_=doc2_wrap, doc2_str=doc2_str)

    print('重复文本字典：',result2)
    result6 = time_
    result7 = doc1_str
    result = doc2_str
    # return result4

    result_dic = {'dup_rate': result1,
                  'doc1_label': result4,
                  'doc2_label': result5}
    return jsonify(result_dic)
    # return jsonify([result1, result2, result3, result4, result5, result6])


    # return result4


# http://127.0.0.1:5002/NLP/Algorithm/base/dup_check/winnowing?doc1=中双方均希望对本协议所述保密资料及信息予以有效保护&doc2=双方均希望对本协议所述保密资料及信息予以有效保护两
# 0.96
import time

@web.route('/NLP/Algorithm/base/dup_check/winnowing', methods=['POST','GET'])
def dup_check2():
    # args_dic = request.args  # 这个是不可变字典，如果转成普通字典
    print('当前路由winnowing')
    args_dic=request.form.to_dict()
    print('当前时间:',time.localtime(time.time()))

    try:
        dic=request.args.to_dict()
        doc1=dic['doc1']
        doc2=dic['doc2']
        # a, b = check_args_validation(dic)
    except:
        dic=request.form.to_dict()
        doc1=dic['doc1']
        doc2=dic['doc2']
        # a, b = check_args_validation(dic)
    # if not a:
    #     return b

    doc1=doc1.split(r'\n')
    doc2 = doc2.split(r'\n')
    print('split之后doc1:',doc1)
    print('split之后doc2:', doc2)

    all_doc1=[]
    for i in range(len(doc1)):
        if doc1[i]:#如果不为空
            all_doc1.append(doc1[i])
    doc1=all_doc1

    all_doc2 = []
    for i in range(len(doc2)):
        if doc2[i]:  # 如果不为空
            all_doc2.append(doc2[i])
    doc2 = all_doc2


    example=paragraph_winnowing()
    s_time=time.time()
    similarity,result_str,doc1_wrap,doc2_wrap=example.get_sim(doc1,doc2)
    time_=time.time()-s_time
    for duan in range(len(doc1_wrap)):
        for num in range(len(doc1_wrap[duan])):
            a,b,c=doc1_wrap[duan][num]
            doc1_wrap[duan][num]=tuple([duan,a,b,c])
    for duan in range(len(doc2_wrap)):
        for num in range(len(doc2_wrap[duan])):
            a,b,c=doc2_wrap[duan][num]
            doc2_wrap[duan][num]=tuple([duan,a,b,c])

    print('similarity:',similarity)
    result1=similarity
    result3 = render_template('testHtml2.html', name1='doc1', name2='doc2', time=time_, dup_check=similarity,doc1_str=doc1, doc2_str=doc2,
                    doc1_wrap=doc1_wrap, doc2_group_=doc2_wrap)
    result4 = render_template('add_href_doc1_2.html', doc1_wrap=doc1_wrap, doc1_str=doc1)
    result5 = render_template('add_href_doc2_2.html', doc2_group_=doc2_wrap, doc2_str=doc2)

    result_dic = {'dup_rate': result1,
                  'doc1_label': result4,
                  'doc2_label': result5}

    print('doc1_wrap:',doc1_wrap)
    print('doc2_wrap:', doc2_wrap)

    return jsonify(result_dic)



    #
    #
    # time_, result = check_str(str(doc1), str(doc2), k=13)
    # similiarize, dup_text, dup_dic, doc1_str, doc2_str, doc1_wrap, doc2_wrap = result
    #
    # result1 = str(similiarize)
    # result2 = dup_dic
    # result3 = render_template('testHtml.html', name1='doc1', name2='doc2', time=time_, dup_check=similiarize,
    #                           dup_text=dup_text, dup_dic=dup_dic, doc1_str=doc1_str, doc2_str=doc2_str,
    #                           doc1_wrap=doc1_wrap, doc2_group_=doc2_wrap)
    # result4 = render_template('add_href_doc1.html', doc1_wrap=doc1_wrap, doc1_str=doc1_str)
    # result5 = render_template('add_href_doc2.html', doc2_group_=doc2_wrap, doc2_str=doc2_str)
    #
    # print('重复文本字典：',result2)
    # result6 = time_
    # result7 = doc1_str
    # result = doc2_str
    # # return result4
    #
    # return result4
    #
    # result_dic = {'dup_rate': result1,
    #               'doc1_label': result4,
    #               'doc2_label': result5}
    # return jsonify(result_dic)

















